from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


# ======================================================
# ENUMS
# ======================================================
class JoinStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# ======================================================
# REQUEST SCHEMAS
# ======================================================
class CircleJoinRequest(BaseModel):
    message: str | None = Field(None, max_length=200)


# ======================================================
# RESPONSE SCHEMAS
# ======================================================
class CircleJoinResponse(BaseModel):
    request_id: int
    user_id: int
    username: str
    status: JoinStatus
    created_at: datetime
