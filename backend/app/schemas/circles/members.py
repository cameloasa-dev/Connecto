#schemas/circles/members


from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from .roles import CircleRole

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


class CircleMemberActionResponse(BaseModel):
    success: bool
    message: str
    member: CircleMemberResponse | None = None

