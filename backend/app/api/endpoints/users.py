from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse
from app.schemas.circles import UserSearchResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


# ======================================================
# GET ME
# ======================================================
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user_from_session)) -> UserResponse:
    return UserResponse.model_validate(current_user)


# ======================================================
# GET ALL USERS (with pagination)
# ======================================================
@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_from_session),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await service.list_users(current_user, skip, limit)


# ======================================================
# SEARCH USERS (for adding to a circle)
# ======================================================
@router.get("/search", response_model=list[UserSearchResponse])
async def search_users(
    query: str,
    circle_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: UserService = Depends(get_user_service),
) -> list[UserSearchResponse]:
    return await service.search_users_for_circle(
        current_user=current_user,
        circle_id=circle_id,
        query=query,
    )


# ======================================================
# GET USER PROFILE (for ProfilePage)
# ======================================================
@router.get("/{user_id}/profile")
async def get_user_profile(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    return await service.get_profile(user_id)
