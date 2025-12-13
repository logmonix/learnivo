import asyncio
import sys
import os

# Ensure backend in path
sys.path.append('backend')

from app.core.database import AsyncSessionLocal
from app.models.user import User, Profile
from app.core.security import get_password_hash
from sqlalchemy import select

async def seed_user():
    async with AsyncSessionLocal() as db:
        # Check if user exists
        email = "parent@learnivo.com"
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if not user:
            print(f"Creating user {email}...")
            user = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name="Demo Parent",
                role="parent",
                is_active=True,
                is_admin=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            print(f"User {email} already exists.")
            
        # Check if profile exists
        result = await db.execute(select(Profile).where(Profile.parent_id == user.id))
        profile = result.scalars().first()
        
        if not profile:
            print("Creating profile 'Bobby'...")
            profile = Profile(
                parent_id=user.id,
                display_name="Bobby",
                current_grade=4,
                avatar_url="default_avatar.png",
                xp=0,
                coins=0
            )
            db.add(profile)
            await db.commit()
        else:
            print(f"Profile {profile.display_name} already exists.")
            
        print("✅ User seed complete.")
        print("Email: parent@learnivo.com")
        print("Password: password123")
        print(f"Profile: {profile.display_name}")

if __name__ == "__main__":
    asyncio.run(seed_user())
