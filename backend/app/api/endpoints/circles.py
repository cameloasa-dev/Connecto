"""
Circle management endpoints
Session-based authentication
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Circle, CircleMember, User
from app.schemas import (
    CircleCreate,
    CircleMemberResponse,
    CircleResponse,
    CircleRole,
)

router = APIRouter(prefix="/circles", tags=["circles"])


# ======================================================
# HELPERS
# ======================================================

BADGE_MAP = {
    CircleRole.OWNER: "👑",
    CircleRole.MODERATOR: "🛡️",
    CircleRole.MEMBER: "👤",
}


def normalize_role(role: str | CircleRole) -> CircleRole:
    """Ensure role is always a CircleRole enum."""
    return CircleRole(role) if isinstance(role, str) else role


def build_member_response(member: CircleMember, username: str) -> CircleMemberResponse:
    """Build a clean member response object."""
    role_enum = normalize_role(member.role)
    return CircleMemberResponse(
        circle_id=member.circle_id,
        user_id=member.user_id,
        username=username,
        role=role_enum,
        badge=BADGE_MAP.get(role_enum, "👤"),
        joined_at=member.joined_at,
    )


# ======================================================
# GET MY CIRCLES
# ======================================================
@router.get("/my", response_model=list[CircleResponse])
async def get_my_circles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> list[CircleResponse]:

    circles_result = await db.execute(
        select(Circle)
        .join(CircleMember, Circle.id == CircleMember.circle_id)
        .where(CircleMember.user_id == current_user.id)
        .options(selectinload(Circle.members))
        .order_by(Circle.created_at.desc())
    )
    circles = circles_result.scalars().all()

    responses = []

    for circle in circles:
        owner = await db.get(User, circle.owner_id)
        owner_name = owner.username if owner else None

        members_list = []
        for member in circle.members:
            user_obj = await db.get(User, member.user_id)
            if user_obj:
                members_list.append(build_member_response(member, user_obj.username))

        responses.append(
            CircleResponse(
                id=circle.id,
                name=circle.name,
                description=circle.description,
                owner_id=circle.owner_id,
                owner_name=owner_name,
                members=members_list,
                member_count=len(members_list),
                created_at=circle.created_at,
            )
        )

    return responses


# ======================================================
# CREATE CIRCLE
# ======================================================
@router.post("/", response_model=CircleResponse, status_code=status.HTTP_201_CREATED)
async def create_circle(
    circle_data: CircleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> CircleResponse:

    existing = await db.execute(select(Circle).where(Circle.name == circle_data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "A circle with this name already exists")

    new_circle = Circle(
        name=circle_data.name,
        description=circle_data.description,
        owner_id=current_user.id,
    )
    db.add(new_circle)
    await db.flush()

    owner_member = CircleMember(
        circle_id=new_circle.id,
        user_id=current_user.id,
        role=CircleRole.OWNER,
    )
    db.add(owner_member)

    await db.commit()
    await db.refresh(new_circle)

    return CircleResponse(
        id=new_circle.id,
        name=new_circle.name,
        description=new_circle.description,
        owner_id=new_circle.owner_id,
        owner_name=current_user.username,
        members=[build_member_response(owner_member, current_user.username)],
        member_count=1,
        created_at=new_circle.created_at,
    )


# ======================================================
# GET CIRCLE BY ID
# ======================================================
@router.get("/{circle_id}", response_model=CircleResponse)
async def get_circle(
    circle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> CircleResponse:

    circle_result = await db.execute(
        select(Circle).where(Circle.id == circle_id).options(selectinload(Circle.members))
    )
    circle = circle_result.scalar_one_or_none()

    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Check membership
    if not any(m.user_id == current_user.id for m in circle.members):
        raise HTTPException(status_code=403, detail="You are not a member of this circle")

    # Build members
    members = []
    for member in circle.members:
        user_obj = await db.get(User, member.user_id)
        if user_obj:
            members.append(build_member_response(member, user_obj.username))

    owner = await db.get(User, circle.owner_id)

    return CircleResponse(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        owner_id=circle.owner_id,
        owner_name=owner.username if owner else None,
        members=members,
        member_count=len(members),
        created_at=circle.created_at,
    )


# ======================================================
# UPDATE CIRCLE
# ======================================================
@router.put("/{circle_id}", response_model=CircleResponse)
async def update_circle(
    circle_id: int,
    circle_data: CircleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> CircleResponse:

    circle = await db.get(Circle, circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    if circle.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can update the circle")

    circle.name = circle_data.name
    circle.description = circle_data.description

    await db.commit()
    await db.refresh(circle)

    return await get_circle(circle_id, db, current_user)


# ======================================================
# DELETE CIRCLE
# ======================================================
@router.delete("/{circle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circle(
    circle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> None:

    circle = await db.get(Circle, circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    if circle.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can delete the circle")

    await db.delete(circle)
    await db.commit()


# ======================================================
# UPDATE CIRCLE NAME
# ======================================================
@router.put("/{circle_id}/name", response_model=CircleResponse)
async def update_circle_name(
    circle_id: int,
    request: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> CircleResponse:

    circle = await db.get(Circle, circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    if circle.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can change the name")

    new_name = request.get("name")
    if not new_name or len(new_name) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters")

    existing = await db.execute(
        select(Circle).where(Circle.name == new_name, Circle.id != circle_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="A circle with this name already exists")

    circle.name = new_name
    await db.commit()
    await db.refresh(circle)

    return await get_circle(circle_id, db, current_user)
