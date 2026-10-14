from typing import Any

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import SessionResponse, UserCreate, UserLogin
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db), CircleRepository(db))


# =========================================================
# REGISTER
# =========================================================
@router.post("/register", response_model=SessionResponse, status_code=201)
async def register(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> SessionResponse:
    return await service.register(user_data)


# =========================================================
# LOGIN
# =========================================================
@router.post("/login", response_model=SessionResponse)
async def login(
    credentials: UserLogin,
    request: Request,
    response: Response,
    service: UserService = Depends(get_user_service),
) -> SessionResponse:
    return await service.login(credentials, request, response)


# =========================================================
# LOGOUT
# =========================================================
@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    return await service.logout(request, response)
