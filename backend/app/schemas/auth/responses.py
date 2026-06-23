"""
Authentication schemas for Connecto
Primary authentication: SESSION-BASED
Optional fallback: JWT tokens (for future mobile/API use)
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    username: str | None = None
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
