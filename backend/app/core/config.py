"""
Application configuration
Environment variables and settings management
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENVIRONMENT", "development")


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}",  # Load from .env.development by default
        env_ignore_empty=True,
        extra="ignore",
    )

    # API Configuration
    PROJECT_NAME: str = "Connecto API"
    VERSION: str = "0.1.0"

    # Database (SQLite by default)
    # Example for local dev:
    #   sqlite+aiosqlite:///./dev.db
    #
    # Example for production (commented):
    #   postgresql+asyncpg://user:password@host/dbname
    DATABASE_URL: str = ""

    # Security - JWT Tokens
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Security - Sessions
    SESSION_SECRET_KEY: str = ""
    SESSION_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    SESSION_EXPIRE_HOURS: int = 24

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # dev
        # "https://connecto.vercel.app",  # production (exemple)
        # "https://connecto.netlify.app", # production (exemple)
        # "https://connecto.se",          # production (my domain, but not live yet)
    ]

    # Environment
    ENVIRONMENT: str = "development"  # "production" on deploy
    FRONTEND_URL: str = "http://localhost:3000"  # used for CSP

    # Test user data (for seeding)
    TEST_USER_EMAIL: str = ""
    TEST_USER_USERNAME: str = ""
    TEST_USER_PASSWORD: str = ""

    TEST_USER2_EMAIL: str = ""
    TEST_USER2_USERNAME: str = ""
    TEST_USER2_PASSWORD: str = ""


# Global settings instance
settings = Settings()
