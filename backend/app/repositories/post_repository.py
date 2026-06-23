from collections.abc import Sequence

from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circle, Comment, Post, PostLike, User


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --------------------------------------------------
    # POSTS CRUD
    # --------------------------------------------------

    async def create_post(self, post: Post) -> Post:
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def get_post_by_id(self, post_id: int) -> Post | None:
        return await self.db.get(Post, post_id)

    async def update_post(self, post: Post) -> Post:
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def delete_post(self, post: Post) -> None:
        await self.db.delete(post)
        await self.db.commit()

    # --------------------------------------------------
    # POSTS WITH AUTHOR + CIRCLE
    # --------------------------------------------------

    async def get_post_with_author_and_circle(
        self, post_id: int
    ) -> tuple[Post, str, str | None] | None:

        result = await self.db.execute(
            select(Post, User.username, Circle.name)
            .join(User, Post.author_id == User.id)
            .join(Circle, Post.circle_id == Circle.id, isouter=True)
            .where(Post.id == post_id)
        )

        row = result.first()
        if not row:
            return None

        post, author_name, circle_name = row
        return post, author_name, circle_name

    # --------------------------------------------------
    # POSTS FOR CIRCLE (FEED)
    # --------------------------------------------------

    async def get_posts_for_circles(
        self, circle_ids: list[int], limit: int
    ) -> Sequence[tuple[Post, str, str | None]]:
        if not circle_ids:
            return []

        result = await self.db.execute(
            select(Post, User.username, Circle.name)
            .join(User, Post.author_id == User.id)
            .join(Circle, Post.circle_id == Circle.id, isouter=True)
            .where(Post.circle_id.in_(circle_ids))
            .order_by(desc(Post.created_at))
            .limit(limit)
        )

        rows = result.all()
        return [(row[0], row[1], row[2]) for row in rows]

    async def get_posts_for_circle(
        self, circle_id: int, limit: int, offset: int
    ) -> Sequence[tuple[Post, str]]:
        result = await self.db.execute(
            select(Post, User.username)
            .join(User, Post.author_id == User.id)
            .where(Post.circle_id == circle_id)
            .order_by(desc(Post.created_at))
            .offset(offset)
            .limit(limit)
        )
        rows = result.all()
        return [(row[0], row[1]) for row in rows]

    # --------------------------------------------------
    # LIKES
    # --------------------------------------------------

    async def has_liked(self, post_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(PostLike).where(
                PostLike.post_id == post_id,
                PostLike.user_id == user_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def add_like(self, post_id: int, user_id: int) -> None:
        like = PostLike(post_id=post_id, user_id=user_id)
        self.db.add(like)
        await self.db.commit()

    async def remove_like(self, post_id: int, user_id: int) -> None:
        result = await self.db.execute(
            select(PostLike).where(
                PostLike.post_id == post_id,
                PostLike.user_id == user_id,
            )
        )
        like = result.scalar_one_or_none()
        if like:
            await self.db.delete(like)
            await self.db.commit()

    async def count_likes(self, post_id: int) -> int:
        result = await self.db.execute(select(func.count()).where(PostLike.post_id == post_id))
        return result.scalar_one()

    # --------------------------------------------------
    # COMMENTS
    # --------------------------------------------------

    async def add_comment(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete_comment(self, comment: Comment) -> None:
        await self.db.delete(comment)
        await self.db.commit()

    async def get_comments_for_post(self, post_id: int) -> Sequence[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.asc())
        )
        return result.scalars().all()

    async def count_comments(self, post_id: int) -> int:
        result = await self.db.execute(select(func.count()).where(Comment.post_id == post_id))
        return result.scalar_one()

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------
    async def search_posts(
        self,
        term: str,
        circle_ids: list[int],
        limit: int,
        offset: int,
    ) -> Sequence[tuple[Post, str, str | None]]:
        if not circle_ids:
            return []

        pattern = f"%{term}%"

        result = await self.db.execute(
            select(Post, User.username, Circle.name)
            .join(User, Post.author_id == User.id)
            .join(Circle, Post.circle_id == Circle.id, isouter=True)
            .where(
                Post.circle_id.in_(circle_ids),
                or_(
                    Post.title.ilike(pattern),
                    Post.content.ilike(pattern),
                ),
            )
            .order_by(desc(Post.created_at))
            .offset(offset)
            .limit(limit)
        )

        rows = result.all()
        return [(row[0], row[1], row[2]) for row in rows]
