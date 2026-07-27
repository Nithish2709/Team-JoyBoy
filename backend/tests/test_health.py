from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


async def test_general_health(client: AsyncClient) -> None:
    """General check: server is up and responding."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "PDS Sentinel AI Backend"


async def test_database_health_success(client: AsyncClient) -> None:
    """Database check: returns healthy when SELECT 1 succeeds."""
    response = await client.get("/api/v1/health/database")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


async def test_database_health_failure(client: AsyncClient, mock_db_session: AsyncMock) -> None:
    """Database check: returns 503 when an exception is raised."""
    mock_db_session.execute.side_effect = Exception("Database unreachable")

    response = await client.get("/api/v1/health/database")
    assert response.status_code == 503
    data = response.json()
    assert data["detail"]["status"] == "unhealthy"
    assert "Database unreachable" in data["detail"]["error"]


async def test_redis_health_success(client: AsyncClient) -> None:
    """Redis check: returns healthy when ping succeeds."""
    with patch("app.api.v1.endpoints.health.check_redis_health", return_value=True):
        response = await client.get("/api/v1/health/redis")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["redis"] == "connected"


async def test_redis_health_failure(client: AsyncClient) -> None:
    """Redis check: returns 503 when ping fails."""
    with patch("app.api.v1.endpoints.health.check_redis_health", return_value=False):
        response = await client.get("/api/v1/health/redis")
    assert response.status_code == 503
    data = response.json()
    assert data["detail"]["status"] == "unhealthy"
    assert data["detail"]["redis"] == "disconnected"
