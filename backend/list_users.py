import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import User

async def list_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"Email: {user.email}, Role: {user.role}, Is Admin: {user.is_admin}")

if __name__ == "__main__":
    asyncio.run(list_users())
