import asyncpg
from ollama import AsyncClient

from app.core.config import settings
from app.models.schemas import SimilarIncident


class VectorService:
    def __init__(self):
        self.ollama_client = AsyncClient(host=settings.OLLAMA_BASE_URL)

    async def get_embedding(self, text: str) -> list[float]:
        response = await self.ollama_client.embeddings(
            model=settings.EMBED_MODEL, prompt=text
        )
        return response["embedding"]

    async def search_similar_logs(
        self, query_text: str, limit: int = 3
    ) -> list[SimilarIncident]:
        query_vector = await self.get_embedding(query_text)
        vector_str = f"[{','.join(map(str, query_vector))}]"

        conn = await asyncpg.connect(settings.DATABASE_URL)
        try:
            rows = await conn.fetch(
                """
                SELECT id, service_name, error_message, root_cause, remediation,
                       (1 - (embedding <=> $1::vector)) AS similarity_score
                FROM incident_logs
                ORDER BY embedding <=> $1::vector ASC
                LIMIT $2
                """,
                vector_str,
                limit,
            )
            return [
                SimilarIncident(
                    id=row["id"],
                    service_name=row["service_name"],
                    error_message=row["error_message"],
                    root_cause=row["root_cause"],
                    remediation=row["remediation"],
                    similarity_score=float(row["similarity_score"]),
                )
                for row in rows
            ]
        finally:
            await conn.close()


vector_service = VectorService()
