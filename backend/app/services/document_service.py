from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.document_processing.extractor import DocumentExtractor
from app.document_processing.chunker import TextChunker
from app.models.chunk import Chunk
from app.llm.embedding_service import EmbeddingService


class DocumentService:
    """Business logic for document uploads."""

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.embedding_service = EmbeddingService()

    async def upload_document(
        self,
        agent_id,
        file: UploadFile,
    ) -> Document:

        upload_dir = Path("uploads/documents")
        upload_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid4()}_{file.filename}"
        file_path = upload_dir / filename

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        document = Document(
            agent_id=agent_id,
            filename=file.filename,
            file_path=str(file_path),
            content_type=file.content_type,
        )

        document = await self.document_repository.create_document(
            document,
        )

        text = DocumentExtractor.extract(
            str(file_path),
        )

        chunks = TextChunker.chunk_text(
            text,
        )

        for index, chunk_text in enumerate(chunks):
            embedding = await self.embedding_service.embed(chunk_text)

            chunk = Chunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk_text,
                embedding=embedding,
        )

        await self.chunk_repository.create_chunk(
            chunk,
        )

        return document
