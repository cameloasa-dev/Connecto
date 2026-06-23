from datetime import datetime

from fastapi import HTTPException

from app.db.models import Comment, Post, User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.circles.circle_members import CircleRole
from app.schemas.posts.comments import CommentCreate
from app.schemas.posts.comments import CommentResponse
from app.schemas.posts.likes import LikeResponse
from app.schemas.posts.requests import PostCreate
from app.schemas.posts.responses import PostResponse


class PostService:
    def __init__(
        self,
        post_repo: PostRepository,
        circle_repo: CircleRepository,
        user_repo: UserRepository,
    ):
        self.post_repo = post_repo
        self.circle_repo = circle_repo
        self.user_repo = user_repo

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    async def _ensure_post(self, post_id: int) -> Post:
        post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise HTTPException(404, "Post not found")
        return post

    async def _ensure_circle_member(self, circle_id: int, user_id: int) -> None:
        if not await self.circle_repo.is_member(circle_id, user_id):
            raise HTTPException(403, "Not a member of this circle")

    async def _build_post_response(self, post: Post) -> PostResponse:
        author = await self.user_repo.get_by_id(post.author_id)
        circle = await self.circle_repo.get_circle_by_id(post.circle_id) if post.circle_id else None

        likes_count = await self.post_repo.count_likes(post.id)
        comments_count = await self.post_repo.count_comments(post.id)

        return PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            author_name=author.username if author else None,
            circle_id=post.circle_id,
            circle_name=circle.name if circle else None,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=likes_count,
            comments_count=comments_count,
        )

    # --------------------------------------------------
    # CREATE POST
    # --------------------------------------------------

    async def create_post(self, data: PostCreate, current_user: User) -> PostResponse:
        if data.circle_id:
            await self._ensure_circle_member(data.circle_id, current_user.id)

        post = Post(
            title=data.title,
            content=data.content,
            author_id=current_user.id,
            circle_id=data.circle_id,
        )

        created = await self.post_repo.create_post(post)
        return await self._build_post_response(created)

    # --------------------------------------------------
    # UPDATE POST
    # --------------------------------------------------

    async def update_post(self, post_id: int, data: PostCreate, current_user: User) -> PostResponse:

        post = await self._ensure_post(post_id)

        if post.author_id != current_user.id:
            raise HTTPException(403, "Not allowed")

        post.title = data.title
        post.content = data.content

        updated = await self.post_repo.update_post(post)
        return await self._build_post_response(updated)

    # --------------------------------------------------
    # DELETE POST
    # --------------------------------------------------

    async def delete_post(self, post_id: int, current_user: User) -> None:
        post = await self._ensure_post(post_id)

        # Author can delete
        if post.author_id == current_user.id:
            await self.post_repo.delete_post(post)
            return

        # Circle moderators/owners can delete
        if post.circle_id:
            role = await self.circle_repo.get_user_role(post.circle_id, current_user.id)
            if role in (CircleRole.OWNER, CircleRole.MODERATOR):
                await self.post_repo.delete_post(post)
                return

        raise HTTPException(403, "You don't have permission to delete this post")

    # --------------------------------------------------
    # GET POST BY ID
    # --------------------------------------------------

    async def get_post(self, post_id: int, current_user: User) -> PostResponse:
        row = await self.post_repo.get_post_with_author_and_circle(post_id)
        if not row:
            raise HTTPException(404, "Post not found")

        post, author_name, circle_name = row

        if post.circle_id:
            await self._ensure_circle_member(post.circle_id, current_user.id)

        return await self._build_post_response(post)

    # --------------------------------------------------
    # GET POSTS FOR CIRCLE
    # --------------------------------------------------

    async def get_circle_posts(
        self, circle_id: int, current_user: User, limit: int, offset: int
    ) -> list[PostResponse]:

        await self._ensure_circle_member(circle_id, current_user.id)

        rows = await self.post_repo.get_posts_for_circle(circle_id, limit, offset)

        responses: list[PostResponse] = []
        for post, _author_name in rows:
            responses.append(await self._build_post_response(post))

        return responses

    # --------------------------------------------------
    # LIKE / UNLIKE
    # --------------------------------------------------

    async def toggle_like(self, post_id: int, current_user: User) -> LikeResponse:
        post = await self._ensure_post(post_id)

        if post.circle_id:
            await self._ensure_circle_member(post.circle_id, current_user.id)

        if await self.post_repo.has_liked(post_id, current_user.id):
            await self.post_repo.remove_like(post_id, current_user.id)
            liked = False
        else:
            await self.post_repo.add_like(post_id, current_user.id)
            liked = True

        count = await self.post_repo.count_likes(post_id)

        return LikeResponse(
            success=True,
            liked=liked,
            likes_count=count,
        )

    # --------------------------------------------------
    # COMMENTS
    # --------------------------------------------------

    async def add_comment(
        self, post_id: int, data: CommentCreate, current_user: User
    ) -> CommentResponse:

        post = await self._ensure_post(post_id)

        if post.circle_id:
            await self._ensure_circle_member(post.circle_id, current_user.id)

        comment = Comment(
            post_id=post_id,
            user_id=current_user.id,
            content=data.content,
            created_at=datetime.now(),
        )

        created = await self.post_repo.add_comment(comment)

        user = await self.user_repo.get_by_id(current_user.id)

        return CommentResponse(
            id=created.id,
            post_id=post_id,
            user_id=current_user.id,
            username=user.username if user else None,
            content=created.content,
            created_at=created.created_at,
        )

    async def delete_comment(self, comment_id: int, current_user: User) -> None:

        # We need to fetch the comment manually
        comments = await self.post_repo.get_comments_for_post(post_id=0)  # placeholder
        comment = next((c for c in comments if c.id == comment_id), None)

        if not comment:
            raise HTTPException(404, "Comment not found")

        # Only author or moderator/owner can delete
        if comment.user_id != current_user.id:
            post = await self._ensure_post(comment.post_id)
            if post.circle_id:
                role = await self.circle_repo.get_user_role(post.circle_id, current_user.id)
                if role not in (CircleRole.OWNER, CircleRole.MODERATOR):
                    raise HTTPException(403, "Not allowed")

        await self.post_repo.delete_comment(comment)
