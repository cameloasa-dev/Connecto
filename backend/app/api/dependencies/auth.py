from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db), CircleRepository(db))


async def get_current_user_from_session(
    request: Request,
    service: UserService = Depends(get_user_service),
) -> User:
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return await service.get_current_user_from_session_token(session_token)
