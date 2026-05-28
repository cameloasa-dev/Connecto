# backend/tests/integration/test_circles.py
"""
Integration tests for Circle endpoints.
"""

# backend/tests/integration/test_circles.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circle, CircleMember, User
from app.schemas.social import CircleRole


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
    assert login.status_code == 200

    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    user.session_token = token
    return user


# ------------------------------------------------------
# FIXTURE: create a circle for tests
# ------------------------------------------------------
@pytest_asyncio.fixture
async def circle(db_session: AsyncSession, owner: User) -> Circle:
    c = Circle(
        name="Test Circle",
        description="Circle for testing",
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
# CREATE CIRCLE
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_create_circle(client: AsyncClient, owner: User):
    response = await client.post(
        "/circles/",
        json={"name": "My Circle", "description": "Hello"},
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "My Circle"
    assert data["owner_id"] == owner.id
    assert data["member_count"] == 1
    assert data["members"][0]["role"] == "owner"


# ------------------------------------------------------
# CREATE CIRCLE - duplicate name
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_create_circle_duplicate_name(client: AsyncClient, owner: User):
    # First create
    await client.post("/circles/", json={"name": "Dup", "description": "x"})

    # Duplicate
    response = await client.post("/circles/", json={"name": "Dup", "description": "x"})
    assert response.status_code == 400


# ------------------------------------------------------
# GET MY CIRCLES
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_get_my_circles(client: AsyncClient, circle: Circle):
    response = await client.get("/circles/my")
    assert response.status_code == 200

    circles = response.json()
    assert len(circles) == 1
    assert circles[0]["id"] == circle.id
    assert circles[0]["member_count"] == 1


# ------------------------------------------------------
# GET CIRCLE BY ID
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_get_circle_by_id(client: AsyncClient, circle: Circle):
    response = await client.get(f"/circles/{circle.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == circle.id
    assert data["owner_id"] == circle.owner_id
    assert data["member_count"] == 1


# ------------------------------------------------------
# GET CIRCLE - forbidden for non-member
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_get_circle_forbidden(
    client: AsyncClient,
    create_test_user,
    db_session: AsyncSession,
    circle: Circle,
):
    # Create a new user who is NOT a member
    outsider = await create_test_user("outsider", "pass")

    # Login outsider
    login = await client.post(
        "/auth/login",
        json={"username": "outsider", "password": "pass"},
    )
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    response = await client.get(f"/circles/{circle.id}")
    assert response.status_code == 403


# ------------------------------------------------------
# UPDATE CIRCLE
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_update_circle(client: AsyncClient, circle: Circle):
    response = await client.put(
        f"/circles/{circle.id}",
        json={"name": "Updated", "description": "New desc"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Updated"
    assert data["description"] == "New desc"


# ------------------------------------------------------
# UPDATE CIRCLE - forbidden for non-owner
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_update_circle_forbidden(
    client: AsyncClient,
    create_test_user,
    db_session: AsyncSession,
    circle: Circle,
):
    # Create non-owner user
    user = await create_test_user("notowner", "pass")

    login = await client.post(
        "/auth/login",
        json={"username": "notowner", "password": "pass"},
    )
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    response = await client.put(
        f"/circles/{circle.id}",
        json={"name": "Hack", "description": "Hack"},
    )

    assert response.status_code == 403


# ------------------------------------------------------
# UPDATE CIRCLE NAME
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_update_circle_name(client: AsyncClient, circle: Circle):
    response = await client.put(
        f"/circles/{circle.id}/name",
        json={"name": "NewName"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "NewName"


# ------------------------------------------------------
# DELETE CIRCLE
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_delete_circle(client: AsyncClient, circle: Circle):
    response = await client.delete(f"/circles/{circle.id}")
    assert response.status_code == 204
