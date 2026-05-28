"""
Dashboard management endpoints
Session-based authentication
"""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Circle, CircleMember, Post, User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=dict)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> dict[str, Any]:
    # 1. USER INFO
    user_info = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }

    # 2. CIRCLES
    circles_result = await db.execute(
        select(Circle, CircleMember.role)
        .join(CircleMember, Circle.id == CircleMember.circle_id)
        .where(CircleMember.user_id == current_user.id)
    )

    circles = []
    circle_ids = []

    for circle, role in circles_result:
        circles.append(
            {
                "id": circle.id,
                "name": circle.name,
                "description": circle.description,
                "role": role,
            }
        )
        circle_ids.append(circle.id)

    # 3. FEED
    feed = []
    if circle_ids:
        posts_result = await db.execute(
            select(Post, User.username, Circle.name)
            .join(User, Post.author_id == User.id)
            .join(Circle, Post.circle_id == Circle.id, isouter=True)
            .where(Post.circle_id.in_(circle_ids))
            .order_by(desc(Post.created_at))
            .limit(20)
        )

        for post, author_name, circle_name in posts_result:
            feed.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "author_id": post.author_id,
                    "author_name": author_name,
                    "circle_id": post.circle_id,
                    "circle_name": circle_name,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at,
                }
            )

    # 4. STATS
    stats = {
        "total_circles": len(circles),
        "total_posts_in_feed": len(feed),
    }

    return {
        "user": user_info,
        "circles": circles,
        "feed": feed,
        "stats": stats,
    }
