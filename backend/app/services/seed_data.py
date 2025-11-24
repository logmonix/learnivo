"""Seed initial badges and avatar items"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.gamification import Badge, AvatarItem

async def seed_badges(db: AsyncSession):
    """Create initial badge achievements."""
    badges = [
        Badge(
            name="First Steps",
            description="Complete your first lesson",
            icon="🌟",
            requirement_type="lessons_completed",
            requirement_value=1
        ),
        Badge(
            name="Quick Learner",
            description="Complete 10 lessons",
            icon="⚡",
            requirement_type="lessons_completed",
            requirement_value=10
        ),
        Badge(
            name="Math Whiz",
            description="Earn 100 XP",
            icon="🧮",
            requirement_type="xp_total",
            requirement_value=100
        ),
        Badge(
            name="Dedicated Student",
            description="Earn 500 XP",
            icon="🏆",
            requirement_type="xp_total",
            requirement_value=500
        ),
        Badge(
            name="Streak Master",
            description="Learn for 7 days in a row",
            icon="🔥",
            requirement_type="streak_days",
            requirement_value=7
        ),
    ]
    
    for badge in badges:
        db.add(badge)
    
    await db.commit()

async def seed_avatar_items(db: AsyncSession):
    """Create initial avatar shop items."""
    items = [
        # Hats
        AvatarItem(name="Wizard Hat", category="hat", icon="🧙", cost=50),
        AvatarItem(name="Crown", category="hat", icon="👑", cost=100),
        AvatarItem(name="Graduation Cap", category="hat", icon="🎓", cost=75),
        AvatarItem(name="Party Hat", category="hat", icon="🎉", cost=30),
        
        # Accessories
        AvatarItem(name="Sunglasses", category="accessory", icon="😎", cost=40),
        AvatarItem(name="Star Badge", category="accessory", icon="⭐", cost=60),
        AvatarItem(name="Medal", category="accessory", icon="🏅", cost=80),
        
        # Backgrounds
        AvatarItem(name="Rainbow", category="background", icon="🌈", cost=100),
        AvatarItem(name="Space", category="background", icon="🌌", cost=120),
        AvatarItem(name="Forest", category="background", icon="🌲", cost=90),
    ]
    
    for item in items:
        db.add(item)
    
    await db.commit()
