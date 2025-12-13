from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.models.curriculum import Chapter, ContentBlock
from app.models.user import Profile
from app.models.progress import StudentProgress
from app.services.ai.orchestrator import ai_orchestrator
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/{chapter_id}/lesson")
async def get_or_generate_lesson(
    chapter_id: str,
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get lesson content for a chapter. Generates if not exists."""
    
    # 1. Get chapter
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = result.scalars().first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # 2. Check if lesson already exists
    result = await db.execute(
        select(ContentBlock)
        .where(ContentBlock.chapter_id == chapter_id)
        .where(ContentBlock.block_type == 'lesson')
    )
    content_block = result.scalars().first()
    
    if not content_block:
        # 3. Generate lesson via AI
        try:
            lesson_data = await ai_orchestrator.generate_lesson(
                chapter.title,
                chapter.description or "",
                5  # TODO: Get from profile
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")
        
        # 4. Save to DB
        content_block = ContentBlock(
            chapter_id=chapter_id,
            block_type='lesson',
            content_data=lesson_data,
            ai_model_used='mock'
        )
        db.add(content_block)
        await db.commit()
        await db.refresh(content_block)
    
    # 5. Get or create progress
    result = await db.execute(
        select(StudentProgress)
        .where(StudentProgress.profile_id == profile_id)
        .where(StudentProgress.chapter_id == chapter_id)
    )
    progress = result.scalars().first()
    
    if not progress:
        progress = StudentProgress(
            profile_id=profile_id,
            chapter_id=chapter_id,
            status='in_progress'
        )
        db.add(progress)
        await db.commit()
    
    return {
        "chapter": {
            "id": str(chapter.id),
            "title": chapter.title,
            "description": chapter.description
        },
        "lesson": content_block.content_data,
        "progress": {
            "status": progress.status,
            "score": progress.score,
            "total_questions": progress.total_questions
        }
    }

@router.post("/{chapter_id}/submit-quiz")
async def submit_quiz(
    chapter_id: str,
    profile_id: str,
    answers: Dict[int, str],
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Submit quiz answers and calculate score."""
    
    # 1. Get quiz content
    result = await db.execute(
        select(ContentBlock)
        .where(ContentBlock.chapter_id == chapter_id)
        .where(ContentBlock.block_type == 'quiz')
    )
    content_block = result.scalars().first()
    if not content_block:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # 2. Calculate score
    # content_data is directly the quiz dict {"questions": [...]}
    questions = content_block.content_data.get('questions', [])
    
    correct_count = 0
    for idx, question in enumerate(questions):
        user_answer = answers.get(idx)
        if user_answer == question.get('correct_answer'):
            correct_count += 1
    
    total_questions = len(questions)
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # 3. Calculate XP (10 XP per correct answer)
    xp_earned = correct_count * 10
    
    # 4. Update progress
    result = await db.execute(
        select(StudentProgress)
        .where(StudentProgress.profile_id == profile_id)
        .where(StudentProgress.chapter_id == chapter_id)
    )
    progress = result.scalars().first()
    
    if progress:
        progress.status = 'completed'
        progress.score = correct_count
        progress.total_questions = total_questions
        progress.xp_earned = xp_earned
        progress.completed_at = datetime.utcnow()
    
    # 5. Update profile XP
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalars().first()
    if profile:
        profile.xp += xp_earned
        profile.coins += correct_count * 5  # 5 coins per correct answer
    
    await db.commit()
    
    return {
        "score": correct_count,
        "total": total_questions,
        "percentage": score_percentage,
        "xp_earned": xp_earned,
        "coins_earned": correct_count * 5
    }

@router.get("/{chapter_id}/quiz")
async def get_quiz(
    chapter_id: str,
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve the quiz content for a chapter.
    Returns the stored quiz JSON (questions, options, etc.) and progress info.
    """
    # 1️⃣ Fetch the quiz ContentBlock
    result = await db.execute(
        select(ContentBlock)
        .where(ContentBlock.chapter_id == chapter_id)
        .where(ContentBlock.block_type == "quiz")
    )
    quiz_block = result.scalars().first()
    if not quiz_block:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 2️⃣ Ensure a StudentProgress row exists (lazy creation)
    result = await db.execute(
        select(StudentProgress)
        .where(StudentProgress.profile_id == profile_id)
        .where(StudentProgress.chapter_id == chapter_id)
    )
    progress = result.scalars().first()
    if not progress:
        progress = StudentProgress(
            profile_id=profile_id,
            chapter_id=chapter_id,
            status="not_started",
        )
        db.add(progress)
        await db.commit()

    return {
        "quiz": quiz_block.content_data,
        "progress": {
            "status": progress.status,
            "score": progress.score,
            "total_questions": progress.total_questions,
        },
    }
