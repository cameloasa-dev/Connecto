"""
Endpoints package
Exports all API routers
"""

from .auth import router as auth_router
from .circle_members import router as circle_members_router
from .circles import router as circles_router
from .dashboard import router as dashboard_router
from .posts import router as posts_router
from .search import router as search_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "circles_router",
    "circle_members_router",
    "posts_router",
    "search_router",
    "dashboard_router",
]
