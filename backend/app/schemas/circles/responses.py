""" "
Social feature schemas for Connecto
Circles Responses
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .circle_members import CircleMemberResponse

# ======================================================
# CIRCLE  RESPONSES SCHEMAS
# ======================================================


class CircleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    owner_id: int
    owner_name: str | None = None

    members: list[CircleMemberResponse] = Field(default_factory=list)
    member_count: int | None = None

    created_at: datetime

    is_member: bool | None = None
    is_owner: bool | None = None
    is_private: bool | None = None
    pending_requests_count: int | None = None

    model_config = ConfigDict(from_attributes=True)
