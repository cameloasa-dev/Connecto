import pytest
from httpx import AsyncClient


# ============================================================================
# SUCCESSFUL REGISTRATION
# ============================================================================

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient) -> None:
    payload = {
        "username": "johndoe",
        "password": "SecurePass123!",
        "email": "john@example.com",
        "full_name": "John Doe",
    }

    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["success"] is True
    assert data["username"] == "johndoe"
    assert data["user"]["email"] == "john@example.com"
    assert "hashed_password" not in data["user"]


# ============================================================================
# MINIMAL REGISTRATION
# ============================================================================

@pytest.mark.asyncio
async def test_register_minimal_data(client: AsyncClient) -> None:
    payload = {
        "username": "minimaluser",
        "password": "SecurePass123!",
        "email": "minimal@example.com",
    }

    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["success"] is True
    assert data["user"]["email"] == "minimal@example.com"


# ============================================================================
# DUPLICATES
# ============================================================================

@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient) -> None:
    payload = {
        "username": "duplicate",
        "password": "SecurePass123!",
        "email": "dup1@example.com",
    }

    # First registration
    assert (await client.post("/auth/register", json=payload)).status_code == 201

    # Second registration with same username
    payload["email"] = "dup2@example.com"
    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {
        "username": "dupemail",
        "password": "SecurePass123!",
        "email": "duplicate@example.com",
    }

    # First registration
    assert (await client.post("/auth/register", json=payload)).status_code == 201

    # Second registration with same email
    payload["username"] = "dupemail2"
    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


# ============================================================================
# INVALID DATA
# ============================================================================

@pytest.mark.asyncio
async def test_register_invalid_data(client: AsyncClient) -> None:
    # Missing password
    response = await client.post("/auth/register", json={"username": "test"})
    assert response.status_code == 422

    # Missing username
    response = await client.post("/auth/register", json={"password": "pass"})
    assert response.status_code == 422
