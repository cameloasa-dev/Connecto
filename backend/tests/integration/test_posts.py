# backend/tests/integration/test_posts.py
"""
Integration tests for Post endpoints.
"""

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
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    return user


# ------------------------------------------------------
# FIXTURE: circle with owner
# ------------------------------------------------------
@pytest_asyncio.fixture
async def circle(db_session: AsyncSession, owner: User) -> Circle:
    c = Circle(
        name="PostsCircle",
        description="Circle for posts",
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
# 1. CREATE POST
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_create_post_in_circle(client: AsyncClient, circle: Circle):
    response = await client.post(
        "/posts/",
        json={
            "title": "Hello",
            "content": "World",
            "circle_id": circle.id,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Hello"
    assert data["circle_id"] == circle.id


@pytest.mark.asyncio
async def test_create_post_not_member_forbidden(client: AsyncClient, user2: User, circle: Circle):
    # Login user2 (not a member)
    login = await client.post(
        "/auth/login",
        json={"username": "user2", "password": "pass"},
    )
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    response = await client.post(
        "/posts/",
        json={
            "title": "Hack",
            "content": "Nope",
            "circle_id": circle.id,
        },
    )

    assert response.status_code == 403


# ------------------------------------------------------
# 2. GET POST
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_get_post(client: AsyncClient, circle: Circle):
    # Create post
    create = await client.post(
        "/posts/",
        json={"title": "Test", "content": "Content", "circle_id": circle.id},
    )
    post_id = create.json()["id"]

    response = await client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.asyncio
async def test_get_post_forbidden_not_member(client: AsyncClient, user2: User, circle: Circle):
    # Create post as owner
    create = await client.post(
        "/posts/",
        json={"title": "Secret", "content": "Hidden", "circle_id": circle.id},
    )
    post_id = create.json()["id"]

    # Login outsider
    login = await client.post(
        "/auth/login",
        json={"username": "user2", "password": "pass"},
    )
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    response = await client.get(f"/posts/{post_id}")
    assert response.status_code == 403


# ------------------------------------------------------
# 4. DELETE POST
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_delete_post_author(client: AsyncClient, circle: Circle):
    # Create post
    create = await client.post(
        "/posts/",
        json={"title": "DeleteMe", "content": "Bye", "circle_id": circle.id},
    )
    post_id = create.json()["id"]

    response = await client.delete(f"/posts/{post_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_post_forbidden_not_author_or_mod(
    client: AsyncClient, circle: Circle, user2: User
):
    # Create post as owner
    create = await client.post(
        "/posts/",
        json={"title": "Protected", "content": "Nope", "circle_id": circle.id},
    )
    post_id = create.json()["id"]

    # Login outsider
    login = await client.post(
        "/auth/login",
        json={"username": "user2", "password": "pass"},
    )
    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    response = await client.delete(f"/posts/{post_id}")
    assert response.status_code == 403


# ------------------------------------------------------
# 5. GET POSTS FROM CIRCLE
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_get_circle_posts(client: AsyncClient, circle: Circle):
    await client.post("/posts/", json={"title": "X", "content": "1", "circle_id": circle.id})
    await client.post("/posts/", json={"title": "Y", "content": "2", "circle_id": circle.id})

    response = await client.get(f"/posts/circle/{circle.id}")
    assert response.status_code == 200

    posts = response.json()
    assert len(posts) >= 2
    assert posts[0]["circle_id"] == circle.id
