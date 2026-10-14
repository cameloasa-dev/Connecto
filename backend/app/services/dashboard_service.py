from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth.responses import UserResponse
from app.schemas.circles.responses import CircleResponse
from app.schemas.circles.roles import CircleRole
from app.schemas.dashboard.dashboard import (
    CirclesByRole,
    DashboardPostItem,
    DashboardResponse,
    DashboardStats,
)
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
    async def get_dashboard(self, current_user: User) -> DashboardResponse:

        # ==================================================
        # 1. USER DTO
        # ==================================================
        user_dto = UserResponse.model_validate(current_user)

        # ==================================================
        # 2. CIRCLES GROUPED BY ROLE
        # ==================================================
        circle_rows = await self.circle_repo.get_user_circles_with_membership(current_user.id)

        grouped: dict[CircleRole, list[CircleResponse]] = {}
        circle_ids: list[int] = []

        for circle, role in circle_rows:
            circle_role = CircleRole(role.role)
            grouped.setdefault(circle_role, []).append(
                CircleResponse.model_validate(circle)
            )
            circle_ids.append(circle.id)

        circles_by_role: list[CirclesByRole] = [
            CirclesByRole(role=role, items=circles)
            for role, circles in grouped.items()
        ]

        # ==================================================
        # 3. RECENT POSTS (FEED)
        # ==================================================
        recent_posts: list[DashboardPostItem] = []

        if circle_ids:
            posts = await self.post_repo.get_posts_for_circles(
                circle_ids,
                limit=20,
            )

            for post, author_name, circle_name in posts:
                recent_posts.append(
                    DashboardPostItem(
                        id=post.id,
                        title=post.title,
                        content=post.content,
                        circle_id=post.circle_id,
                        circle_name=circle_name,
                        author_name=author_name,
                        created_at=post.created_at,
                    )
                )

        # ==================================================
        # 4. STATS
        # ==================================================
        stats = DashboardStats(
            total_circles=len(circle_ids),
            total_posts_in_feed=len(recent_posts),
        )

        # ==================================================
        # 5. FINAL DTO
        # ==================================================
        return DashboardResponse(
            user=user_dto,
            circles_by_role=circles_by_role,
            recent_posts=recent_posts,
            stats=stats,
        )
