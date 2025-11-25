from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# Image Schemas
class ImageUploadResponse(BaseModel):
    id: UUID
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime
    url: str  # URL to access the image
    
    class Config:
        from_attributes = True

class ImageResponse(BaseModel):
    id: UUID
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    width: Optional[int] = None
    height: Optional[int] = None
    uploaded_by: UUID
    created_at: datetime
    updated_at: datetime
    url: str  # URL to access the image
    
    class Config:
        from_attributes = True

class ImageListResponse(BaseModel):
    images: list[ImageResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# Chapter-Image Association Schemas
class ChapterImageCreate(BaseModel):
    image_id: UUID
    caption: Optional[str] = None
    display_order: Optional[int] = 0

class ChapterImageUpdate(BaseModel):
    caption: Optional[str] = None
    display_order: Optional[int] = None

class ChapterImageResponse(BaseModel):
    id: UUID
    chapter_id: UUID
    image_id: UUID
    display_order: int
    caption: Optional[str] = None
    created_at: datetime
    image: ImageResponse  # Nested image data
    
    class Config:
        from_attributes = True

class ChapterImageListResponse(BaseModel):
    chapter_images: list[ChapterImageResponse]
    total: int
