import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_full_integration_flow(client: AsyncClient, db_session: AsyncSession):
    # ------------------------------------------------------
    # 1. REGISTER USER
    # ------------------------------------------------------
    create_user = await client.post(
        "/auth/register",
        json={
            "username": "flow_user",
            "email": "flow@test.com",
            "password": "Abc123!!"
        },
    )
    assert create_user.status_code == 201

    # ------------------------------------------------------
    # 2. LOGIN
    # ------------------------------------------------------
    login = await client.post(
        "/auth/login",
        json={"username": "flow_user", "password": "Abc123!!"},
    )
    assert login.status_code == 200

    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    # ------------------------------------------------------
    # 3. CREATE CIRCLE
    # ------------------------------------------------------
    create_circle = await client.post(
        "/circles/",
        json={"name": "FlowCircle", "description": "Full flow test"},
    )
    assert create_circle.status_code == 201
    circle_id = create_circle.json()["id"]

    # ------------------------------------------------------
    # 4. CREATE POSTS (user is already OWNER by default)
    # ------------------------------------------------------
    p1 = await client.post(
        "/posts/",
        json={"title": "First", "content": "Post", "circle_id": circle_id},
    )
    assert p1.status_code == 201

    p2 = await client.post(
        "/posts/",
        json={"title": "Second", "content": "Post", "circle_id": circle_id},
    )
    assert p2.status_code == 201

    # ------------------------------------------------------
    # 5. DASHBOARD
    # ------------------------------------------------------
    dashboard = await client.get("/dashboard")
    assert dashboard.status_code == 200

    data = dashboard.json()

    # Validate user
    assert data["user"]["username"] == "flow_user"

    # Validate circles
    assert len(data["circles"]) == 1
    assert data["circles"][0]["id"] == circle_id

    # Validate feed
    titles = [p["title"] for p in data["feed"]]
    assert "First" in titles
    assert "Second" in titles

    # Validate stats
    assert data["stats"]["total_circles"] == 1
    assert data["stats"]["total_posts_in_feed"] == 2
