"""
Circle management endpoints
Session-based authentication
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.schemas.circles.requests import CircleCreate, CircleUpdate
from app.schemas.circles.responses import CircleResponse
from app.services.circle_service import CircleService

router = APIRouter(prefix="/circles", tags=["circles"])


def get_circle_service(db: AsyncSession = Depends(get_db)) -> CircleService:
    return CircleService(CircleRepository(db))


# ======================================================
# GET MY CIRCLES
# ======================================================
@router.get("/my", response_model=list[CircleResponse])
async def get_my_circles(
    current_user: User = Depends(get_current_user_from_session),
    service: CircleService = Depends(get_circle_service),
) -> list[CircleResponse]:
    return await service.get_my_circles(current_user)


# ======================================================
# CREATE CIRCLE
# ======================================================
@router.post("/", response_model=CircleResponse, status_code=status.HTTP_201_CREATED)
async def create_circle(
    circle_data: CircleCreate,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleService = Depends(get_circle_service),
) -> CircleResponse:
    return await service.create_circle(circle_data, current_user)


# ======================================================
# GET CIRCLE BY ID
# ======================================================
@router.get("/{circle_id}", response_model=CircleResponse)
async def get_circle(
    circle_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleService = Depends(get_circle_service),
) -> CircleResponse:
    return await service.get_circle(circle_id, current_user)


# ======================================================
# UPDATE CIRCLE
# ======================================================
@router.patch("/{circle_id}", response_model=CircleResponse)
async def update_circle(
    circle_id: int,
    circle_data: CircleUpdate,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleService = Depends(get_circle_service),
) -> CircleResponse:
    return await service.update_circle(circle_id, circle_data, current_user)


# ======================================================
# DELETE CIRCLE
# ======================================================
@router.delete("/{circle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circle(
    circle_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleService = Depends(get_circle_service),
) -> None:
    await service.delete_circle(circle_id, current_user)
