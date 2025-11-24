import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    icon = Column(String)  # Emoji or icon name
    requirement_type = Column(String)  # 'xp_total', 'lessons_completed', 'streak_days'
    requirement_value = Column(Integer)
    
class ProfileBadge(Base):
    __tablename__ = "profile_badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

class AvatarItem(Base):
    __tablename__ = "avatar_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String)  # 'hat', 'outfit', 'accessory', 'background'
    icon = Column(String)  # Emoji representation
    cost = Column(Integer, default=0)  # Coin cost
    is_premium = Column(Boolean, default=False)

class ProfileAvatar(Base):
    __tablename__ = "profile_avatars"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("avatar_items.id"), nullable=False)
    is_equipped = Column(Boolean, default=False)
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())
