from uuid import UUID
from sqlalchemy import select, delete

from app.models.chunk import Chunk
from sqlalchemy.ext.asyncio import AsyncSession


class ChunkRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create_chunk(
        self,
        chunk: Chunk,
    ) -> Chunk:

        self.db.add(chunk)

        await self.db.commit()

        await self.db.refresh(chunk)

        return chunk

    async def search_similar_chunks(
            self,
            agent_id: UUID,
            query_embedding: list[float],
            limit: int = 5,
    ) -> list[Chunk]:
        """Return the most relevant chunks for an agent."""

        result = await self.db.execute(
            select(Chunk)
            .join(Chunk.document)
            .where(
                Chunk.document.has(agent_id=agent_id),
                Chunk.embedding.is_not(None),
            )
            .order_by(
                Chunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        return list(result.scalars().all())

    async def delete_chunks_by_document(
            self,
            document_id: UUID,
    ) -> None:
        await self.db.execute(
            delete(Chunk).where(
                Chunk.document_id == document_id,
            )
        )

        await self.db.commit()
