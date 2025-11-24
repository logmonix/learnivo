"""Initialize database with seed data"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.seed_data import seed_badges, seed_avatar_items

router = APIRouter()

@router.post("/seed")
async def seed_database(db: AsyncSession = Depends(get_db)):
    """Seed the database with initial badges and avatar items."""
    try:
        await seed_badges(db)
        await seed_avatar_items(db)
        return {"message": "Database seeded successfully"}
    except Exception as e:
        return {"error": str(e)}
