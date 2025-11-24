from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ChapterBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 0

class SubjectBase(BaseModel):
    name: str
    grade_level: int
    icon_name: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: UUID
    chapters: List[ChapterBase] = []

    class Config:
        from_attributes = True

class GenerateCurriculumRequest(BaseModel):
    grade_level: int
    subject_name: str
