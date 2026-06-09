import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_measurement(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Meas User", "email": "meas@example.com", "password": "securepass123"},
    )
    login = await client.post(
        "/api/v1/auth/login/json",
        json={"email": "meas@example.com", "password": "securepass123"},
    )
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project = await client.post(
        "/api/v1/projects", json={"name": "Meas Project"}, headers=headers
    )
    project_id = project.json()["data"]["id"]

    response = await client.post(
        f"/api/v1/measurements/projects/{project_id}",
        headers=headers,
        json={
            "measurement_type": "length",
            "label": "Wall A",
            "value": 12.5,
            "unit": "ft",
            "geometry": {"points": [[0, 0], [100, 0]]},
        },
    )
    assert response.status_code == 201
    assert response.json()["data"]["label"] == "Wall A"
