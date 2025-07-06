from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl



class Settings(BaseSettings):
    JOB_URL: Optional[AnyHttpUrl] = None
    SCRAPE_INTERVAL_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./jobs.db"
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"


settings = Settings()