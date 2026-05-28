import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User


@pytest.mark.asyncio
async def test_password_hashing(client: AsyncClient, db_session: AsyncSession) -> None:
    # Register user
    await client.post(
        "/auth/register",
        json={
            "email": "hash@example.com",
            "username": "hashtest",
            "password": "SecurePass123!",
        },
    )

    # Fetch user from DB
    result = await db_session.execute(
        select(User).where(User.username == "hashtest")
    )
    user = result.scalar_one()

    # Password must be hashed
    assert user.hashed_password != "SecurePass123!"
    assert user.hashed_password.startswith("$argon2")
