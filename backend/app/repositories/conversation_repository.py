# message_repository.py
# manages messages of create, get and list messages from DBs

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationRepository:
    """Repository for Conversation database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(
        self,
        conversation: Conversation,
    ) -> Conversation:
        """Create a new conversation."""

        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def get_conversation_by_id(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        """Get a conversation by its ID."""

        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_agent_conversations(
        self,
        agent_id: UUID,
    ) -> list[Conversation]:
        """Return all conversations for an agents."""

        result = await self.db.execute(
            select(Conversation).where(
                Conversation.agent_id == agent_id,
            )
        )

        return list(result.scalars().all())
