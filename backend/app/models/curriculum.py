import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False) # e.g., "Mathematics"
    grade_level = Column(Integer, nullable=False) # e.g., 5
    description = Column(Text, nullable=True)
    icon_name = Column(String, nullable=True) # For UI icon mapping
    
    chapters = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)
    title = Column(String, nullable=False) # e.g., "Fractions and Decimals"
    order_index = Column(Integer, default=0) # To order chapters 1, 2, 3...
    description = Column(Text, nullable=True)
    
    subject = relationship("Subject", back_populates="chapters")
    content_blocks = relationship("ContentBlock", back_populates="chapter")

class ContentBlock(Base):
    __tablename__ = "content_blocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    
    # Type: 'lesson', 'quiz', 'video_script', 'flashcard'
    block_type = Column(String, nullable=False) 
    
    # The actual AI generated content. 
    # For a lesson: {"markdown": "..."}
    # For a quiz: {"questions": [...]}
    content_data = Column(JSON, nullable=False)
    
    ai_model_used = Column(String, nullable=True) # e.g., "gpt-4-turbo"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chapter = relationship("Chapter", back_populates="content_blocks")
