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
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)
    is_private: bool = False


class CircleUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)
    is_private: bool | None = None
