from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Hackathon Template"
    gemini_api_key: str
    database_url: str = "sqlite:///./app.db"
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
