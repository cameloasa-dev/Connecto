# backend/tests/integration/test_circle_members.py
"""
Comprehensive tests for circle_members covering all CRUD operations and role-based permissions.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circle, CircleMember, User
from app.schemas.circles.circle_members import CircleRole


# ------------------------------------------------------
# FIXTURE: owner + login
# ------------------------------------------------------
@pytest_asyncio.fixture
async def owner(create_test_user, client: AsyncClient) -> User:
    user = await create_test_user("owner", "password123")

    login = await client.post(
        "/auth/login",
        json={"username": "owner", "password": "password123"},
    )
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    return user


# ------------------------------------------------------
# FIXTURE: circle with owner
# ------------------------------------------------------
@pytest_asyncio.fixture
async def circle(db_session: AsyncSession, owner: User) -> Circle:
    c = Circle(
        name="CircleMembersTest",
        description="Test circle",
        owner_id=owner.id,
    )
    db_session.add(c)
    await db_session.flush()

    db_session.add(
        CircleMember(
            circle_id=c.id,
            user_id=owner.id,
            role=CircleRole.OWNER,
        )
    )

    await db_session.flush()
    await db_session.refresh(c)
    return c


# ------------------------------------------------------
# FIXTURE: another user
# ------------------------------------------------------
@pytest_asyncio.fixture
async def user2(create_test_user) -> User:
    return await create_test_user("user2", "pass")


# ------------------------------------------------------
# 1. ADD MEMBER
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_add_member(client: AsyncClient, circle: Circle, user2: User):
    response = await client.post(
        f"/circles/{circle.id}/members",
        json={"user_id": user2.id},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["member"]["user_id"] == user2.id
    assert data["member"]["role"] == "member"


@pytest.mark.asyncio
async def test_add_member_already_exists(client: AsyncClient, circle: Circle, user2: User):
    # Add once
    await client.post(f"/circles/{circle.id}/members", json={"user_id": user2.id})

    # Add again
    response = await client.post(
        f"/circles/{circle.id}/members",
        json={"user_id": user2.id},
    )
    assert response.status_code == 400


# ------------------------------------------------------
# 2. REMOVE MEMBER
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_remove_member(client: AsyncClient, circle: Circle, user2: User):
    # Add member first
    await client.post(f"/circles/{circle.id}/members", json={"user_id": user2.id})

    response = await client.delete(f"/circles/{circle.id}/members/{user2.id}")

    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_remove_owner_forbidden(client: AsyncClient, circle: Circle, owner: User):
    response = await client.delete(f"/circles/{circle.id}/members/{owner.id}")
    assert response.status_code == 403


# ------------------------------------------------------
# 3. UPDATE ROLE
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_update_member_role(client: AsyncClient, circle: Circle, user2: User):
    # Add member
    await client.post(f"/circles/{circle.id}/members", json={"user_id": user2.id})

    response = await client.put(
        f"/circles/{circle.id}/members/{user2.id}/role",
        json={"role": "moderator"},
    )

    assert response.status_code == 200
    assert response.json()["member"]["role"] == "moderator"


@pytest.mark.asyncio
async def test_update_owner_role_forbidden(client: AsyncClient, circle: Circle, owner: User):
    response = await client.put(
        f"/circles/{circle.id}/members/{owner.id}/role",
        json={"role": "moderator"},
    )
    assert response.status_code == 403
