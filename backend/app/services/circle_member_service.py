from datetime import datetime

from fastapi import HTTPException

from app.db.models import CircleMember, User
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth.responses import UserResponse
from app.schemas.circles.members import (
    AddMemberRequest,
    CircleMemberActionResponse,
    CircleMemberResponse,
    CircleRole,
    UpdateRoleRequest,
)


class CircleMemberService:
    def __init__(self, circle_repo: CircleRepository, user_repo: UserRepository):
        self.circle_repo = circle_repo
        self.user_repo = user_repo

    # ======================================================
    # HELPERS
    # ======================================================

    def _to_role(self, role: str) -> CircleRole:
        return CircleRole(role)

    def _to_member_response(
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

    async def _get_current_role(
        self,
        circle_id: int,
        user_id: int,
    ) -> CircleRole | None:

        member = await self.circle_repo.get_member(circle_id, user_id)
        return CircleRole(member.role) if member else None

    def _require_role(self, role: CircleRole | None) -> CircleRole:
        if role is None:
            raise HTTPException(403, "Not a member of this circle")
        return role

    def _require_moderator_or_owner(self, role: CircleRole) -> None:
        if role not in (CircleRole.OWNER, CircleRole.MODERATOR):
            raise HTTPException(403, "Not allowed")

    def _require_owner(self, role: CircleRole) -> None:
        if role != CircleRole.OWNER:
            raise HTTPException(403, "Only owner allowed")

    # ======================================================
    # ADD MEMBER
    # ======================================================

    async def add_member(
        self,
        circle_id: int,
        request: AddMemberRequest,
        current_user: User,
    ) -> CircleMemberActionResponse:

        role = await self._get_current_role(circle_id, current_user.id)
        role = self._require_role(role)
        self._require_moderator_or_owner(role)

        if await self.circle_repo.get_member(circle_id, request.user_id):
            raise HTTPException(400, "Already a member")

        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise HTTPException(404, "User not found")

        new_member = CircleMember(
            circle_id=circle_id,
            user_id=user.id,
            role=CircleRole.MEMBER.value,
            joined_at=datetime.utcnow(),
        )

        await self.circle_repo.add_member(new_member)

        return CircleMemberActionResponse(
            success=True,
            message="Member added successfully",
            member=self._to_member_response(new_member, user.username),
        )

    # ======================================================
    # REMOVE MEMBER
    # ======================================================

    async def remove_member(
        self,
        circle_id: int,
        user_id: int,
        current_user: User,
    ) -> CircleMemberActionResponse:

        role = await self._get_current_role(circle_id, current_user.id)
        role = self._require_role(role)
        self._require_moderator_or_owner(role)

        member = await self.circle_repo.get_member(circle_id, user_id)
        if not member:
            raise HTTPException(404, "Member not found")

        if member.role == CircleRole.OWNER.value:
            raise HTTPException(403, "Cannot remove owner")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        await self.circle_repo.remove_member(member)

        return CircleMemberActionResponse(
            success=True,
            message=f"Member {user.username} removed successfully",
            member=None,
        )

    # ======================================================
    # UPDATE ROLE
    # ======================================================

    async def update_member_role(
        self,
        circle_id: int,
        user_id: int,
        request: UpdateRoleRequest,
        current_user: User,
    ) -> CircleMemberActionResponse:

        role = await self._get_current_role(circle_id, current_user.id)
        role = self._require_role(role)
        self._require_owner(role)

        member = await self.circle_repo.get_member(circle_id, user_id)
        if not member:
            raise HTTPException(404, "Member not found")

        if member.role == CircleRole.OWNER.value:
            raise HTTPException(403, "Cannot change owner role")

        old_role = member.role

        updated_member = await self.circle_repo.update_member_role(
            member,
            request.role.value,
        )

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        return CircleMemberActionResponse(
            success=True,
            message=f"Role changed from {old_role} to {request.role.value}",
            member=self._to_member_response(updated_member, user.username),
        )

    # ======================================================
    # SEARCH USERS FOR ADD FLOW
    # ======================================================

    async def search_users_for_circle(
        self,
        current_user: User,
        circle_id: int,
        query: str,
    ) -> list[UserResponse]:

        role = await self._get_current_role(circle_id, current_user.id)
        role = self._require_role(role)
        self._require_moderator_or_owner(role)

        if not query.strip():
            return []

        exclude_ids = await self.circle_repo.get_member_user_ids(circle_id)

        users = await self.user_repo.search_users(
            term=query,
            exclude_ids=exclude_ids,
            current_user_id=current_user.id,
        )

        return [UserResponse.model_validate(u) for u in users]
