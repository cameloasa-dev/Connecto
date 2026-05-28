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
    user = await create_test_user("owner_dash", "password123")

    login = await client.post(
        "/auth/login",
        json={"username": "owner_dash", "password": "password123"},
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
        name="DashboardCircle",
        description="Circle for dashboard test",
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
# TEST: DASHBOARD ENDPOINT
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_dashboard(client: AsyncClient, circle: Circle):
    # Create some posts
    await client.post(
        "/posts/",
        json={"title": "Hello", "content": "World", "circle_id": circle.id},
    )
    await client.post(
        "/posts/",
        json={"title": "Another", "content": "Post", "circle_id": circle.id},
    )

    # Call dashboard
    response = await client.get("/dashboard")
    assert response.status_code == 200

    data = response.json()

    # Validate structure
    assert "user" in data
    assert "circles" in data
    assert "feed" in data
    assert "stats" in data

    # Validate user info
    assert data["user"]["id"] is not None
    assert data["user"]["username"] == "owner_dash"

    # Validate circles
    assert len(data["circles"]) == 1
    assert data["circles"][0]["id"] == circle.id

    # Validate feed
    assert len(data["feed"]) >= 2
    titles = [p["title"] for p in data["feed"]]
    assert "Hello" in titles
    assert "Another" in titles

    # Validate stats
    assert data["stats"]["total_circles"] == 1
    assert data["stats"]["total_posts_in_feed"] >= 2
