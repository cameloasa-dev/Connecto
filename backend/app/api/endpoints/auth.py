from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import SessionResponse, UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


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
# CURRENT USER
# =========================================================
async def get_current_user_from_session(
    request: Request,
    service: UserService = Depends(get_user_service),
) -> User:
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return await service.get_current_user_from_session_token(session_token)


# =========================================================
# Me
# =========================================================
@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user_from_session),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


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
