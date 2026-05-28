import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.models import User

# ============================================================================
# SUCCESSFUL LOGIN
# ============================================================================


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    # Register user
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "logintest",
            "password": "SecurePass123!",
        },
    )

    # Login
    response = await client.post(
        "/auth/login",
        json={"username": "logintest", "password": "SecurePass123!"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["username"] == "logintest"
    assert "session_token" in data


# ============================================================================
# WRONG PASSWORD
# ============================================================================


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    # Register user
    await client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "username": "wrongpass",
            "password": "CorrectPass123!",
        },
    )

    # Wrong password
    response = await client.post(
        "/auth/login",
        json={"username": "wrongpass", "password": "WrongPass123!"},
    )

    assert response.status_code == 401
    assert "invalid username or password" in response.json()["detail"].lower()


# ============================================================================
# NONEXISTENT USER
# ============================================================================


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/login",
        json={"username": "ghost", "password": "SomePass123!"},
    )

    assert response.status_code == 401
    assert "invalid username or password" in response.json()["detail"].lower()


# ============================================================================
# INACTIVE USER
# ============================================================================


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, db_session: AsyncSession) -> None:
    # Create inactive user directly in DB
    inactive = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password=get_password_hash("Pass123!"),
        is_active=False,
    )
    db_session.add(inactive)
    await db_session.commit()

    # Attempt login
    response = await client.post(
        "/auth/login",
        json={"username": "inactive", "password": "Pass123!"},
    )

    assert response.status_code == 403
    assert "inactive" in response.json()["detail"].lower()
