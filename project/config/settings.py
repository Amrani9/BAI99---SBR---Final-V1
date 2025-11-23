"""Application settings and configuration helpers."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def _sqlite_url(db_path: Path) -> str:
    return f"sqlite:///{db_path.as_posix()}"


class Settings:
    """Centralized application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "Smart School Bus Routing System")
        self.debug: bool = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
        self.secret_key: str = os.getenv("SECRET_KEY", "change-me")
        self.database_url: Optional[str] = os.getenv("DATABASE_URL")
        self.google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return _sqlite_url(DATABASE_DIR / "smartbus.db")


@lru_cache()
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance."""

    return Settings()
