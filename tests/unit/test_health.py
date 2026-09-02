from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_healthz_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_ready_endpoint_unhealthy():
    """Verify /ready returns 503 when PostgreSQL is unreachable."""
    with patch(
        "app.api.health.asyncpg.connect", side_effect=OSError("Connection refused")
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/ready")
            assert response.status_code == 503
            assert "Database readiness check failed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_ready_endpoint_healthy():
    """Verify /ready returns 200 when database connection succeeds."""
    mock_conn = AsyncMock()
    mock_conn.execute.return_value = "SELECT 1"
    mock_conn.close.return_value = None

    with patch("app.api.health.asyncpg.connect", AsyncMock(return_value=mock_conn)):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/ready")
            assert response.status_code == 200
            assert response.json() == {"status": "ready", "database": "connected"}
