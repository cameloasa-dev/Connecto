"""
Async SQLite database configuration and session management.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# -----------------------------
# DATABASE CONFIG (SQLite)
# -----------------------------
DATABASE_URL = settings.DATABASE_URL  #  sqlite+aiosqlite:///./dev.db

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # set to False in production
)


# Base class for all ORM models
class Base(DeclarativeBase):
    pass


# Async session factory
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# -----------------------------
# Dependency for FastAPI
# -----------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an async database session for request handlers.
    """
    async with SessionLocal() as session:
        yield session
