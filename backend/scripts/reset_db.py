# backend/scripts/reset_db.py

import asyncio

from app.db.database import Base, engine


async def reset_database() -> None:
    """Drop all tables and recreate them."""
    print("🔄 Resetting database...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database reset complete")


if __name__ == "__main__":
    asyncio.run(reset_database())
