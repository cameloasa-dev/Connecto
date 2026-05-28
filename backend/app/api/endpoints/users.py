"""
User management endpoints
Session-based authentication
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import CircleMember, User
from app.schemas import UserResponse, UserSearchResponse

router = APIRouter(prefix="/users", tags=["users"])


# ======================================================
# GET ALL USERS (with pagination)
# ======================================================
@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> list[UserResponse]:
    """
    Get all users except the current user.
    Supports pagination.
    """

    result = await db.execute(
        select(User).where(User.id != current_user.id).offset(skip).limit(limit)
    )
    users = result.scalars().all()

    return [UserResponse.model_validate(user) for user in users]


# ======================================================
# SEARCH USERS (for adding to a circle)
# ======================================================
@router.get("/search", response_model=list[UserSearchResponse])
async def search_users(
    query: str,
    circle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> list[UserSearchResponse]:
    """
    Search users by username (case-insensitive).
    Only circle owners or moderators can search.
    Excludes:
    - current user
    - users already in the circle
    """

    # 1. Permission check
    permission = await db.execute(
        select(CircleMember).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id,
            CircleMember.role.in_(["owner", "moderator"]),
        )
    )

    if not permission.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only circle owners and moderators can search for new members",
        )

    # 2. Empty query → empty list
    if not query.strip():
        return []

    # 3. Get existing member IDs
    existing_members = await db.execute(
        select(CircleMember.user_id).where(CircleMember.circle_id == circle_id)
    )
    existing_ids = [row[0] for row in existing_members.fetchall()]

    # 4. Search users
    stmt = (
        select(User)
        .where(
            User.id != current_user.id,
            User.username.ilike(f"%{query}%"),
        )
        .limit(20)
    )

    if existing_ids:
        stmt = stmt.where(User.id.not_in(existing_ids))

    result = await db.execute(stmt)
    users = result.scalars().all()

    # 5. Build response
    return [
        UserSearchResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_already_member=False,
        )
        for user in users
    ]
