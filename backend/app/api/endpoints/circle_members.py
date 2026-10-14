"""
Circle member management endpoints
Session-based authentication
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse
from app.schemas.circles.members import (
    AddMemberRequest,
    CircleMemberActionResponse,
    UpdateRoleRequest,
)
from app.services.circle_member_service import CircleMemberService

router = APIRouter(prefix="/circles", tags=["circle-members"])


def get_circle_member_service(
    db: AsyncSession = Depends(get_db),
) -> CircleMemberService:
    return CircleMemberService(
        circle_repo=CircleRepository(db),
        user_repo=UserRepository(db),
    )


# ======================================================
# 1. ADD MEMBER
# ======================================================
@router.post("/{circle_id}/members", status_code=201, response_model=CircleMemberActionResponse)
async def add_member(
    circle_id: int,
    request: AddMemberRequest,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleMemberService = Depends(get_circle_member_service),
) -> CircleMemberActionResponse:
    return await service.add_member(circle_id, request, current_user)


# ======================================================
# 2. REMOVE MEMBER
# ======================================================
@router.delete("/{circle_id}/members/{user_id}", response_model=CircleMemberActionResponse)
async def remove_member(
    circle_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleMemberService = Depends(get_circle_member_service),
) -> CircleMemberActionResponse:
    return await service.remove_member(circle_id, user_id, current_user)


# ======================================================
# 3. UPDATE MEMBER ROLE
# ======================================================
@router.put("/{circle_id}/members/{user_id}/role", response_model=CircleMemberActionResponse)
async def update_member_role(
    circle_id: int,
    user_id: int,
    request: UpdateRoleRequest,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleMemberService = Depends(get_circle_member_service),
) -> CircleMemberActionResponse:
    return await service.update_member_role(circle_id, user_id, request, current_user)

# ======================================================
# 4. SEARCH USERS FOR CIRCLE
# ======================================================
@router.get("/{circle_id}/members/search", response_model=list[UserResponse])
async def search_users(
    circle_id: int,
    query: str,
    current_user: User = Depends(get_current_user_from_session),
    service: CircleMemberService = Depends(get_circle_member_service),
) -> list[UserResponse]:
    return await service.search_users_for_circle(
        current_user=current_user,
        circle_id=circle_id,
        query=query,
    )
