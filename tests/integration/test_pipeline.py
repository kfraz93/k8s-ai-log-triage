import pytest

from app.services.llm_service import llm_service
from app.services.vector_service import vector_service


@pytest.mark.asyncio
async def test_vector_similarity_search():
    test_error = "OOMKilled: Container memory limit exceeded (used 1024Mi, limit 512Mi)"

    matches = await vector_service.search_similar_logs(test_error, limit=2)

    assert len(matches) > 0
    assert matches[0].similarity_score > 0.5
    assert matches[0].service_name == "fastapi-backend"


@pytest.mark.asyncio
async def test_llm_diagnosis_generation():
    test_error = "OOMKilled: Container memory limit exceeded (used 1024Mi, limit 512Mi)"
    test_service = "analytics-processor"

    matches = await vector_service.search_similar_logs(test_error, limit=2)
    diagnosis = await llm_service.diagnose_log(
        error_message=test_error, service_name=test_service, matches=matches
    )

    assert diagnosis.root_cause != ""
    assert 0.0 <= diagnosis.confidence_score <= 1.0
    assert diagnosis.recommended_remediation != ""
    assert diagnosis.kubectl_command is not None
