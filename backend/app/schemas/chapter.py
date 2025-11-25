from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ChapterCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 1

class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
