
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


# ======================================================
# DEPENDENCY
# ======================================================
def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db), CircleRepository(db))


# ======================================================
# ME (current user)
# ======================================================
@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user_from_session),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


# ======================================================
# GET ALL USERS (pagination)
# ======================================================
@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_from_session),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await service.list_users(current_user, skip, limit)
