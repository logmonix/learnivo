import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Image(Base):
    __tablename__ = "images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False, unique=True)  # Unique storage filename
    original_filename = Column(String, nullable=False)  # Original upload filename
    file_path = Column(String, nullable=False)  # Relative path from upload directory
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String, nullable=False)  # e.g., "image/jpeg"
    width = Column(Integer, nullable=True)  # Image width in pixels
    height = Column(Integer, nullable=True)  # Image height in pixels
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    uploader = relationship("User", backref="uploaded_images")
    chapter_associations = relationship("ChapterImage", back_populates="image", cascade="all, delete-orphan")

class ChapterImage(Base):
    __tablename__ = "chapter_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    display_order = Column(Integer, default=0)  # Order of images in chapter
    caption = Column(Text, nullable=True)  # Optional caption for the image
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chapter = relationship("Chapter", backref="chapter_images")
    image = relationship("Image", back_populates="chapter_associations")
