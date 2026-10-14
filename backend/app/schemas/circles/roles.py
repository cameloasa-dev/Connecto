#schemas/circles/circle_role
from enum import StrEnum

from pydantic import BaseModel

from app.schemas.auth.responses import UserResponse

# ======================================================
# ENUMS
# ======================================================


class CircleRole(StrEnum):
    OWNER = "owner"
    MODERATOR = "moderator"
    MEMBER = "member"



class UserRoleItem(BaseModel):
    circle_id: int
    circle_name: str
    role: CircleRole


class UserRolesResponse(BaseModel):
    user: UserResponse
    roles: list[UserRoleItem]
