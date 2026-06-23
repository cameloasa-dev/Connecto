from datetime import datetime

from fastapi import HTTPException

from app.db.models import Circle, CircleMember, User
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.circles.circle_members import (
    AddMemberRequest,
    CircleMemberResponse,
    CircleRole,
    MemberActionResponse,
    UpdateRoleRequest,
)


class CircleMemberService:
    def __init__(self, circle_repo: CircleRepository, user_repo: UserRepository):
        self.circle_repo = circle_repo
        self.user_repo = user_repo

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _ensure_circle(self, circle: Circle | None) -> Circle:
        if not circle:
            raise HTTPException(404, "Circle not found")
        return circle

    def _ensure_member(self, member: CircleMember | None) -> CircleMember:
        if not member:
            raise HTTPException(404, "Member not found in this circle")
        return member

    def _ensure_user(self, user: User | None) -> User:
        if not user:
            raise HTTPException(404, "User not found")
        return user

    def _ensure_owner_or_moderator(self, role: CircleRole) -> None:
        if role not in (CircleRole.OWNER, CircleRole.MODERATOR):
            raise HTTPException(403, "Only owners and moderators can perform this action")

    def _ensure_owner(self, role: CircleRole) -> None:
        if role != CircleRole.OWNER:
            raise HTTPException(403, "Only the circle owner can perform this action")

    def _build_member_response(self, member: CircleMember, username: str) -> CircleMemberResponse:
        return CircleMemberResponse(
            circle_id=member.circle_id,
            user_id=member.user_id,
            username=username,
            role=CircleRole(member.role),
            joined_at=member.joined_at,
        )

    # --------------------------------------------------
    # ADD MEMBER
    # --------------------------------------------------

    async def add_member(
        self,
        circle_id: int,
        request: AddMemberRequest,
        current_user: User,
    ) -> MemberActionResponse:

        self._ensure_circle(await self.circle_repo.get_circle_by_id(circle_id))

        # Current user's role
        current_role = await self.circle_repo.get_user_role(circle_id, current_user.id)
        if current_role is None:
            raise HTTPException(403, "You must be a member of the circle to add members")

        self._ensure_owner_or_moderator(current_role)

        # User to add
        user_to_add = self._ensure_user(await self.user_repo.get_by_id(request.user_id))

        # Already member?
        if await self.circle_repo.is_member(circle_id, request.user_id):
            raise HTTPException(400, "User is already a member of this circle")

        # Add member
        new_member = CircleMember(
            circle_id=circle_id,
            user_id=request.user_id,
            role=CircleRole.MEMBER,
            joined_at=datetime.now(),
        )

        await self.circle_repo.add_member(new_member)

        return MemberActionResponse(
            success=True,
            message="Member added successfully",
            member=self._build_member_response(new_member, user_to_add.username),
        )

    # --------------------------------------------------
    # REMOVE MEMBER
    # --------------------------------------------------

    async def remove_member(
        self,
        circle_id: int,
        user_id: int,
        current_user: User,
    ) -> MemberActionResponse:

        self._ensure_circle(await self.circle_repo.get_circle_by_id(circle_id))

        member = self._ensure_member(await self.circle_repo.get_member(circle_id, user_id))

        # Cannot remove owner
        if member.role == CircleRole.OWNER:
            raise HTTPException(403, "Cannot remove the circle owner")

        # Current user's role
        current_role = await self.circle_repo.get_user_role(circle_id, current_user.id)
        if current_role is None:
            raise HTTPException(403, "You are not a member of this circle")

        # Permission logic
        if current_role == CircleRole.OWNER:
            pass
        elif current_role == CircleRole.MODERATOR:
            if member.role == CircleRole.MODERATOR:
                raise HTTPException(403, "Moderators cannot remove other moderators")
        else:
            raise HTTPException(403, "Only owners and moderators can remove members")

        user = self._ensure_user(await self.user_repo.get_by_id(user_id))

        await self.circle_repo.remove_member(member)

        return MemberActionResponse(
            success=True,
            message=f"Member {user.username} removed successfully",
            member=None,
        )

    # --------------------------------------------------
    # UPDATE MEMBER ROLE
    # --------------------------------------------------

    async def update_member_role(
        self,
        circle_id: int,
        user_id: int,
        request: UpdateRoleRequest,
        current_user: User,
    ) -> MemberActionResponse:

        # Only owner can change roles
        current_role = await self.circle_repo.get_user_role(circle_id, current_user.id)
        if current_role is None:
            raise HTTPException(403, "You are not a member of this circle")

        self._ensure_owner(current_role)

        member = self._ensure_member(await self.circle_repo.get_member(circle_id, user_id))

        # Cannot change owner's role
        if member.role == CircleRole.OWNER:
            raise HTTPException(403, "Cannot change the circle owner's role")

        old_role = member.role

        updated_member = await self.circle_repo.update_member_role(member, request.role)

        user = self._ensure_user(await self.user_repo.get_by_id(user_id))

        return MemberActionResponse(
            success=True,
            message=f"Role changed from {old_role} to {request.role}",
            member=self._build_member_response(updated_member, user.username),
        )
