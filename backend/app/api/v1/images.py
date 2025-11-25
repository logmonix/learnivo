from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import math

from app.core.database import get_db
from app.api.v1.admin_deps import require_admin
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.schemas.image import (
    ImageUploadResponse,
    ImageResponse,
    ImageListResponse
)
from app.services.image_service import image_service

router = APIRouter()

# New endpoint: allow any authenticated user to upload images (student upload)
from app.api.v1.deps import get_current_user

@router.post("/upload/student", response_model=ImageUploadResponse)
async def upload_image_student(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Student upload endpoint – any logged‑in user can upload images.
    The same validation rules as admin upload apply.
    """
    image = await image_service.save_uploaded_file(file, current_user.id, db)
    return ImageUploadResponse(
        id=image.id,
        filename=image.filename,
        original_filename=image.original_filename,
        file_size=image.file_size,
        mime_type=image.mime_type,
        width=image.width,
        height=image.height,
        created_at=image.created_at,
        url=_build_image_url(str(image.id))
    )


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

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Upload a new image.
    
    - **file**: Image file to upload (JPEG, PNG, GIF, WebP)
    - **Max size**: 5MB
    - **Returns**: Image metadata including URL
    """
    image = await image_service.save_uploaded_file(file, current_user.id, db)
    
    return ImageUploadResponse(
        id=image.id,
        filename=image.filename,
        original_filename=image.original_filename,
        file_size=image.file_size,
        mime_type=image.mime_type,
        width=image.width,
        height=image.height,
        created_at=image.created_at,
        url=_build_image_url(str(image.id))
    )

@router.get("", response_model=ImageListResponse)
async def list_images(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List all uploaded images with pagination.
    
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **search**: Optional search term for filename
    """
    # Validate pagination
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Page size must be between 1 and 100")
    
    images, total = await image_service.list_images(
        db=db,
        page=page,
        page_size=page_size,
        search=search
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return ImageListResponse(
        images=[_image_to_response(img) for img in images],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(
    image_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get image metadata by ID."""
    image = await image_service.get_image_by_id(image_id, db)
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return _image_to_response(image)

@router.delete("/{image_id}")
async def delete_image(
    image_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete an image.
    
    - Only the uploader or an admin can delete an image
    - Deletes both the file and database record
    - Removes all chapter associations
    """
    await image_service.delete_image(
        image_id=image_id,
        user_id=current_user.id,
        db=db,
        is_admin=True  # Admin can delete any image
    )
    
    return {"message": "Image deleted successfully"}

@router.get("/{image_id}/file")
async def serve_image(
    image_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Serve the actual image file.
    
    - This endpoint is public (no authentication required)
    - Used to display images in the frontend
    """
    image = await image_service.get_image_by_id(image_id, db)
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_path = image_service.get_image_file_path(image.filename)
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found on disk")
    
    return FileResponse(
        path=file_path,
        media_type=image.mime_type,
        filename=image.original_filename
    )
