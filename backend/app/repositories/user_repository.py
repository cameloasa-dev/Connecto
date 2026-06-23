from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CircleMember, User, UserSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email_case_insensitive(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(func.lower(User.email) == func.lower(email))
        )
        return result.scalar_one_or_none()

    async def get_all_except(self, current_user_id: int, skip: int, limit: int) -> Sequence[User]:
        result = await self.db.execute(
            select(User).where(User.id != current_user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def search_by_username_excluding_ids(
        self,
        query: str,
        exclude_ids: list[int],
        current_user_id: int,
        limit: int = 20,
    ) -> Sequence[User]:
        stmt = (
            select(User)
            .where(
                User.id != current_user_id,
                User.username.ilike(f"%{query}%"),
            )
            .limit(limit)
        )

        if exclude_ids:
            stmt = stmt.where(User.id.not_in(exclude_ids))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_circle_member_ids(self, circle_id: int) -> list[int]:
        result = await self.db.execute(
            select(CircleMember.user_id).where(CircleMember.circle_id == circle_id)
        )
        return [row[0] for row in result.fetchall()]

    async def get_user_circle_role(self, circle_id: int, user_id: int) -> CircleMember | None:
        result = await self.db.execute(
            select(CircleMember).where(
                CircleMember.circle_id == circle_id,
                CircleMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    # --------------------------------------------------
    # Session
    # --------------------------------------------------
    async def create_session(self, session: UserSession) -> None:
        self.db.add(session)
        await self.db.commit()

    async def get_valid_session(self, session_token: str) -> UserSession | None:
        result = await self.db.execute(
            select(UserSession)
            .where(UserSession.session_token == session_token)
            .where(UserSession.expires_at > func.now())
        )
        return result.scalar_one_or_none()

    async def delete_session(self, session: UserSession) -> None:
        await self.db.delete(session)
        await self.db.commit()

    # --------------------------------------------------
    # Add user
    # --------------------------------------------------
    async def add_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------
    async def search_users(
        self,
        term: str,
        limit: int,
        offset: int,
    ) -> Sequence[User]:
        pattern = f"%{term}%"

        result = await self.db.execute(
            select(User)
            .where(
                or_(
                    User.username.ilike(pattern),
                    User.email.ilike(pattern),
                )
            )
            .order_by(User.username.asc())
            .offset(offset)
            .limit(limit)
        )

        return result.scalars().all()
