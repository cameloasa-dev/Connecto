from typing import Any

from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.post_service import PostService


class SearchService:
    def __init__(
        self,
        post_repo: PostRepository,
        user_repo: UserRepository,
        circle_repo: CircleRepository,
        post_service: PostService,
    ):
        self.post_repo = post_repo
        self.user_repo = user_repo
        self.circle_repo = circle_repo
        self.post_service = post_service

    # --------------------------------------------------
    # MAIN SEARCH
    # --------------------------------------------------
    async def search(
        self,
        current_user: User,
        term: str,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:

        offset = (page - 1) * page_size

        # 1. users is member
        circle_rows = await self.circle_repo.get_circles_with_role_for_user(current_user.id)
        circle_ids = [circle.id for circle, _role in circle_rows]

        # 2. POSTS SEARCH
        posts_raw = await self.post_repo.search_posts(
            term=term,
            circle_ids=circle_ids,
            limit=page_size,
            offset=offset,
        )

        posts: list[dict[str, Any]] = []
        for post, _author_name, _circle_name in posts_raw:
            posts.append((await self.post_service._build_post_response(post)).model_dump())

        # 3. USERS SEARCH
        users_raw = await self.user_repo.search_users(
            term=term,
            limit=page_size,
            offset=offset,
        )

        users = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "created_at": u.created_at,
            }
            for u in users_raw
        ]

        # 4. CIRCLES SEARCH
        circles_raw = await self.circle_repo.search_circles(
            term=term,
            limit=page_size,
            offset=offset,
        )

        circles = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "created_at": c.created_at,
            }
            for c in circles_raw
        ]

        # 5. Final structure
        return {
            "query": term,
            "page": page,
            "page_size": page_size,
            "results": {
                "posts": posts,
                "users": users,
                "circles": circles,
            },
        }
