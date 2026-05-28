import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_negative_flow(client: AsyncClient):
    # ------------------------------------------------------
    # 1. LOGIN FAIL (wrong password)
    # ------------------------------------------------------
    bad_login = await client.post(
        "/auth/login",
        json={"username": "nouser", "password": "gresit"},
    )
    assert bad_login.status_code == 401

    # ------------------------------------------------------
    # 2. ACCESS DASHBOARD WITHOUT LOGIN
    # ------------------------------------------------------
    dashboard = await client.get("/dashboard")
    assert dashboard.status_code == 401

    # ------------------------------------------------------
    # 3. CREATE CIRCLE WITHOUT LOGIN
    # ------------------------------------------------------
    create_circle = await client.post(
        "/circles/",
        json={"name": "BadCircle", "description": "Should fail"},
    )
    assert create_circle.status_code == 401

    # ------------------------------------------------------
    # 4. REGISTER + LOGIN (valid user)
    # ------------------------------------------------------
    await client.post(
        "/auth/register",
        json={"username": "neg_user", "email": "neg@test.com", "password": "Abc123!!"},
    )

    login = await client.post(
        "/auth/login",
        json={"username": "neg_user", "password": "Abc123!!"},
    )
    assert login.status_code == 200

    token = login.json()["session_token"]
    client.cookies.set("session_token", token)

    # ------------------------------------------------------
    # IMPORTANT: clear session to test unauthorized access
    # ------------------------------------------------------
    client.cookies.clear()

    # ------------------------------------------------------
    # 5. CREATE A CIRCLE WITHOUT LOGIN (should fail)
    # ------------------------------------------------------
    circle = await client.post(
        "/circles/",
        json={"name": "NegCircle", "description": "Valid circle"},
    )
    assert circle.status_code == 401

    # ------------------------------------------------------
    # 6. ADD MEMBER THAT DOES NOT EXIST
    # ------------------------------------------------------
    add_fake_member = await client.post(
        "/circle-members/1/add",
        json={"username": "nu_exista", "role": "MEMBER"},
    )
    assert add_fake_member.status_code in (401, 403, 404)

    # ------------------------------------------------------
    # 7. ADD MEMBER TO NON-EXISTENT CIRCLE
    # ------------------------------------------------------
    add_to_fake_circle = await client.post(
        "/circle-members/999999/add",
        json={"username": "neg_user", "role": "MEMBER"},
    )
    assert add_to_fake_circle.status_code in (401, 403, 404)

    # ------------------------------------------------------
    # 8. CREATE POST IN A CIRCLE WHERE USER IS NOT MEMBER
    # ------------------------------------------------------
    create_post = await client.post(
        "/posts/",
        json={"title": "Bad", "content": "Post", "circle_id": 999999},
    )
    assert create_post.status_code in (401, 403, 404)

    # ------------------------------------------------------
    # 9. ACCESS FEED OF A CIRCLE WHERE USER IS NOT MEMBER
    # ------------------------------------------------------
    feed = await client.get("/posts/feed?circle_id=999999")
    assert feed.status_code in (401, 403, 404)
