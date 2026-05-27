"""
Application configuration
Environment variables and settings management
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    # API Configuration
    PROJECT_NAME: str = "Social App API"
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

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # dev
        # "https://connecto.vercel.app",  # production (exemplu)
        # "https://connecto.netlify.app", # production (exemplu)
        # "https://connecto.se",          # production (domeniu propriu)
    ]

    # Environment
    ENVIRONMENT: str = "development"  # "production" on deploy
    FRONTEND_URL: str = "http://localhost:3000"  # used for CSP


# Global settings instance
settings = Settings()
