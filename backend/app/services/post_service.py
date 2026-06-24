from datetime import datetime

from fastapi import HTTPException

from app.db.models import Comment, Post, User
from app.repositories.circle_repository import CircleRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.circles.circle_members import CircleRole
from app.schemas.posts.comments import CommentCreate, CommentResponse
from app.schemas.posts.likes import LikeToggleResponse
from app.schemas.posts.requests import PostCreate, PostUpdate
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

    async def _ensure_comment(self, comment_id: int) -> Comment:
        comment = await self.post_repo.get_comment_by_id(comment_id)
        if not comment:
            raise HTTPException(404, "Comment not found")
        return comment

    async def _build_post_response(
        self, post: Post, current_user: User | None = None
    ) -> PostResponse:

        author = await self.user_repo.get_by_id(post.author_id)
        circle = await self.circle_repo.get_circle_by_id(post.circle_id) if post.circle_id else None

        liked_by_me = False
        can_edit = False
        can_delete = False

        if current_user:
            liked_by_me = await self.post_repo.has_liked(post.id, current_user.id)

            is_author = post.author_id == current_user.id

            if post.circle_id is None:
                is_owner_or_moderator = False
            else:
                is_owner_or_moderator = await self.circle_repo.user_is_owner_or_moderator(
                    post.circle_id, current_user.id
                )

            can_edit = is_author or is_owner_or_moderator
            can_delete = is_author or is_owner_or_moderator

        likes_count = await self.post_repo.count_likes(post.id)
        comments_count = await self.post_repo.count_comments(post.id, status="approved")

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
            liked_by_me=liked_by_me,
            can_delete=can_delete,
            can_edit=can_edit,
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
        return await self._build_post_response(created, current_user)

    # --------------------------------------------------
    # UPDATE POST
    # --------------------------------------------------

    async def update_post(self, post_id: int, data: PostUpdate, current_user: User) -> PostResponse:

        post = await self._ensure_post(post_id)

        if post.author_id != current_user.id:
            raise HTTPException(403, "Not allowed")

        if data.title is not None:
            post.title = data.title

        if data.content is not None:
            post.content = data.content

        if data.circle_id is not None:
            await self._ensure_circle_member(data.circle_id, current_user.id)
            post.circle_id = data.circle_id

        if data.circle_id is None and data.circle_id is not ...:
            post.circle_id = None

        updated = await self.post_repo.update_post(post)
        return await self._build_post_response(updated, current_user)

    # --------------------------------------------------
    # DELETE POST
    # --------------------------------------------------

    async def delete_post(self, post_id: int, current_user: User) -> None:
        post = await self._ensure_post(post_id)

        if post.author_id == current_user.id:
            await self.post_repo.delete_post(post)
            return

        if post.circle_id:
            role = await self.circle_repo.get_user_role(post.circle_id, current_user.id)
            if role in (CircleRole.OWNER, CircleRole.MODERATOR):
                await self.post_repo.delete_post(post)
                return

        raise HTTPException(403, "You don't have permission to delete this post")

    # --------------------------------------------------
    # GET POST BY ID (with approved comments)
    # --------------------------------------------------

    async def get_post(self, post_id: int, current_user: User) -> PostResponse:
        post = await self._ensure_post(post_id)

        if post.circle_id:
            await self._ensure_circle_member(post.circle_id, current_user.id)

        return await self._build_post_response(post, current_user)

    # --------------------------------------------------
    # GET POSTS FOR CIRCLE
    # --------------------------------------------------

    async def get_circle_posts(
        self, circle_id: int, current_user: User, limit: int, offset: int
    ) -> list[PostResponse]:

        await self._ensure_circle_member(circle_id, current_user.id)

        rows = await self.post_repo.get_posts_for_circle(circle_id, limit, offset)

        return [await self._build_post_response(post, current_user) for post, _author_name in rows]

    # --------------------------------------------------
    # LIKE / UNLIKE
    # --------------------------------------------------

    async def toggle_like(self, post_id: int, current_user: User) -> LikeToggleResponse:
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

        return LikeToggleResponse(
            success=True,
            liked=liked,
            likes_count=count,
        )

    # --------------------------------------------------
    # COMMENTS (pending)
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
            status="pending",
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
            status=created.status,
            created_at=created.created_at,
        )

    # --------------------------------------------------
    # APPROVE COMMENT
    # --------------------------------------------------

    async def approve_comment(self, comment_id: int, current_user: User) -> CommentResponse:
        comment = await self._ensure_comment(comment_id)
        post = await self._ensure_post(comment.post_id)

        if post.circle_id:
            role = await self.circle_repo.get_user_role(post.circle_id, current_user.id)
            if role not in (CircleRole.OWNER, CircleRole.MODERATOR):
                raise HTTPException(403, "Not allowed")

        comment.status = "approved"
        updated = await self.post_repo.update_comment(comment)

        user = await self.user_repo.get_by_id(comment.user_id)

        return CommentResponse(
            id=updated.id,
            post_id=updated.post_id,
            user_id=updated.user_id,
            username=user.username if user else None,
            content=updated.content,
            status=updated.status,
            created_at=updated.created_at,
        )

    # --------------------------------------------------
    # DELETE COMMENT (author or moderator)
    # --------------------------------------------------

    async def delete_comment(self, comment_id: int, current_user: User) -> None:
        comment = await self._ensure_comment(comment_id)
        post = await self._ensure_post(comment.post_id)

        if comment.user_id == current_user.id:
            await self.post_repo.delete_comment(comment)
            return

        if post.circle_id:
            role = await self.circle_repo.get_user_role(post.circle_id, current_user.id)
            if role in (CircleRole.OWNER, CircleRole.MODERATOR):
                await self.post_repo.delete_comment(comment)
                return

        raise HTTPException(403, "Not allowed")

    # --------------------------------------------------
    # Get pending COMMENT (author or moderator)
    # --------------------------------------------------
    async def get_pending_comments(self, post_id: int, current_user: User) -> list[CommentResponse]:
        post = await self._ensure_post(post_id)

        # doar owner sau moderator pot vedea pending
        if post.circle_id:
            role = await self.circle_repo.get_user_role(post.circle_id, current_user.id)
            if role not in (CircleRole.OWNER, CircleRole.MODERATOR):
                raise HTTPException(403, "Not allowed")

        comments = await self.post_repo.get_comments_for_post(post_id, status="pending")

        responses = []
        for c in comments:
            user = await self.user_repo.get_by_id(c.user_id)
            responses.append(
                CommentResponse(
                    id=c.id,
                    post_id=c.post_id,
                    user_id=c.user_id,
                    username=user.username if user else None,
                    content=c.content,
                    status=c.status,
                    created_at=c.created_at,
                )
            )

        return responses
