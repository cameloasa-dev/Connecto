from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Comment, Post, User
from app.schemas.posts.comments import CommentResponse

router = APIRouter(prefix="/posts", tags=["posts"])


# ======================================================
# HELPERS
# ======================================================


def build_comment_response(comment: Comment, username: str) -> CommentResponse:
    return CommentResponse(
        id=comment.id,
        post_id=comment.post_id,
        user_id=comment.user_id,
        username=username,
        content=comment.content,
        created_at=comment.created_at,
    )


# ======================================================
# CREATE COMMENT
# ======================================================


@router.post("/{post_id}/comments", response_model=CommentResponse)
async def add_comment(
    post_id: int,
    content: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> CommentResponse:

    # Ensure post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create comment
    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=content,
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return build_comment_response(comment, current_user.username)
