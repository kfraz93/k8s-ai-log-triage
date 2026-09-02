from fastapi import APIRouter, HTTPException, status

from app.models.schemas import LogPayload, TriageResult
from app.services.llm_service import llm_service
from app.services.vector_service import vector_service

router = APIRouter(prefix="/api/v1", tags=["Triage"])


@router.post("/triage", response_model=TriageResult, status_code=status.HTTP_200_OK)
async def triage_log(payload: LogPayload):
    """RAG Triage Endpoint: Executes pgvector retrieval and LLM diagnosis."""
    try:
        matches = await vector_service.search_similar_logs(
            query_text=payload.error_message, limit=3
        )
        diagnosis = await llm_service.diagnose_log(
            error_message=payload.error_message,
            service_name=payload.service_name,
            matches=matches,
        )
        return TriageResult(
            query_log=payload, matched_incidents=matches, diagnosis=diagnosis
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Triage execution failed: {e!s}",
        )
