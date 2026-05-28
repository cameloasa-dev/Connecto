import pytest
from httpx import AsyncClient


# ============================================================================
# SESSION-BASED LOGIN
# ============================================================================

@pytest.mark.asyncio
async def test_login_session_mode(client: AsyncClient) -> None:
    # Register user
    await client.post(
        "/auth/register",
        json={
            "email": "session@example.com",
            "username": "sessionuser",
            "password": "SecurePass123!",
        },
    )

    # Login with session mode enabled
    response = await client.post(
        "/auth/login?use_session=true",
        json={"username": "sessionuser", "password": "SecurePass123!"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["username"] == "sessionuser"
    assert "session_token" in data
    assert "user" in data

    # Cookie must be set
    assert "session_token" in response.cookies
