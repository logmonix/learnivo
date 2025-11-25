# Import all models here so Alembic can find them
from app.core.database import Base
from app.models.user import User, Profile
from app.models.curriculum import Subject, Chapter, ContentBlock
from app.models.progress import StudentProgress
from app.models.gamification import Badge, ProfileBadge, AvatarItem, ProfileAvatar
from app.models.image import Image, ChapterImage
