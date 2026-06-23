"""
Post like management endpoints
Clean, organized, session-based authentication
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Post, PostLike, User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/{post_id}/like", status_code=204)
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> None:

    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")

    exists = await db.scalar(
        select(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id,
        )
    )

    if exists:
        raise HTTPException(400, "Already liked")

    db.add(PostLike(post_id=post_id, user_id=current_user.id))
    await db.commit()


@router.delete("/{post_id}/like", status_code=204)
async def unlike_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> None:

    like = await db.scalar(
        select(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id,
        )
    )

    if not like:
        raise HTTPException(400, detail="You have not liked this post")

    await db.delete(like)
    await db.commit()
