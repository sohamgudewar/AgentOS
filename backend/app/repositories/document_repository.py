from sqlalchemy.ext.asyncio import AsyncSession

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
