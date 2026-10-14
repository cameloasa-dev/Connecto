from collections.abc import Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Circle, CircleMember


class CircleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================================================
    # CIRCLE CRUD
    # ==================================================

    async def create_circle(self, circle: Circle) -> Circle:
        self.db.add(circle)
        await self.db.flush()
        return circle

    async def get_circle_by_id(self, circle_id: int) -> Circle | None:
        return await self.db.get(Circle, circle_id)

    async def get_circle_with_members(self, circle_id: int) -> Circle | None:
        result = await self.db.execute(
            select(Circle)
            .where(Circle.id == circle_id)
            .options(selectinload(Circle.members))
        )
        return result.scalar_one_or_none()

    async def update_circle(self, circle: Circle) -> Circle:
        await self.db.commit()
        await self.db.refresh(circle)
        return circle

    async def delete_circle(self, circle: Circle) -> None:
        await self.db.delete(circle)
        await self.db.commit()

    async def circle_name_exists(self, name: str, exclude_id: int | None = None) -> bool:
        stmt = select(Circle).where(Circle.name == name)

        if exclude_id is not None:
            stmt = stmt.where(Circle.id != exclude_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    # ==================================================
    # MEMBERSHIP (RAW DB ONLY)
    # ==================================================

    async def add_member(self, member: CircleMember) -> CircleMember:
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def get_member(self, circle_id: int, user_id: int) -> CircleMember | None:
        result = await self.db.execute(
            select(CircleMember).where(
                CircleMember.circle_id == circle_id,
                CircleMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def is_member(self, circle_id: int, user_id: int) -> bool:
        return await self.get_member(circle_id, user_id) is not None

    async def user_is_owner_or_moderator(self, circle_id: int, user_id: int) -> bool:
        role = await self.get_user_role(circle_id, user_id)
        return role in ("owner", "moderator")

    async def get_user_role(self, circle_id: int, user_id: int) -> str | None:
        member = await self.get_member(circle_id, user_id)
        return member.role if member else None

    async def get_members(self, circle_id: int) -> Sequence[CircleMember]:
        result = await self.db.execute(
            select(CircleMember).where(CircleMember.circle_id == circle_id)
        )
        return result.scalars().all()

    async def get_member_user_ids(self, circle_id: int) -> list[int]:
        result = await self.db.execute(
            select(CircleMember.user_id).where(CircleMember.circle_id == circle_id)
        )
        return list(result.scalars().all())

    async def remove_member(self, member: CircleMember) -> None:
        await self.db.delete(member)
        await self.db.commit()

    async def update_member_role(self, member: CircleMember, new_role: str) -> CircleMember:
        member.role = new_role
        await self.db.commit()
        await self.db.refresh(member)
        return member

    # ==================================================
    # RELATIONS (NO BUSINESS LOGIC)
    # ==================================================

    async def get_user_circles_with_membership(
        self,
        user_id: int,
    ) -> Sequence[tuple[Circle, CircleMember]]:
        result = await self.db.execute(
            select(Circle, CircleMember)
            .join(CircleMember, Circle.id == CircleMember.circle_id)
            .where(CircleMember.user_id == user_id)
            .order_by(Circle.created_at.desc())
        )

        rows = result.all()
        return [(circle, member) for circle, member in rows]

    # ==================================================
    # SEARCH
    # ==================================================

    async def search_circles(self, term: str, limit: int, offset: int) -> Sequence[Circle]:
        pattern = f"%{term}%"

        result = await self.db.execute(
            select(Circle)
            .where(
                or_(
                    Circle.name.ilike(pattern),
                    Circle.description.ilike(pattern),
                )
            )
            .order_by(Circle.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return result.scalars().all()
