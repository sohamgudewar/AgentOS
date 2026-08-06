from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from app.models.document import Document


class DocumentRepository:
    """Repository for Document database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(
        self,
        document: Document,
    ) -> Document:
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)

        return document

    async def get_documents_by_agent(
            self,
            agent_id: UUID,
    ) -> list[Document]:
        result = await self.db.execute(
            select(Document).where(Document.agent_id == agent_id)
            .order_by(Document.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_document_by_id(
            self,
            document_id: UUID,
    ) -> Document | None:
        result = await self.db.execute(
            select(Document).where(
                Document.id == document_id,
            )
        )

        return result.scalar_one_or_none()


    async def delete_document(
            self,
            document: Document,
    ) -> None:
        await self.db.delete(document)
        await self.db.commit()
