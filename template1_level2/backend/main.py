from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import engine, Base
from routes import chat, users

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} API is running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
