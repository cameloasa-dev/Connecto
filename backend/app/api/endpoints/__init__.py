"""
Endpoints package
Exports all API routers
"""

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.circle_members import router as circle_members_router
from app.api.endpoints.circles import router as circles_router
from app.api.endpoints.posts import router as posts_router
from app.api.endpoints.users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "circles_router",
    "circle_members_router",
    "posts_router",
]
