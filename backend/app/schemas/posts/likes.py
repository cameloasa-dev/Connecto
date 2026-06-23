"""
Social feature schemas for Connecto
Likes Response, toogle
"""

from pydantic import BaseModel


class LikeResponse(BaseModel):
    post_id: int
    user_id: int
    liked: bool


class LikeToggleResponse(BaseModel):
    success: bool
    liked: bool
    likes_count: int
