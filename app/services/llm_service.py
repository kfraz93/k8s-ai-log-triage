from ollama import AsyncClient

from app.core.config import settings
from app.models.schemas import IncidentDiagnosis, SimilarIncident


class LLMService:
    def __init__(self):
        self.ollama_client = AsyncClient(host=settings.OLLAMA_BASE_URL, timeout=120.0)

    async def diagnose_log(
        self, error_message: str, service_name: str, matches: list[SimilarIncident]
    ) -> IncidentDiagnosis:
        context_str = "\n".join(
            [
                f"- Historical Root Cause: {m.root_cause} | Remediation: {m.remediation}"
                for m in matches
            ]
        )

        prompt = f"""
You are an expert Kubernetes Reliability Engineer. Analyze this error log and match it against historical incidents.

Target Service: {service_name}
Target Error Log: {error_message}

Historical Incidents Context:
{context_str}

Return ONLY a JSON object matching this schema:
{{
    "root_cause": "Concise explanation of the cause",
    "confidence_score": 0.95,
    "recommended_remediation": "Clear resolution steps",
    "kubectl_command": "Exact diagnostic command"
}}
"""
        response = await self.ollama_client.generate(
            model=settings.LLM_MODEL, prompt=prompt, format="json"
        )

        return IncidentDiagnosis.model_validate_json(response["response"])


llm_service = LLMService()
