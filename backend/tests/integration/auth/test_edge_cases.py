import pytest
from httpx import AsyncClient

# ============================================================================
# USERNAME CASE SENSITIVITY
# ============================================================================


@pytest.mark.asyncio
async def test_username_case_sensitivity(client: AsyncClient) -> None:
    # Register with uppercase username
    await client.post(
        "/auth/register",
        json={
            "email": "casesensitive@example.com",
            "username": "CaseSensitive",
            "password": "Pass123!",
        },
    )

    # Login with lowercase username → should fail
    response = await client.post(
        "/auth/login",
        json={"username": "casesensitive", "password": "Pass123!"},
    )

    assert response.status_code == 401


# ============================================================================
# SPECIAL CHARACTERS IN USERNAME
# ============================================================================


@pytest.mark.asyncio
async def test_special_characters_in_username(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "email": "special@example.com",
            "username": "user_test-123",
            "password": "Pass123!",
        },
    )

    # Should succeed (underscores + hyphens allowed)
    assert response.status_code == 201


# ============================================================================
# USERNAME LENGTH LIMITS
# ============================================================================


@pytest.mark.asyncio
async def test_username_length_limits(client: AsyncClient) -> None:
    long_username = "a" * 51  # >50 chars

    response = await client.post(
        "/auth/register",
        json={
            "email": "long@example.com",
            "username": long_username,
            "password": "Pass123!",
        },
    )

    # Depending on your schema: 400 (custom) or 422 (Pydantic)
    assert response.status_code in [400, 422]
