import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_projects(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Proj User", "email": "proj@example.com", "password": "securepass123"},
    )
    login = await client.post(
        "/api/v1/auth/login/json",
        json={"email": "proj@example.com", "password": "securepass123"},
    )
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        "/api/v1/projects",
        json={"name": "Office Tower", "description": "Phase 1"},
        headers=headers,
    )
    assert create.status_code == 201
    assert create.json()["data"]["name"] == "Office Tower"

    listing = await client.get("/api/v1/projects", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["data"]["total"] >= 1
