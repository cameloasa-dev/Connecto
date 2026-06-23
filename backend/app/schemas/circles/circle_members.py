""" "
Social feature schemas for Connecto
Circle Members
"""

from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

# ======================================================
# ENUMS
# ======================================================


class CircleRole(StrEnum):
    OWNER = "owner"
    MODERATOR = "moderator"
    MEMBER = "member"


# ======================================================
# REQUEST SCHEMAS
# ======================================================


class AddMemberRequest(BaseModel):
    user_id: int


class UpdateRoleRequest(BaseModel):
    role: CircleRole


# ======================================================
# RESPONSE SCHEMAS
# ======================================================


class CircleMemberResponse(BaseModel):
    circle_id: int
    user_id: int
    username: str | None = None
    role: CircleRole
    joined_at: datetime
    badge: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def assign_badge(self) -> Self:
        badge_map = {
            CircleRole.OWNER: "👑",
            CircleRole.MODERATOR: "🛡️",
            CircleRole.MEMBER: "👤",
        }
        self.badge = badge_map.get(self.role, "👤")
        return self


class UserSearchResponse(BaseModel):
    id: int
    username: str
    email: str
    is_already_member: bool = False


class MemberActionResponse(BaseModel):
    success: bool
    message: str
    member: CircleMemberResponse | None = None
