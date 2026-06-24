from typing import Any

from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.post_service import PostService


class DashboardService:
    def __init__(
        self,
        circle_repo: CircleRepository,
        post_repo: PostRepository,
        user_repo: UserRepository,
        post_service: PostService,
    ):
        self.circle_repo = circle_repo
        self.post_repo = post_repo
        self.user_repo = user_repo
        self.post_service = post_service

    # --------------------------------------------------
    # MAIN DASHBOARD
    # --------------------------------------------------
    async def get_dashboard(self, current_user: User) -> dict[str, Any]:

        # 1. USER INFO
        user_info = {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "created_at": current_user.created_at,
        }

        # 2. CIRCLES + ROLE
        circle_rows = await self.circle_repo.get_circles_with_role_for_user(current_user.id)

        circles: list[dict[str, Any]] = []
        circle_ids: list[int] = []

        for circle, role in circle_rows:
            circles.append(
                {
                    "id": circle.id,
                    "name": circle.name,
                    "description": circle.description,
                    "is_private": circle.is_private,
                    "role": role,
                }
            )
            circle_ids.append(circle.id)

        # 3. FEED (posts from all circles)
        feed: list[dict[str, Any]] = []

        if circle_ids:
            posts = await self.post_repo.get_posts_for_circles(circle_ids, limit=20)

            for post, _author_name, _circle_name in posts:
                # use build response
                feed.append((await self.post_service._build_post_response(post)).model_dump())

        # 4. STATS
        stats = {
            "total_circles": len(circles),
            "total_posts_in_feed": len(feed),
        }

        return {
            "user": user_info,
            "circles": circles,
            "feed": feed,
            "stats": stats,
        }
