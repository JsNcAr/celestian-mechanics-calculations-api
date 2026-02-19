import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_returns_200(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_root_response_shape(client: AsyncClient) -> None:
    response = await client.get("/")
    body = response.json()
    assert "message" in body
    assert "docs" in body
    assert "version" in body


@pytest.mark.asyncio
async def test_health_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_status_ok(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


@pytest.mark.asyncio
async def test_openapi_schema_available(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
