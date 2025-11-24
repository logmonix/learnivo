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
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Learnivo API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
