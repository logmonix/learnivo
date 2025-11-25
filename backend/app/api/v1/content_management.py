from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.curriculum import Subject, Chapter
from app.schemas.chapter import ChapterCreate, ChapterUpdate
from app.api.v1.admin_deps import require_admin

router = APIRouter()

@router.get("/subjects/{subject_id}/chapters")
async def get_subject_chapters(
    subject_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Get all chapters for a subject."""
    result = await db.execute(
        select(Chapter)
        .where(Chapter.subject_id == subject_id)
        .order_by(Chapter.order_index)
    )
    return result.scalars().all()

@router.post("/subjects/{subject_id}/chapters")
async def create_chapter(
    subject_id: str,
    chapter: ChapterCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Create a new chapter."""
    # Verify subject exists
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    new_chapter = Chapter(
        subject_id=subject_id,
        title=chapter.title,
        description=chapter.description,
        order_index=chapter.order_index
    )
    db.add(new_chapter)
    await db.commit()
    await db.refresh(new_chapter)
    
    return new_chapter

@router.put("/chapters/{chapter_id}")
async def update_chapter(
    chapter_id: str,
    chapter_update: ChapterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Update chapter details."""
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = result.scalars().first()
    
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    if chapter_update.title is not None:
        chapter.title = chapter_update.title
    if chapter_update.description is not None:
        chapter.description = chapter_update.description
    if chapter_update.order_index is not None:
        chapter.order_index = chapter_update.order_index
    
    await db.commit()
    await db.refresh(chapter)
    
    return chapter

@router.delete("/chapters/{chapter_id}")
async def delete_chapter(
    chapter_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Delete a chapter."""
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = result.scalars().first()
    
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    await db.delete(chapter)
    await db.commit()
    
    return {"message": "Chapter deleted successfully"}

# ============================================
# Chapter-Image Association Endpoints
# ============================================

from app.schemas.image import (
    ChapterImageCreate,
    ChapterImageUpdate,
    ChapterImageResponse,
    ChapterImageListResponse,
    ImageResponse
)
from app.services.image_service import image_service

def _build_image_url(image_id: str) -> str:
    """Build the URL for accessing an image."""
    return f"/api/v1/images/{image_id}/file"

def _image_to_response(image) -> ImageResponse:
    """Convert Image model to ImageResponse schema."""
    return ImageResponse(
        id=image.id,
        filename=image.filename,
        original_filename=image.original_filename,
        file_path=image.file_path,
        file_size=image.file_size,
        mime_type=image.mime_type,
        width=image.width,
        height=image.height,
        uploaded_by=image.uploaded_by,
        created_at=image.created_at,
        updated_at=image.updated_at,
        url=_build_image_url(str(image.id))
    )

@router.post("/chapters/{chapter_id}/images", response_model=ChapterImageResponse)
async def add_image_to_chapter(
    chapter_id: str,
    image_data: ChapterImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Associate an image with a chapter.
    
    - **chapter_id**: ID of the chapter
    - **image_id**: ID of the image to associate
    - **caption**: Optional caption for the image
    - **display_order**: Order of the image (default: 0)
    """
    # Verify chapter exists
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = result.scalars().first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter_image = await image_service.associate_image_with_chapter(
        chapter_id=chapter_id,
        image_id=image_data.image_id,
        caption=image_data.caption,
        display_order=image_data.display_order,
        db=db
    )
    
    # Refresh to load relationships
    await db.refresh(chapter_image, ["image"])
    
    return ChapterImageResponse(
        id=chapter_image.id,
        chapter_id=chapter_image.chapter_id,
        image_id=chapter_image.image_id,
        display_order=chapter_image.display_order,
        caption=chapter_image.caption,
        created_at=chapter_image.created_at,
        image=_image_to_response(chapter_image.image)
    )

@router.get("/chapters/{chapter_id}/images", response_model=ChapterImageListResponse)
async def get_chapter_images(
    chapter_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Get all images associated with a chapter.
    
    - **chapter_id**: ID of the chapter
    - Returns images ordered by display_order
    """
    # Verify chapter exists
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = result.scalars().first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter_images = await image_service.get_chapter_images(chapter_id, db)
    
    # Load image relationships
    response_items = []
    for ci in chapter_images:
        await db.refresh(ci, ["image"])
        response_items.append(
            ChapterImageResponse(
                id=ci.id,
                chapter_id=ci.chapter_id,
                image_id=ci.image_id,
                display_order=ci.display_order,
                caption=ci.caption,
                created_at=ci.created_at,
                image=_image_to_response(ci.image)
            )
        )
    
    return ChapterImageListResponse(
        chapter_images=response_items,
        total=len(response_items)
    )

@router.delete("/chapters/{chapter_id}/images/{image_id}")
async def remove_image_from_chapter(
    chapter_id: str,
    image_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Remove an image association from a chapter.
    
    - **chapter_id**: ID of the chapter
    - **image_id**: ID of the image to remove
    - Note: This only removes the association, not the image itself
    """
    await image_service.remove_image_from_chapter(chapter_id, image_id, db)
    return {"message": "Image removed from chapter successfully"}

@router.put("/chapters/{chapter_id}/images/{image_id}/order", response_model=ChapterImageResponse)
async def update_image_order(
    chapter_id: str,
    image_id: str,
    order_data: ChapterImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Update the display order of an image in a chapter.
    
    - **chapter_id**: ID of the chapter
    - **image_id**: ID of the image
    - **display_order**: New display order
    """
    if order_data.display_order is None:
        raise HTTPException(status_code=400, detail="display_order is required")
    
    chapter_image = await image_service.update_image_order(
        chapter_id=chapter_id,
        image_id=image_id,
        new_order=order_data.display_order,
        db=db
    )
    
    # Refresh to load relationships
    await db.refresh(chapter_image, ["image"])
    
    return ChapterImageResponse(
        id=chapter_image.id,
        chapter_id=chapter_image.chapter_id,
        image_id=chapter_image.image_id,
        display_order=chapter_image.display_order,
        caption=chapter_image.caption,
        created_at=chapter_image.created_at,
        image=_image_to_response(chapter_image.image)
    )
