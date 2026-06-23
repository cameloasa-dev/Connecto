"""
Authentication schemas for Connecto
Primary authentication: SESSION-BASED
Optional fallback: JWT tokens (for future mobile/API use)
"""

import re

from pydantic import BaseModel, EmailStr, Field, field_validator


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
