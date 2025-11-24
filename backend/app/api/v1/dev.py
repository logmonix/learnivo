"""Make a user an admin"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/make-admin/{email}")
async def make_user_admin(email: str, db: AsyncSession = Depends(get_db)):
    """Make a user an admin (development only - remove in production)."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = True
    await db.commit()
    
    return {"message": f"User {email} is now an admin"}
