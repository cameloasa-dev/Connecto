from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories import (
    CircleRepository,
    PostRepository,
    UserRepository,
)
from app.schemas.search import SearchResponse
from app.services import SearchService

router = APIRouter(prefix="/search", tags=["search"])


# --------------------------------------------------
# DEPENDENCY: SearchService
# --------------------------------------------------
def get_search_service(
    db: AsyncSession = Depends(get_db),
) -> SearchService:
    return SearchService(
        user_repo=UserRepository(db),
        circle_repo=CircleRepository(db),
        post_repo=PostRepository(db),
    )


# --------------------------------------------------
# SEARCH ENDPOINT
# --------------------------------------------------
@router.get("", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user_from_session),
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:

    return await service.search(
        current_user=current_user,
        term=q,
        page=page,
    )
