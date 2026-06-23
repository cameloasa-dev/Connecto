from collections.abc import Sequence

from fastapi import HTTPException

from app.db.models import Circle, CircleMember, User
from app.repositories.circle_repository import CircleRepository
from app.schemas.circles.circle_members import CircleMemberResponse, CircleRole
from app.schemas.circles.requests import CircleCreate
from app.schemas.circles.responses import CircleResponse


class CircleService:
    def __init__(self, repo: CircleRepository):
        self.repo = repo

    # --------------------------------------------------
    # HELPERS (business logic)
    # --------------------------------------------------

    def _build_member_response(self, member: CircleMember, username: str) -> CircleMemberResponse:
        badge_map = {
            CircleRole.OWNER: "👑",
            CircleRole.MODERATOR: "🛡️",
            CircleRole.MEMBER: "👤",
        }

        role_enum = CircleRole(member.role)
        return CircleMemberResponse(
            circle_id=member.circle_id,
            user_id=member.user_id,
            username=username,
            role=role_enum,
            badge=badge_map.get(role_enum, "👤"),
            joined_at=member.joined_at,
        )

    async def _build_circle_response(self, circle: Circle) -> CircleResponse:
        owner = await self.repo.get_user_by_id(circle.owner_id)
        owner_name = owner.username if owner else None

        members: Sequence[CircleMember] = await self.repo.get_members_for_circle(circle.id)

        member_responses: list[CircleMemberResponse] = []
        for member in members:
            user_obj = await self.repo.get_user_by_id(member.user_id)
            if user_obj:
                member_responses.append(self._build_member_response(member, user_obj.username))

        return CircleResponse(
            id=circle.id,
            name=circle.name,
            description=circle.description,
            owner_id=circle.owner_id,
            owner_name=owner_name,
            members=member_responses,
            member_count=len(member_responses),
            created_at=circle.created_at,
        )

    # --------------------------------------------------
    # GET MY CIRCLES
    # --------------------------------------------------

    async def get_my_circles(self, current_user: User) -> list[CircleResponse]:
        circles = await self.repo.get_circles_for_user(current_user.id)
        return [await self._build_circle_response(circle) for circle in circles]

    # --------------------------------------------------
    # CREATE CIRCLE
    # --------------------------------------------------

    async def create_circle(self, circle_data: CircleCreate, current_user: User) -> CircleResponse:
        if await self.repo.circle_name_exists(circle_data.name):
            raise HTTPException(400, "A circle with this name already exists")

        new_circle = Circle(
            name=circle_data.name,
            description=circle_data.description,
            owner_id=current_user.id,
        )

        circle = await self.repo.create_circle(new_circle)

        owner_member = CircleMember(
            circle_id=circle.id,
            user_id=current_user.id,
            role=CircleRole.OWNER,
        )

        await self.repo.add_member(owner_member)

        return await self._build_circle_response(circle)

    # --------------------------------------------------
    # GET CIRCLE BY ID
    # --------------------------------------------------

    async def get_circle(self, circle_id: int, current_user: User) -> CircleResponse:
        circle = await self.repo.get_circle_with_members(circle_id)
        if not circle:
            raise HTTPException(404, "Circle not found")

        if not await self.repo.is_member(circle_id, current_user.id):
            raise HTTPException(403, "You are not a member of this circle")

        return await self._build_circle_response(circle)

    # --------------------------------------------------
    # UPDATE CIRCLE
    # --------------------------------------------------

    async def update_circle(
        self, circle_id: int, data: CircleCreate, current_user: User
    ) -> CircleResponse:
        circle = await self.repo.get_circle_by_id(circle_id)
        if not circle:
            raise HTTPException(404, "Circle not found")

        if circle.owner_id != current_user.id:
            raise HTTPException(403, "Only the owner can update the circle")

        circle.name = data.name
        circle.description = data.description

        await self.repo.update_circle(circle)

        return await self.get_circle(circle_id, current_user)

    # --------------------------------------------------
    # DELETE CIRCLE
    # --------------------------------------------------

    async def delete_circle(self, circle_id: int, current_user: User) -> None:
        circle = await self.repo.get_circle_by_id(circle_id)
        if not circle:
            raise HTTPException(404, "Circle not found")

        if circle.owner_id != current_user.id:
            raise HTTPException(403, "Only the owner can delete the circle")

        await self.repo.delete_circle(circle)

    # --------------------------------------------------
    # UPDATE CIRCLE NAME
    # --------------------------------------------------

    async def update_circle_name(
        self, circle_id: int, new_name: str, current_user: User
    ) -> CircleResponse:
        circle = await self.repo.get_circle_by_id(circle_id)
        if not circle:
            raise HTTPException(404, "Circle not found")

        if circle.owner_id != current_user.id:
            raise HTTPException(403, "Only the owner can change the name")

        if not new_name or len(new_name) < 3:
            raise HTTPException(400, "Name must be at least 3 characters")

        if await self.repo.circle_name_exists(new_name, exclude_id=circle_id):
            raise HTTPException(400, "A circle with this name already exists")

        circle.name = new_name
        await self.repo.update_circle(circle)

        return await self.get_circle(circle_id, current_user)
