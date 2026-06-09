"""Authentication flow tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient) -> None:
    """Verify user registration and login return valid tokens."""
    register_payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepass123",
    }

    register_response = await client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert register_data["success"] is True
    assert "access_token" in register_data["data"]
    assert register_data["data"]["user"]["email"] == "test@example.com"

    login_response = await client.post(
        "/api/v1/auth/login/json",
        json={"email": "test@example.com", "password": "securepass123"},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["success"] is True
    assert login_data["data"]["access_token"]


@pytest.mark.asyncio
async def test_duplicate_registration(client: AsyncClient) -> None:
    """Verify duplicate email registration returns conflict error."""
    payload = {
        "name": "Duplicate User",
        "email": "dup@example.com",
        "password": "securepass123",
    }
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["success"] is False
