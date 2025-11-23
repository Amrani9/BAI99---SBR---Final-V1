"""Database configuration and session management."""
from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import get_settings

Settings = get_settings()

# Configure SQLAlchemy
engine = create_engine(
    Settings.sqlalchemy_database_uri,
    connect_args={"check_same_thread": False} if Settings.sqlalchemy_database_uri.startswith("sqlite") else {},
    future=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_engine():
    """Return the configured SQLAlchemy engine."""

    return engine


def get_session() -> Generator:
    """Yield a database session and ensure closure."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
