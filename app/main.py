from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1.triage import router as triage_router

app = FastAPI(
    title="k8s-ai-log-triage",
    description="AI-Powered Kubernetes Log Triage & Anomaly Service",
    version="1.0.0",
)

# Mount infrastructure and API routers separately
app.include_router(health_router)
app.include_router(triage_router)
