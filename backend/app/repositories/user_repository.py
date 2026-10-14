from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, UserSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ======================================================
    # BASIC USER QUERIES
    # ======================================================

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email_case_insensitive(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(func.lower(User.email) == func.lower(email))
        )
        return result.scalar_one_or_none()

    async def add_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # ======================================================
    # LIST / SEARCH USERS
    # ======================================================

    # ======================================================
    # LIST USERS (BASIC)
    # ======================================================

    async def get_all_except(
        self,
        current_user_id: int,
        skip: int,
        limit: int,
    ) -> Sequence[User]:
        result = await self.db.execute(
            select(User)
            .where(User.id != current_user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ======================================================
    # SEARCH USERS (UNIFIED)
    # ======================================================

    async def search_users(
        self,
        term: str,
        *,
        limit: int = 20,
        offset: int = 0,
        current_user_id: int | None = None,
        exclude_ids: list[int] | None = None,
    ) -> Sequence[User]:

        stmt = select(User)

        # exclude current user if needed
        if current_user_id is not None:
            stmt = stmt.where(User.id != current_user_id)

        # exclude additional ids (e.g. circle members)
        if exclude_ids:
            stmt = stmt.where(User.id.not_in(exclude_ids))

        pattern = f"%{term}%"

        stmt = (
            stmt.where(
                or_(
                    User.username.ilike(pattern),
                    User.email.ilike(pattern),
                )
            )
            .order_by(User.username.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    # ======================================================
    # GET USERS BY IDS (BATCH)
    # ======================================================

    async def get_users_by_ids(
        self,
        user_ids: list[int],
    ) -> Sequence[User]:

        if not user_ids:
            return []

        result = await self.db.execute(
            select(User).where(User.id.in_(user_ids))
        )
        return result.scalars().all()


    # ======================================================
    # SESSIONS
    # ======================================================

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
