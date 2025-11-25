import os
import uuid
import shutil
from pathlib import Path
from typing import Optional, BinaryIO
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, or_
from PIL import Image as PILImage

from app.core.config import settings
from app.models.image import Image, ChapterImage
from app.models.user import User

class ImageService:
    """Service for handling image uploads and management."""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR) / "images"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename using UUID while preserving extension."""
        ext = Path(original_filename).suffix.lower()
        return f"{uuid.uuid4()}{ext}"
    
    def _validate_file_type(self, mime_type: str) -> bool:
        """Validate if the file type is allowed."""
        return mime_type in settings.ALLOWED_IMAGE_TYPES
    
    def _validate_file_size(self, file_size: int) -> bool:
        """Validate if the file size is within limits."""
        return file_size <= settings.MAX_FILE_SIZE
    
    def _get_image_dimensions(self, file_path: Path) -> tuple[Optional[int], Optional[int]]:
        """Get image dimensions using PIL."""
        try:
            with PILImage.open(file_path) as img:
                return img.width, img.height
        except Exception:
            return None, None
    
    async def save_uploaded_file(
        self,
        file: UploadFile,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> Image:
        """
        Save an uploaded file to disk and create database record.
        
        Args:
            file: The uploaded file
            user_id: ID of the user uploading the file
            db: Database session
            
        Returns:
            Image: The created image record
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate file type
        if not self._validate_file_type(file.content_type):
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        if not self._validate_file_size(file_size):
            raise HTTPException(
                status_code=400,
                detail=f"File size {file_size} bytes exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Generate unique filename
        unique_filename = self._generate_unique_filename(file.filename)
        file_path = self.upload_dir / unique_filename
        
        # Save file to disk
        try:
            with open(file_path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Get image dimensions
        width, height = self._get_image_dimensions(file_path)
        
        # Create database record
        image = Image(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=f"images/{unique_filename}",
            file_size=file_size,
            mime_type=file.content_type,
            width=width,
            height=height,
            uploaded_by=user_id
        )
        
        db.add(image)
        await db.commit()
        await db.refresh(image)
        
        return image
    
    async def delete_image(
        self,
        image_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession,
        is_admin: bool = False
    ) -> bool:
        """
        Delete an image from disk and database.
        
        Args:
            image_id: ID of the image to delete
            user_id: ID of the user requesting deletion
            db: Database session
            is_admin: Whether the user is an admin (can delete any image)
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            HTTPException: If image not found or user not authorized
        """
        result = await db.execute(select(Image).where(Image.id == image_id))
        image = result.scalars().first()
        
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Check authorization (only uploader or admin can delete)
        if not is_admin and image.uploaded_by != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this image")
        
        # Delete file from disk
        file_path = self.upload_dir / image.filename
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Warning: Failed to delete file {file_path}: {str(e)}")
        
        # Delete from database (cascade will handle chapter_images)
        await db.delete(image)
        await db.commit()
        
        return True
    
    async def get_image_by_id(
        self,
        image_id: uuid.UUID,
        db: AsyncSession
    ) -> Optional[Image]:
        """Get an image by ID."""
        result = await db.execute(select(Image).where(Image.id == image_id))
        return result.scalars().first()
    
    async def list_images(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None
    ) -> tuple[list[Image], int]:
        """
        List images with pagination and optional filtering.
        
        Args:
            db: Database session
            page: Page number (1-indexed)
            page_size: Number of items per page
            search: Optional search term for filename
            user_id: Optional filter by uploader
            
        Returns:
            tuple: (list of images, total count)
        """
        # Build query
        query = select(Image)
        
        # Apply filters
        if search:
            query = query.where(
                or_(
                    Image.original_filename.ilike(f"%{search}%"),
                    Image.filename.ilike(f"%{search}%")
                )
            )
        
        if user_id:
            query = query.where(Image.uploaded_by == user_id)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Image.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # Execute query
        result = await db.execute(query)
        images = result.scalars().all()
        
        return images, total
    
    async def associate_image_with_chapter(
        self,
        chapter_id: uuid.UUID,
        image_id: uuid.UUID,
        caption: Optional[str],
        display_order: int,
        db: AsyncSession
    ) -> ChapterImage:
        """
        Associate an image with a chapter.
        
        Args:
            chapter_id: ID of the chapter
            image_id: ID of the image
            caption: Optional caption for the image
            display_order: Order of the image in the chapter
            db: Database session
            
        Returns:
            ChapterImage: The created association
            
        Raises:
            HTTPException: If image not found
        """
        # Verify image exists
        image = await self.get_image_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Check if association already exists
        existing = await db.execute(
            select(ChapterImage).where(
                ChapterImage.chapter_id == chapter_id,
                ChapterImage.image_id == image_id
            )
        )
        if existing.scalars().first():
            raise HTTPException(status_code=400, detail="Image already associated with this chapter")
        
        # Create association
        chapter_image = ChapterImage(
            chapter_id=chapter_id,
            image_id=image_id,
            caption=caption,
            display_order=display_order
        )
        
        db.add(chapter_image)
        await db.commit()
        await db.refresh(chapter_image)
        
        return chapter_image
    
    async def remove_image_from_chapter(
        self,
        chapter_id: uuid.UUID,
        image_id: uuid.UUID,
        db: AsyncSession
    ) -> bool:
        """
        Remove an image association from a chapter.
        
        Args:
            chapter_id: ID of the chapter
            image_id: ID of the image
            db: Database session
            
        Returns:
            bool: True if removed successfully
            
        Raises:
            HTTPException: If association not found
        """
        result = await db.execute(
            select(ChapterImage).where(
                ChapterImage.chapter_id == chapter_id,
                ChapterImage.image_id == image_id
            )
        )
        chapter_image = result.scalars().first()
        
        if not chapter_image:
            raise HTTPException(status_code=404, detail="Image association not found")
        
        await db.delete(chapter_image)
        await db.commit()
        
        return True
    
    async def get_chapter_images(
        self,
        chapter_id: uuid.UUID,
        db: AsyncSession
    ) -> list[ChapterImage]:
        """
        Get all images associated with a chapter.
        
        Args:
            chapter_id: ID of the chapter
            db: Database session
            
        Returns:
            list[ChapterImage]: List of chapter image associations
        """
        result = await db.execute(
            select(ChapterImage)
            .where(ChapterImage.chapter_id == chapter_id)
            .order_by(ChapterImage.display_order)
        )
        return result.scalars().all()
    
    async def update_image_order(
        self,
        chapter_id: uuid.UUID,
        image_id: uuid.UUID,
        new_order: int,
        db: AsyncSession
    ) -> ChapterImage:
        """
        Update the display order of an image in a chapter.
        
        Args:
            chapter_id: ID of the chapter
            image_id: ID of the image
            new_order: New display order
            db: Database session
            
        Returns:
            ChapterImage: Updated association
            
        Raises:
            HTTPException: If association not found
        """
        result = await db.execute(
            select(ChapterImage).where(
                ChapterImage.chapter_id == chapter_id,
                ChapterImage.image_id == image_id
            )
        )
        chapter_image = result.scalars().first()
        
        if not chapter_image:
            raise HTTPException(status_code=404, detail="Image association not found")
        
        chapter_image.display_order = new_order
        await db.commit()
        await db.refresh(chapter_image)
        
        return chapter_image
    
    def get_image_file_path(self, filename: str) -> Path:
        """Get the full file path for an image."""
        return self.upload_dir / filename

# Create singleton instance
image_service = ImageService()
