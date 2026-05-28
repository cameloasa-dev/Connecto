""" "
Social feature schemas for Connecto
Posts, Circles, Circle Members
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

# ======================================================
# POST SCHEMAS
# ======================================================


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    circle_id: int | None = Field(None, description="Optional Circle ID if posting inside a circle")


class PostResponse(PostBase):
    id: int
    author_id: int
    author_name: str | None = None
    circle_id: int | None = None
    circle_name: str | None = None
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# CIRCLE SCHEMAS
# ======================================================


class CircleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)


class CircleCreate(CircleBase):
    pass


class UpdateCircleNameRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)


class CircleRole(StrEnum):
    OWNER = "owner"
    MODERATOR = "moderator"
    MEMBER = "member"


class CircleMemberResponse(BaseModel):
    circle_id: int
    user_id: int
    username: str | None = None
    role: CircleRole
    joined_at: datetime
    badge: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def assign_badge(self):
        badge_map = {CircleRole.OWNER: "👑", CircleRole.MODERATOR: "🛡️", CircleRole.MEMBER: "👤"}
        self.badge = badge_map.get(self.role, "👤")
        return self


class CircleResponse(CircleBase):
    id: int
    owner_id: int
    owner_name: str | None = None
    members: list[CircleMemberResponse] = Field(default_factory=list)
    member_count: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# CIRCLE MEMBER MANAGEMENT
# ======================================================


class CircleMemberUpdate(BaseModel):
    role: CircleRole


class UserSearchResponse(BaseModel):
    id: int
    username: str
    email: str
    is_already_member: bool = False


class AddMemberRequest(BaseModel):
    user_id: int


class UpdateRoleRequest(BaseModel):
    role: CircleRole


class MemberActionResponse(BaseModel):
    success: bool
    message: str
    member: CircleMemberResponse | None = None


# ======================================================
# FUTURE FEATURES
# ======================================================


class CirclePrivacyUpdate(BaseModel):
    is_private: bool


class JoinStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class CircleJoinRequest(BaseModel):
    message: str | None = Field(None, max_length=200)


class CircleJoinResponse(BaseModel):
    request_id: int
    user_id: int
    username: str
    status: JoinStatus
    created_at: datetime
