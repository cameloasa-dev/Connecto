"""
Social feature schemas for Connecto
Posts Request
"""

from pydantic import BaseModel, Field

# ======================================================
# POST  REQUEST SCHEMAS
# ======================================================


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=250)


class PostCreate(PostBase):
    circle_id: int | None = None


class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1, max_length=250)
    circle_id: int | None = None
