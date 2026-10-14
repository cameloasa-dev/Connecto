#schemas/dashboard/dashboard
from datetime import datetime

from pydantic import BaseModel

from app.schemas.auth.responses import UserResponse
from app.schemas.circles.responses import CircleResponse
from app.schemas.circles.roles import CircleRole


# --------------------------------------------------
# DASHBOARD POST (feed item)
# --------------------------------------------------
class DashboardPostItem(BaseModel):
    id: int
    title: str
    content: str
    circle_id: int
    circle_name: str
    author_name: str
    created_at: datetime


# --------------------------------------------------
# CIRCLES GROUPED BY ROLE
# --------------------------------------------------
class CirclesByRole(BaseModel):
    role: CircleRole
    items: list[CircleResponse]

# --------------------------------------------------
# dashboard stats
# --------------------------------------------------
class DashboardStats(BaseModel):
    total_circles: int
    total_posts_in_feed: int


# --------------------------------------------------
# DASHBOARD RESPONSE (ROOT DTO)
# --------------------------------------------------
class DashboardResponse(BaseModel):
    user: UserResponse
    circles_by_role: list[CirclesByRole]
    recent_posts: list[DashboardPostItem]
    stats: DashboardStats
