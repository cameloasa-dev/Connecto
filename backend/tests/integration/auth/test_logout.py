import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient) -> None:
    # Register user
    await client.post(
        "/auth/register",
        json={
            "email": "logout@example.com",
            "username": "logoutuser",
            "password": "SecurePass123!",
        },
    )

    # Login with session mode
    login_response = await client.post(
        "/auth/login?use_session=true",
        json={"username": "logoutuser", "password": "SecurePass123!"},
    )

    assert login_response.status_code == 200

    # Extract session cookie
    session_token = login_response.cookies.get("session_token")
    assert session_token is not None

    # Logout
    response = await client.post(
        "/auth/logout",
        cookies={"session_token": session_token},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "logged out" in data["message"].lower()
