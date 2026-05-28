# backend/tests/integration/test_users.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circle, CircleMember, User
from app.schemas.social import CircleRole


# ------------------------------------------------------
# FIXTURE: create owner + login + attach session cookie
# ------------------------------------------------------
@pytest_asyncio.fixture
async def test_owner(create_test_user, client: AsyncClient) -> User:
    user = await create_test_user("owner", "password123")

    # Login
    login_response = await client.post(
        "/auth/login",
        json={"username": "owner", "password": "password123"},
    )
    assert login_response.status_code == 200

    session_token = login_response.json().get("session_token")
    assert session_token is not None

    # Set cookie on client
    client.cookies.set("session_token", session_token)

    user.session_token = session_token
    return user


# ------------------------------------------------------
# FIXTURE: create 3 users (user0, user1, user2)
# ------------------------------------------------------
@pytest_asyncio.fixture
async def test_users(create_test_user) -> list[User]:
    users = []
    for i in range(3):
        user = await create_test_user(f"user{i}", "password123")
        users.append(user)
    return users


# ------------------------------------------------------
# FIXTURE: create circle with owner + user0 as member
# ------------------------------------------------------
@pytest_asyncio.fixture
async def test_circle(
    db_session: AsyncSession,
    test_owner: User,
    test_users: list[User],
) -> Circle:
    circle = Circle(
        name="Test Circle",
        description="For testing",
        owner_id=test_owner.id,
    )
    db_session.add(circle)
    await db_session.flush()

    # Owner as OWNER
    db_session.add(
        CircleMember(
            circle_id=circle.id,
            user_id=test_owner.id,
            role=CircleRole.OWNER,
        )
    )

    # user0 as MEMBER
    db_session.add(
        CircleMember(
            circle_id=circle.id,
            user_id=test_users[0].id,
            role=CircleRole.MEMBER,
        )
    )

    await db_session.commit()
    await db_session.refresh(circle)
    return circle


# ------------------------------------------------------
# TEST: search by username
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_search_users_by_username(
    client: AsyncClient,
    test_circle: Circle,
    test_owner: User,
):
    response = await client.get(f"/users/search?query=user&circle_id={test_circle.id}")

    assert response.status_code == 200
    results = response.json()

    # user0 is member → must be excluded
    # user1 and user2 → must be returned
    assert len(results) == 2

    for result in results:
        assert result["is_already_member"] is False
        assert "user" in result["username"]


# ------------------------------------------------------
# TEST: empty query → empty list
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_search_users_empty_query(
    client: AsyncClient,
    test_circle: Circle,
    test_owner: User,
):
    response = await client.get(f"/users/search?query=&circle_id={test_circle.id}")

    assert response.status_code == 200
    assert response.json() == []


# ------------------------------------------------------
# TEST: no results
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_search_users_no_results(
    client: AsyncClient,
    test_circle: Circle,
    test_owner: User,
):
    response = await client.get(f"/users/search?query=nonexistent&circle_id={test_circle.id}")

    assert response.status_code == 200
    assert response.json() == []


# ------------------------------------------------------
# TEST: invalid circle → 403
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_search_users_circle_not_found(
    client: AsyncClient,
    test_owner: User,
):
    # cookie already set by test_owner fixture
    response = await client.get("/users/search?query=user&circle_id=99999")

    assert response.status_code == 403
