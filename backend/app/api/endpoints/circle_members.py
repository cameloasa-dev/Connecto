"""
Circle member management endpoints
Session-based authentication
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Circle, CircleMember, User
from app.schemas import (
    AddMemberRequest,
    CircleMemberResponse,
    CircleRole,
    MemberActionResponse,
    UpdateRoleRequest,
)

router = APIRouter(prefix="/circles", tags=["circle-members"])


# ======================================================
# HELPERS
# ======================================================


def ensure_circle_exists(circle: Circle | None) -> Circle:
    if circle is None:
        raise HTTPException(status_code=404, detail="Circle not found")
    return circle


def ensure_member_exists(member: CircleMember | None) -> CircleMember:
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found in this circle")
    return member


def ensure_user_exists(user: User | None) -> User:
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def ensure_owner_or_moderator(role: CircleRole) -> None:
    if role not in (CircleRole.OWNER, CircleRole.MODERATOR):
        raise HTTPException(
            status_code=403, detail="Only owners and moderators can perform this action"
        )


def ensure_owner(role: CircleRole) -> CircleRole:
    if role != CircleRole.OWNER:
        raise HTTPException(status_code=403, detail="Only the circle owner can perform this action")
    return role


def build_member_response(member: CircleMember, username: str) -> CircleMemberResponse:
    return CircleMemberResponse(
        circle_id=member.circle_id,
        user_id=member.user_id,
        username=username,
        role=CircleRole(member.role),
        joined_at=member.joined_at,
    )


# ======================================================
# 1. ADD MEMBER
# ======================================================
@router.post("/{circle_id}/members", status_code=201, response_model=MemberActionResponse)
async def add_member(
    circle_id: int,
    request: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> MemberActionResponse:

    # Validate circle
    circle = await db.get(Circle, circle_id)
    ensure_circle_exists(circle)

    # Check current user's role
    current_role = await db.execute(
        select(CircleMember.role).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id,
        )
    )
    role_str = current_role.scalar_one_or_none()
    if role_str is None:
        raise HTTPException(
            status_code=403,
            detail="Role not found. You must be a member of the circle to add members.",
        )

    # Permission check
    role = CircleRole(role_str)
    ensure_owner_or_moderator(role)

    # Check user to add
    user_to_add = await db.get(User, request.user_id)
    user_to_add = ensure_user_exists(user_to_add)
    assert user_to_add is not None  # for type checker

    # Check if already member
    existing = await db.execute(
        select(CircleMember).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == request.user_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "User is already a member of this circle")

    # Add member
    new_member = CircleMember(
        circle_id=circle_id,
        user_id=request.user_id,
        role=CircleRole.MEMBER,
        joined_at=datetime.now(),
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)

    return MemberActionResponse(
        success=True,
        message="Member added successfully",
        member=build_member_response(new_member, user_to_add.username),
    )


# ======================================================
# 2. REMOVE MEMBER
# ======================================================
@router.delete("/{circle_id}/members/{user_id}", response_model=MemberActionResponse)
async def remove_member(
    circle_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> MemberActionResponse:

    circle = await db.get(Circle, circle_id)
    ensure_circle_exists(circle)

    # Member to remove
    member_result = await db.execute(
        select(CircleMember).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == user_id,
        )
    )
    member = member_result.scalar_one_or_none()
    member = ensure_member_exists(member)

    # Cannot remove owner
    if member.role == CircleRole.OWNER:
        raise HTTPException(status_code=403, detail="Cannot remove the circle owner")

    # Current user's role
    current_role_result = await db.execute(
        select(CircleMember.role).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id,
        )
    )
    current_role = current_role_result.scalar_one_or_none()

    if not current_role:
        raise HTTPException(status_code=403, detail="You are not a member of this circle")

    # Permission logic
    if current_role == CircleRole.OWNER:
        pass  # owner can remove anyone except owner
    elif current_role == CircleRole.MODERATOR:
        if member.role == CircleRole.MODERATOR:
            raise HTTPException(status_code=403, detail="Moderators cannot remove other moderators")
    else:
        raise HTTPException(status_code=403, detail="Only owners and moderators can remove members")

    # Remove member
    user = await db.get(User, user_id)
    user = ensure_user_exists(user)

    await db.delete(member)
    await db.commit()

    return MemberActionResponse(
        success=True,
        message=f"Member {user.username} removed successfully",
        member=None,
    )


# ======================================================
# 3. UPDATE MEMBER ROLE
# ======================================================
@router.put("/{circle_id}/members/{user_id}/role", response_model=MemberActionResponse)
async def update_member_role(
    circle_id: int,
    user_id: int,
    request: UpdateRoleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> MemberActionResponse:

    # Only owner can change roles
    owner_check = await db.execute(
        select(CircleMember.role).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id,
        )
    )

    role_str = owner_check.scalar_one_or_none()
    if role_str is None:
        raise HTTPException(status_code=403, detail="You are not a member of this circle")
    role = CircleRole(role_str)
    ensure_owner(role)

    # Member to update
    member_result = await db.execute(
        select(CircleMember).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == user_id,
        )
    )
    member = member_result.scalar_one_or_none()
    member = ensure_member_exists(member)

    # Cannot change owner's role
    if member.role == CircleRole.OWNER:
        raise HTTPException(status_code=403, detail="Cannot change the circle owner's role")

    # Update role
    old_role = member.role
    member.role = request.role

    await db.commit()
    await db.refresh(member)

    user = await db.get(User, user_id)
    user = ensure_user_exists(user)

    return MemberActionResponse(
        success=True,
        message=f"Role changed from {old_role} to {request.role}",
        member=build_member_response(member, user.username),
    )
