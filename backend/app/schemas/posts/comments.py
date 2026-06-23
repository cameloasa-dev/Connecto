"""
Social feature schemas for Connecto
Comments
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    username: str | None
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
