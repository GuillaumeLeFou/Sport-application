from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

# Charger .env si présent
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    database_url: str = ""

    class Config:
        fields = {
            "database_url": {"env": "DATABASE_URL"},
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
