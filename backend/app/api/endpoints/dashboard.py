"""
Dashboard management endpoints
Session-based authentication
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.dashboard_service import DashboardService
from app.services.post_service import PostService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# --------------------------------------------------
# DEPENDENCY: DashboardService
# --------------------------------------------------
def get_dashboard_service(
    db: AsyncSession = Depends(get_db),
) -> DashboardService:
    circle_repo = CircleRepository(db)
    post_repo = PostRepository(db)
    user_repo = UserRepository(db)
    post_service = PostService(post_repo, circle_repo, user_repo)

    return DashboardService(
        circle_repo=circle_repo,
        post_repo=post_repo,
        user_repo=user_repo,
        post_service=post_service,
    )


# --------------------------------------------------
# GET DASHBOARD
# --------------------------------------------------
@router.get("", response_model=dict)
async def get_dashboard(
    current_user: User = Depends(get_current_user_from_session),
    service: DashboardService = Depends(get_dashboard_service),
) -> dict:
    return await service.get_dashboard(current_user)
