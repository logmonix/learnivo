from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Learnivo"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://learnivo:learnivo_secret@localhost:5432/learnivo_db"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_TO_A_SECURE_SECRET_KEY_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Keys (Optional for now)
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # File Upload Settings
    UPLOAD_DIR: str = "backend/uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_IMAGE_TYPES: set = {
        "image/jpeg",
        "image/jpg", 
        "image/png",
        "image/gif",
        "image/webp"
    }

    class Config:
        env_file = ".env"

settings = Settings()
