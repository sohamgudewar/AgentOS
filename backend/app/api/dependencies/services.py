from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.database.session import get_db
from app.repositories.agent_repository import AgentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.agent_service import AgentService


def get_agent_service(
    db: AsyncSession = Depends(get_db),
) -> AgentService:
    return AgentService(
        agent_repository=AgentRepository(db),
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
        chunk_repository=ChunkRepository(db),
    )

def get_document_service(
    db: AsyncSession = Depends(get_db),
) -> DocumentService:
    return DocumentService(
        document_repository=DocumentRepository(db),
        chunk_repository=ChunkRepository(db),
        agent_repository=AgentRepository(db),
    )