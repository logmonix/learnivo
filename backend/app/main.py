from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Learnivo API",
    description="AI-Powered Learning Platform Backend",
    version="0.1.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vue Frontend
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import auth, profiles, curriculum, learning, admin, gamification, seed, dev

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["profiles"])
app.include_router(curriculum.router, prefix="/api/v1/curriculum", tags=["curriculum"])
app.include_router(learning.router, prefix="/api/v1/learning", tags=["learning"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(gamification.router, prefix="/api/v1/gamification", tags=["gamification"])
app.include_router(seed.router, prefix="/api/v1/seed", tags=["seed"])
app.include_router(dev.router, prefix="/api/v1/dev", tags=["dev"])

@app.get("/")
async def root():
    return {"message": "Welcome to Learnivo API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
