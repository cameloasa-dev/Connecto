"""
Authentication schemas for Connecto
Primary authentication: SESSION-BASED
Optional fallback: JWT tokens (for future mobile/API use)
"""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ---------------------------------------------------------
# USER REGISTRATION
# ---------------------------------------------------------
class UserCreate(BaseModel):
    """
    Schema for user registration (frontend RegisterPage)
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=50)
    full_name: str | None = Field(None, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Password complexity rules"""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


# ---------------------------------------------------------
# USER LOGIN (SESSION-BASED)
# ---------------------------------------------------------
class UserLogin(BaseModel):
    """
    Login schema (frontend uses USERNAME, not email)
    """
    username: str
    password: str


# ---------------------------------------------------------
# USER RESPONSE (SAFE)
# ---------------------------------------------------------
class UserResponse(BaseModel):
    """
    Public user data returned to frontend
    """
    id: int
    username: str
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# SESSION-BASED AUTH (DEFAULT)
# ---------------------------------------------------------
class SessionResponse(BaseModel):
    """
    Response for session-based authentication
    """
    success: bool = True
    username: str
    session_token: str | None = Field(None, description="Session token stored in HTTP-only cookie")
    user: UserResponse | None = None


# ---------------------------------------------------------
# JWT (OPTIONAL / FUTURE USE)
# ---------------------------------------------------------
class Token(BaseModel):
    """
    JWT token response (optional)
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Decoded JWT payload (internal use)
    """
    username: str | None = None
