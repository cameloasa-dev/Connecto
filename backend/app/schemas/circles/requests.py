"""
Social feature schemas for Connecto
Circles Requests
"""

from pydantic import BaseModel, Field

# ======================================================
# CIRCLE  REQUESTS SCHEMAS
# ======================================================


class CircleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)


class CircleCreate(CircleBase):
    pass


class UpdateCircleRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., max_length=255)


class CirclePrivacyUpdate(BaseModel):
    is_private: bool
