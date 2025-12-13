import sys
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import User

async def promote_user(email: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user:
            user.is_admin = True
            user.role = "admin"
            await session.commit()
            print(f"Successfully promoted user {email} to admin!")
        else:
            print(f"User with email {email} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_admin.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    asyncio.run(promote_user(email))
