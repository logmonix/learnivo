from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User, Profile
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProfileResponse])
async def get_my_profiles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all profiles (kids) for the logged-in parent."""
    result = await db.execute(select(Profile).where(Profile.parent_id == current_user.id))
    return result.scalars().all()

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile_in: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new child profile."""
    new_profile = Profile(
        parent_id=current_user.id,
        display_name=profile_in.display_name,
        current_grade=profile_in.current_grade,
        avatar_url=profile_in.avatar_url or "default_avatar.png"
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile
