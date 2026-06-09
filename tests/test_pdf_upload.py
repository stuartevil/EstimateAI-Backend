import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_invalid_file_type(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"name": "PDF User", "email": "pdf@example.com", "password": "securepass123"},
    )
    login = await client.post(
        "/api/v1/auth/login/json",
        json={"email": "pdf@example.com", "password": "securepass123"},
    )
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = await client.post(
        "/api/v1/projects", json={"name": "PDF Project"}, headers=headers
    )
    project_id = project.json()["data"]["id"]

    response = await client.post(
        f"/api/v1/drawings/projects/{project_id}/upload",
        headers=headers,
        files={"file": ("test.txt", b"not a pdf", "text/plain")},
    )
    assert response.status_code == 400
