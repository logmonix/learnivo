from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProfileBase(BaseModel):
    display_name: str
    current_grade: int
    avatar_url: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: UUID
    parent_id: UUID
    xp: int
    coins: int

    class Config:
        from_attributes = True
