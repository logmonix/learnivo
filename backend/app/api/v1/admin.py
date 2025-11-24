from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from app.core.database import get_db
from app.models.curriculum import Subject, Chapter, ContentBlock
from app.models.user import Profile
from app.models.progress import StudentProgress
from app.schemas.admin import AdminStats, BulkGenerateRequest, ContentBlockUpdate
from app.schemas.curriculum import SubjectResponse
from app.services.ai.orchestrator import ai_orchestrator
from app.api.v1.admin_deps import require_admin

router = APIRouter()

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Get platform statistics for admin dashboard."""
    
    # Count subjects
    result = await db.execute(select(func.count(Subject.id)))
    total_subjects = result.scalar()
    
    # Count chapters
    result = await db.execute(select(func.count(Chapter.id)))
    total_chapters = result.scalar()
    
    # Count students
    result = await db.execute(select(func.count(Profile.id)))
    total_students = result.scalar()
    
    # Count completed lessons
    result = await db.execute(
        select(func.count(StudentProgress.id))
        .where(StudentProgress.status == 'completed')
    )
    total_lessons_completed = result.scalar()
    
    return {
        "total_subjects": total_subjects or 0,
        "total_chapters": total_chapters or 0,
        "total_students": total_students or 0,
        "total_lessons_completed": total_lessons_completed or 0
    }

@router.post("/bulk-generate", response_model=List[SubjectResponse])
async def bulk_generate_curriculum(
    request: BulkGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Generate multiple subjects at once."""
    
    generated_subjects = []
    
    for subject_name in request.subject_names:
        # Check if exists
        result = await db.execute(
            select(Subject)
            .where(Subject.name == subject_name)
            .where(Subject.grade_level == request.grade_level)
        )
        existing = result.scalars().first()
        
        if existing:
            generated_subjects.append(existing)
            continue
        
        # Generate via AI
        try:
            ai_data = await ai_orchestrator.generate_curriculum(request.grade_level, subject_name)
        except Exception as e:
            continue  # Skip on error
        
        # Save
        new_subject = Subject(
            name=subject_name,
            grade_level=request.grade_level,
            description=f"AI Generated curriculum for {subject_name}",
            icon_name="book"
        )
        db.add(new_subject)
        await db.flush()
        
        chapters_data = ai_data.get("chapters", [])
        for idx, chap in enumerate(chapters_data):
            new_chapter = Chapter(
                subject_id=new_subject.id,
                title=chap.get("title", "Untitled Chapter"),
                description=chap.get("description", ""),
                order_index=idx + 1
            )
            db.add(new_chapter)
        
        await db.commit()
        await db.refresh(new_subject)
        generated_subjects.append(new_subject)
    
    return generated_subjects

@router.get("/content-blocks")
async def list_content_blocks(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """List all generated content blocks for review."""
    result = await db.execute(
        select(ContentBlock)
        .order_by(ContentBlock.created_at.desc())
        .limit(50)
    )
    return result.scalars().all()

@router.put("/content-blocks/{block_id}")
async def update_content_block(
    block_id: str,
    update: ContentBlockUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Edit AI-generated content."""
    result = await db.execute(select(ContentBlock).where(ContentBlock.id == block_id))
    block = result.scalars().first()
    
    if not block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    block.content_data = update.content_data
    await db.commit()
    
    return {"message": "Content updated successfully"}
