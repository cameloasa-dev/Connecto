from app.db.models import User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.search import (
    CircleSearchItem,
    PostSearchItem,
    SearchResponse,
    UserSearchItem,
)


class SearchService:
    def __init__(
        self,
        user_repo: UserRepository,
        circle_repo: CircleRepository,
        post_repo: PostRepository,
    ):
        self.user_repo = user_repo
        self.circle_repo = circle_repo
        self.post_repo = post_repo

    async def search(
        self,
        current_user: User,
        term: str,
        page: int = 1,
        page_size: int = 20,
    ) -> SearchResponse:

        offset = (page - 1) * page_size

        # --------------------------------------------------
        # 1. CIRCLES USER HAS ACCESS TO
        # --------------------------------------------------
        circle_rows = await self.circle_repo.get_user_circles_with_membership(
            current_user.id
        )

        circle_ids = [circle.id for circle, _member in circle_rows]

        # --------------------------------------------------
        # 2. POSTS
        # --------------------------------------------------
        posts_raw = await self.post_repo.search_posts(
            term=term,
            circle_ids=circle_ids,
            limit=page_size,
            offset=offset,
        )

        posts: list[PostSearchItem] = [
            PostSearchItem(
                id=post.id,
                title=post.title,
                content=post.content,
                author_name=author_name,
            )
            for post, author_name, _circle_name in posts_raw
        ]

        # --------------------------------------------------
        # 3. USERS
        # --------------------------------------------------
        users_raw = await self.user_repo.search_users(
            term=term,
            limit=page_size,
            offset=offset,
        )

        users: list[UserSearchItem] = [
            UserSearchItem(
                id=u.id,
                username=u.username,
                email=u.email,
            )
            for u in users_raw
        ]

        # --------------------------------------------------
        # 4. CIRCLES
        # --------------------------------------------------
        circles_raw = await self.circle_repo.search_circles(
            term=term,
            limit=page_size,
            offset=offset,
        )

        circles: list[CircleSearchItem] = [
            CircleSearchItem(
                id=c.id,
                name=c.name,
                description=c.description,
                member_count=getattr(c, "member_count", None),
            )
            for c in circles_raw
        ]

        # --------------------------------------------------
        # 5. RESPONSE
        # --------------------------------------------------
        return SearchResponse(
            query=term,
            page=page,
            page_size=page_size,
            users=users,
            circles=circles,
            posts=posts,
        )
