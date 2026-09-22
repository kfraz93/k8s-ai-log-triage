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


async def seed_database():
    """Seed initial log incidents for testing and development."""
    sample_logs = [
        {
            "service_name": "fastapi-backend",
            "error_message": "OOMKilled: Container memory limit exceeded (used 1024Mi, limit 512Mi)",
            "root_cause": "The container exceeded its memory limit due to unoptimized payload buffering in memory.",
            "remediation": "Increase container memory limits in deployment.yaml or stream large payloads in chunks.",
        },
        {
            "service_name": "analytics-processor",
            "error_message": "ConnectionTimeout: Failed to connect to PostgreSQL database pool after 30s",
            "root_cause": "Database connection pool exhaustion under heavy concurrent load.",
            "remediation": "Scale up connection pool max size or optimize long-running SQL transactions.",
        },
    ]

    conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        for log in sample_logs:
            # Generate vector embedding for the error message
            embedding = await vector_service.get_embedding(log["error_message"])
            vector_str = f"[{','.join(map(str, embedding))}]"

            await conn.execute(
                """
                INSERT INTO incident_logs (service_name, error_message, root_cause, remediation, embedding)
                VALUES ($1, $2, $3, $4, $5::vector)
                ON CONFLICT DO NOTHING
                """,
                log["service_name"],
                log["error_message"],
                log["root_cause"],
                log["remediation"],
                vector_str,
            )
        print("Database seeded successfully!")
    finally:
        await conn.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_database())
