from fastapi import HTTPException

from app.db.models import Circle, CircleMember, User
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.circles.members import CircleMemberResponse, CircleRole
from app.schemas.circles.requests import CircleCreate, CircleUpdate
from app.schemas.circles.responses import CircleResponse


class CircleService:
    def __init__(self, repo: CircleRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    # ======================================================
    # DTO HELPERS
    # ======================================================

    def _to_member_dto(
        self,
        member: CircleMember,
        username: str | None,
    ) -> CircleMemberResponse:
        return CircleMemberResponse(
            user_id=member.user_id,
            username=username,
            role=CircleRole(member.role),
            joined_at=member.joined_at,
        )

    async def _to_circle_dto(
        self,
        circle: Circle,
        members: list[CircleMember],
        users: dict[int, User],
        current_user_id: int | None = None,
    ) -> CircleResponse:

        owner = users.get(circle.owner_id)

        member_dtos: list[CircleMemberResponse] = []
        for member in members:
            user = users.get(member.user_id)

            member_dtos.append(
                self._to_member_dto(
                    member,
                    user.username if user else None,
                )
            )

        is_member = current_user_id in users if current_user_id else None
        is_owner = current_user_id == circle.owner_id if current_user_id else None

        return CircleResponse(
            id=circle.id,
            name=circle.name,
            description=circle.description,
            owner_id=circle.owner_id,
            owner_name=owner.username if owner else None,
            members=member_dtos,
            member_count=len(member_dtos),
            created_at=circle.created_at,
            is_member=is_member,
            is_owner=is_owner,
            is_private=circle.is_private,
        )

    # ======================================================
    # GET MY CIRCLES
    # ======================================================

    async def get_my_circles(self, current_user: User) -> list[CircleResponse]:
        circles = await self.repo.get_circles_for_user(current_user.id)

        if not circles:
            return []

        all_members = await self.repo.get_members([c.id for c in circles])

        user_ids = {m.user_id for m in all_members}
        user_ids.add(current_user.id)

        users_list = await self.user_repo.get_users_by_ids(list(user_ids))
        users = {u.id: u for u in users_list}

        grouped_members: dict[int, list[CircleMember]] = {}
        for m in all_members:
            grouped_members.setdefault(m.circle_id, []).append(m)

        return [
            await self._to_circle_dto(
                circle,
                grouped_members.get(circle.id, []),
                users,
                current_user.id,
            )
            for circle in circles
        ]

    # ======================================================
    # CREATE CIRCLE
    # ======================================================

    async def create_circle(
        self,
        circle_data: CircleCreate,
        current_user: User,
    ) -> CircleResponse:

        if await self.repo.circle_name_exists(circle_data.name):
            raise HTTPException(400, "Circle already exists")

        circle = await self.repo.create_circle(
            Circle(
                name=circle_data.name,
                description=circle_data.description,
                is_private=circle_data.is_private,
                owner_id=current_user.id,
            )
        )

        await self.repo.add_member(
            CircleMember(
                circle_id=circle.id,
                user_id=current_user.id,
                role=CircleRole.OWNER,
            )
        )

        return await self.get_circle(circle.id, current_user)

    # ======================================================
    # GET CIRCLE BY ID
    # ======================================================

    async def get_circle(self, circle_id: int, current_user: User) -> CircleResponse:
        circle = await self.repo.get_circle_with_members(circle_id)

        if not circle:
            raise HTTPException(404, "Circle not found")

        members = await self.repo.get_members([circle_id])

        user_ids = {m.user_id for m in members}
        user_ids.add(circle.owner_id)

        users_list = await self.user_repo.get_users_by_ids(list(user_ids))
        users = {u.id: u for u in users_list}

        return await self._to_circle_dto(
            circle,
            members,
            users,
            current_user.id,
        )

    # ======================================================
    # UPDATE CIRCLE
    # ======================================================

    async def update_circle(
        self,
        circle_id: int,
        data: CircleUpdate,
        current_user: User,
    ) -> CircleResponse:

        circle = await self.repo.get_circle_by_id(circle_id)

        if not circle:
            raise HTTPException(404, "Circle not found")

        if circle.owner_id != current_user.id:
            raise HTTPException(403, "Only owner can update circle")

        if data.name is not None:
            circle.name = data.name

        if data.description is not None:
            circle.description = data.description

        if data.is_private is not None:
            circle.is_private = data.is_private

        await self.repo.update_circle(circle)

        return await self.get_circle(circle_id, current_user)

    # ======================================================
    # DELETE CIRCLE
    # ======================================================

    async def delete_circle(self, circle_id: int, current_user: User) -> None:
        circle = await self.repo.get_circle_by_id(circle_id)

        if not circle:
            raise HTTPException(404, "Circle not found")

        if circle.owner_id != current_user.id:
            raise HTTPException(403, "Only owner can delete circle")

        await self.repo.delete_circle(circle)
