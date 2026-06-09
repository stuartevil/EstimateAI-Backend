import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_drawings_empty(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Draw User", "email": "draw@example.com", "password": "securepass123"},
    )
    login = await client.post(
        "/api/v1/auth/login/json",
        json={"email": "draw@example.com", "password": "securepass123"},
    )
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = await client.post(
        "/api/v1/projects", json={"name": "Drawing Project"}, headers=headers
    )
    project_id = project.json()["data"]["id"]

    response = await client.get(f"/api/v1/drawings/projects/{project_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"] == []
