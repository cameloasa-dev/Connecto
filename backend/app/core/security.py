"""
Security utilities for Connecto
Primary authentication: SESSION-BASED
Optional fallback: JWT tokens (for future mobile/API use)
"""

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import settings

# ======================================================
# PASSWORD HASHING (Argon2)
# ======================================================

pwd_context = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its Argon2 hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ======================================================
# SESSION TOKENS (DEFAULT AUTH METHOD)
# ======================================================

def create_session_token() -> str:
    """
    Create a secure random session token (64 hex chars).
    Used for session-based authentication.
    """
    return secrets.token_hex(32)


def create_session_expiry(hours: int = 24) -> datetime:
    """
    Create expiration datetime for session tokens.
    Default: 24 hours.
    """
    return datetime.now(UTC) + timedelta(hours=hours)


# ======================================================
# JWT TOKENS (OPTIONAL / FALLBACK)
# ======================================================

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.
    Used only for optional JWT-based authentication.
    """
    to_encode = data.copy()

    expire = (
        datetime.now(UTC) + expires_delta
        if expires_delta
        else datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> Any:
    """
    Decode and verify a JWT token.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
