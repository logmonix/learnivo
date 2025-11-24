from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.gamification import Badge, ProfileBadge, AvatarItem, ProfileAvatar
from app.models.user import Profile
from app.models.progress import StudentProgress
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/badges")
async def get_all_badges(db: AsyncSession = Depends(get_db)):
    """Get all available badges."""
    result = await db.execute(select(Badge))
    return result.scalars().all()

@router.get("/badges/profile/{profile_id}")
async def get_profile_badges(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get badges earned by a profile."""
    result = await db.execute(
        select(ProfileBadge).where(ProfileBadge.profile_id == profile_id)
    )
    earned_badges = result.scalars().all()
    
    # Get all badges with earned status
    result = await db.execute(select(Badge))
    all_badges = result.scalars().all()
    
    earned_ids = {str(pb.badge_id) for pb in earned_badges}
    
    return [
        {
            **badge.__dict__,
            "earned": str(badge.id) in earned_ids
        }
        for badge in all_badges
    ]

@router.post("/badges/check/{profile_id}")
async def check_and_award_badges(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Check if profile has earned any new badges."""
    
    # Get profile stats
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Count completed lessons
    result = await db.execute(
        select(StudentProgress)
        .where(StudentProgress.profile_id == profile_id)
        .where(StudentProgress.status == 'completed')
    )
    completed_lessons = len(result.scalars().all())
    
    # Get all badges
    result = await db.execute(select(Badge))
    all_badges = result.scalars().all()
    
    # Get already earned badges
    result = await db.execute(
        select(ProfileBadge).where(ProfileBadge.profile_id == profile_id)
    )
    earned = {str(pb.badge_id) for pb in result.scalars().all()}
    
    newly_earned = []
    
    for badge in all_badges:
        if str(badge.id) in earned:
            continue
            
        should_award = False
        
        if badge.requirement_type == 'xp_total' and profile.xp >= badge.requirement_value:
            should_award = True
        elif badge.requirement_type == 'lessons_completed' and completed_lessons >= badge.requirement_value:
            should_award = True
        
        if should_award:
            new_badge = ProfileBadge(profile_id=profile_id, badge_id=badge.id)
            db.add(new_badge)
            newly_earned.append(badge)
    
    await db.commit()
    
    return {"newly_earned": newly_earned, "count": len(newly_earned)}

@router.get("/shop/items")
async def get_shop_items(db: AsyncSession = Depends(get_db)):
    """Get all avatar items available in shop."""
    result = await db.execute(select(AvatarItem))
    return result.scalars().all()

@router.get("/shop/profile/{profile_id}")
async def get_profile_items(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get items owned by a profile."""
    result = await db.execute(
        select(ProfileAvatar).where(ProfileAvatar.profile_id == profile_id)
    )
    return result.scalars().all()

@router.post("/shop/purchase/{profile_id}/{item_id}")
async def purchase_item(
    profile_id: str,
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Purchase an avatar item."""
    
    # Get profile
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get item
    result = await db.execute(select(AvatarItem).where(AvatarItem.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if already owned
    result = await db.execute(
        select(ProfileAvatar)
        .where(ProfileAvatar.profile_id == profile_id)
        .where(ProfileAvatar.item_id == item_id)
    )
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Item already owned")
    
    # Check coins
    if profile.coins < item.cost:
        raise HTTPException(status_code=400, detail="Insufficient coins")
    
    # Deduct coins
    profile.coins -= item.cost
    
    # Add item
    new_item = ProfileAvatar(profile_id=profile_id, item_id=item_id)
    db.add(new_item)
    
    await db.commit()
    
    return {"message": "Purchase successful", "remaining_coins": profile.coins}
