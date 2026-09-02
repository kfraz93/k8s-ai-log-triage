import asyncio
import json
import os
import sys

import asyncpg
from ollama import AsyncClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings


async def seed_database():
    print("Connecting to database...")
    conn = await asyncpg.connect(settings.DATABASE_URL)
    ollama_client = AsyncClient(host=settings.OLLAMA_BASE_URL)

    seed_path = os.path.join(os.path.dirname(__file__), "seed_data.json")

    def read_json_file(path: str):
        with open(path, "r") as f:
            return json.load(f)

    logs = await asyncio.to_thread(read_json_file, seed_path)

    try:
        # Clear existing entries to prevent duplicate rows on re-runs
        await conn.execute("TRUNCATE TABLE incident_logs;")

        print(f"Generating embeddings for {len(logs)} incident logs...")

        for item in logs:
            combined_text = f"Service: {item['service_name']} | Error: {item['error_message']} | Cause: {item['root_cause']}"

            response = await ollama_client.embeddings(
                model=settings.EMBED_MODEL, prompt=combined_text
            )

            # Use json.dumps for clean vector string formatting
            vector_str = json.dumps(response.embedding)

            await conn.execute(
                """
                INSERT INTO incident_logs (service_name, error_message, root_cause, remediation, embedding)
                VALUES ($1, $2, $3, $4, $5::vector)
                """,
                item["service_name"],
                item["error_message"],
                item["root_cause"],
                item["remediation"],
                vector_str,
            )
            print(f"Successfully seeded: {item['service_name']}")

    finally:
        # Always close connection, even if embedding or database insertion fails
        await conn.close()
        print("Database connection closed. Seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
