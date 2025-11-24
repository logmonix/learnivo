from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class AdminStats(BaseModel):
    total_subjects: int
    total_chapters: int
    total_students: int
    total_lessons_completed: int

class BulkGenerateRequest(BaseModel):
    grade_level: int
    subject_names: List[str]

class ContentBlockUpdate(BaseModel):
    content_data: dict
