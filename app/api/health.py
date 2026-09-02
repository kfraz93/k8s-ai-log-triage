import asyncpg
from fastapi import APIRouter, HTTPException, status

from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/healthz", status_code=status.HTTP_200_OK)
async def liveness_probe():
    """Kubernetes Liveness Probe: Verifies process is alive."""
    return {"status": "healthy"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_probe():
    """Kubernetes Readiness Probe: Verifies DB connectivity."""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        await conn.execute("SELECT 1")
        await conn.close()
        return {"status": "ready", "database": "connected"}
    except (asyncpg.PostgresError, OSError, TimeoutError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database readiness check failed: {e!s}",
        )
