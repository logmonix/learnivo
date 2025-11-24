import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class StudentProgress(Base):
    __tablename__ = "student_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    
    # Status: 'not_started', 'in_progress', 'completed'
    status = Column(String, default='not_started')
    
    # Quiz results
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    
    # XP earned from this chapter
    xp_earned = Column(Integer, default=0)
    
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
