from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories import (
    CircleRepository,
    PostRepository,
    UserRepository,
)
from app.services import (
    PostService,
    SearchService,
)

router = APIRouter(prefix="/search", tags=["search"])


# --------------------------------------------------
# DEPENDENCY: SearchService
# --------------------------------------------------
def get_search_service(
    db: AsyncSession = Depends(get_db),
) -> SearchService:
    post_repo = PostRepository(db)
    user_repo = UserRepository(db)
    circle_repo = CircleRepository(db)
    post_service = PostService(post_repo, circle_repo, user_repo)

    return SearchService(
        post_repo=post_repo,
        user_repo=user_repo,
        circle_repo=circle_repo,
        post_service=post_service,
    )


# --------------------------------------------------
# SEARCH ENDPOINT
# --------------------------------------------------
@router.get("", response_model=dict)
async def search(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user_from_session),
    service: SearchService = Depends(get_search_service),
) -> dict:
    return await service.search(
        current_user=current_user,
        term=q,
        page=page,
    )
