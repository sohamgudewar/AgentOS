# message_repository.py
# manages messages of Save and retrieve msgs from DBs

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageRepository:
    """Repository for Message database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(
        self,
        message: Message,
    ) -> Message:
        """Save a message to DB."""

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def get_conversation_messages(
        self,
        conversation_id: UUID,
    ) -> list[Message]:
        """Return all messages in a conversation."""

        result = await self.db.execute(
            select(Message).where(
                Message.conversation_id == conversation_id,
            )
            .order_by(Message.created_at)
        )

        return list(result.scalars().all())
