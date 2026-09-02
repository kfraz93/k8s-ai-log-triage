from pydantic import BaseModel, Field


class LogPayload(BaseModel):
    service_name: str = Field(..., examples=["postgres-db"])
    error_message: str = Field(
        ..., examples=["psycopg2.OperationalError: Connection refused"]
    )


class SimilarIncident(BaseModel):
    id: int
    service_name: str
    error_message: str
    root_cause: str
    remediation: str
    similarity_score: float


class IncidentDiagnosis(BaseModel):
    root_cause: str
    confidence_score: float
    recommended_remediation: str
    kubectl_command: str | None = None


class TriageResult(BaseModel):
    query_log: LogPayload
    matched_incidents: list[SimilarIncident]
    diagnosis: IncidentDiagnosis
