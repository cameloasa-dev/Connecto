from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Circle, Post, User

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=dict)
async def global_search(
    q: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> dict:
    # Empty query → empty results
    if not q.strip():
        return {"users": [], "circles": [], "posts": []}

    # Search users
    users_result = await db.execute(select(User).where(User.username.ilike(f"%{q}%")).limit(10))
    users = users_result.scalars().all()

    # Search circles
    circles_result = await db.execute(select(Circle).where(Circle.name.ilike(f"%{q}%")).limit(10))
    circles = circles_result.scalars().all()

    # Search posts
    posts_result = await db.execute(select(Post).where(Post.content.ilike(f"%{q}%")).limit(10))
    posts = posts_result.scalars().all()

    # Build response
    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            for user in users
        ],
        "circles": [
            {
                "id": circle.id,
                "name": circle.name,
                "description": circle.description,
            }
            for circle in circles
        ],
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author_id": post.author_id,
                "circle_id": post.circle_id,
                "created_at": post.created_at,
            }
            for post in posts
        ],
    }
