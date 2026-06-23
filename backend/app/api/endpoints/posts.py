"""
Post management endpoints
Clean, organized, session-based authentication
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.posts.comments import CommentCreate
from app.schemas.posts.comments import CommentResponse
from app.schemas.posts.likes import LikeResponse
from app.schemas.posts.requests import PostCreate
from app.schemas.posts.responses import PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


def get_post_service(
    db: AsyncSession = Depends(get_db),
) -> PostService:
    return PostService(
        post_repo=PostRepository(db),
        circle_repo=CircleRepository(db),
        user_repo=UserRepository(db),
    )


# ======================================================
# CREATE POST
# ======================================================
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> PostResponse:
    return await service.create_post(post_data, current_user)


# ======================================================
# UPDATE POST
# ======================================================
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostCreate,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> PostResponse:
    return await service.update_post(post_id, post_data, current_user)


# ======================================================
# DELETE POST
# ======================================================
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> None:
    await service.delete_post(post_id, current_user)


# ======================================================
# GET POST BY ID
# ======================================================
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> PostResponse:
    return await service.get_post(post_id, current_user)


# ======================================================
# GET POSTS FROM A CIRCLE
# ======================================================
@router.get("/circle/{circle_id}", response_model=list[PostResponse])
async def get_circle_posts(
    circle_id: int,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> list[PostResponse]:
    return await service.get_circle_posts(circle_id, current_user, limit, offset)


# ======================================================
# LIKE / UNLIKE POST
# ======================================================
@router.post("/{post_id}/like", response_model=LikeResponse)
async def toggle_like(
    post_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> LikeResponse:
    return await service.toggle_like(post_id, current_user)


# ======================================================
# ADD COMMENT
# ======================================================
@router.post("/{post_id}/comments", response_model=CommentResponse)
async def add_comment(
    post_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> CommentResponse:
    return await service.add_comment(post_id, data, current_user)


# ======================================================
# DELETE COMMENT
# ======================================================
@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: PostService = Depends(get_post_service),
) -> None:
    await service.delete_comment(comment_id, current_user)
