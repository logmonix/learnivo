from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.core.database import get_db
from app.models.curriculum import Subject, Chapter
from app.schemas.curriculum import SubjectCreate, SubjectResponse, GenerateCurriculumRequest
from app.services.ai.orchestrator import ai_orchestrator
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[SubjectResponse])
async def get_subjects(
    grade: int = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all subjects, optionally filtered by grade."""
    query = select(Subject).options(selectinload(Subject.chapters))
    if grade:
        query = query.where(Subject.grade_level == grade)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/generate", response_model=SubjectResponse)
async def generate_curriculum(
    request: GenerateCurriculumRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Triggers AI to generate a curriculum (Subject + Chapters).
    If subject exists, it returns it. If not, it generates it.
    """
    # 1. Check if subject already exists
    result = await db.execute(
        select(Subject)
        .where(Subject.name == request.subject_name)
        .where(Subject.grade_level == request.grade_level)
        .options(selectinload(Subject.chapters))
    )
    existing_subject = result.scalars().first()
    if existing_subject:
        return existing_subject

    # 2. Generate content via AI
    try:
        ai_data = await ai_orchestrator.generate_curriculum(request.grade_level, request.subject_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")

    # 3. Save to DB
    new_subject = Subject(
        name=request.subject_name,
        grade_level=request.grade_level,
        description=f"AI Generated curriculum for {request.subject_name}",
        icon_name="book" # Default icon
    )
    db.add(new_subject)
    await db.flush() # Get ID

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
    
    # Re-fetch to ensure relationships are loaded
    result = await db.execute(
        select(Subject)
        .where(Subject.id == new_subject.id)
        .options(selectinload(Subject.chapters))
    )
    return result.scalars().first()
