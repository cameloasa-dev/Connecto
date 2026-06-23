# backend/scripts/create_db.py
import asyncio

from app.db.database import Base, engine
from app.db.models import *  # noqa: F401,F403


async def create_database() -> None:
    print("🛠️ Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created")


if __name__ == "__main__":
    asyncio.run(create_database())
