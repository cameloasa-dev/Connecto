import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_auth_flow(client: AsyncClient) -> None:
    """
    Full authentication flow:
    1. Register
    2. Login (JWT/session_token in JSON)
    3. Login with session cookie
    4. Logout
    """

    username = "fullflowuser"
    password = "SecurePass123!"

    # 1. Register
    register_response = await client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "email": "fullflow@example.com",
        },
    )
    assert register_response.status_code == 201

    # 2. Login (default mode → returns session_token in JSON)
    jwt_response = await client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )
    assert jwt_response.status_code == 200

    jwt_data = jwt_response.json()
    assert "session_token" in jwt_data

    # 3. Login with session mode (cookie)
    session_response = await client.post(
        "/auth/login?use_session=true",
        json={"username": username, "password": password},
    )
    assert session_response.status_code == 200

    session_token = session_response.cookies.get("session_token")
    assert session_token is not None

    # 4. Logout
    logout_response = await client.post(
        "/auth/logout",
        cookies={"session_token": session_token},
    )

    assert logout_response.status_code == 200
    assert logout_response.json()["success"] is True
