import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_healthz_endpoint():
    """Verify that liveness probe returns 200 OK."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_ready_endpoint():
    """Verify that readiness probe successfully checks PostgreSQL connectivity."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready", "database": "connected"}


@pytest.mark.asyncio
async def test_triage_endpoint():
    """Verify end-to-end API HTTP request triggers RAG retrieval and diagnosis."""
    payload = {
        "service_name": "analytics-processor",
        "error_message": "OOMKilled: Container memory limit exceeded (used 1024Mi, limit 512Mi)",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/triage", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["query_log"]["service_name"] == payload["service_name"]
        assert len(data["matched_incidents"]) > 0
        assert "root_cause" in data["diagnosis"]
        assert 0.0 <= data["diagnosis"]["confidence_score"] <= 1.0
