"""
Social feature schemas for Connecto
Posts Responses
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .comments import CommentResponse

# ======================================================
# POST RESPONSE SCHEMAS
# ======================================================


class PostResponse(BaseModel):
    id: int
    title: str
    content: str

    author_id: int
    author_name: str | None = None
    author_badge: str | None = None

    circle_id: int | None = None
    circle_name: str | None = None

    likes_count: int = 0
    comments_count: int = 0
    liked_by_me: bool = False

    can_edit: bool = False
    can_delete: bool = False

    comments: list[CommentResponse] | None = None

    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
