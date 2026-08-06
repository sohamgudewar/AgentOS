import asyncio

from app.database.session import AsyncSessionLocal
from app.llm.embedding_service import EmbeddingService
from app.repositories.chunk_repository import ChunkRepository


AGENT_ID = "46b81e98-c1f8-41b4-a026-dd2a4af55ff4"


async def main():
    embedding_service = EmbeddingService()

    query_embedding = await embedding_service.embed(
        "What is the green swarm project about?"
    )

    async with AsyncSessionLocal() as db:
        repository = ChunkRepository(db)

        chunks = await repository.search_similar_chunks(
            agent_id=AGENT_ID,
            query_embedding=query_embedding,
            limit=3,
        )

        for index, chunk in enumerate(chunks, start=1):
            print(f"\n--- Result {index} ---")
            print(chunk.content[:500])


asyncio.run(main())