from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chatting with an agent."""

    message: str = Field(
        ...,
        min_length=1
        )

    conversation_id: UUID | None = None


class ChatResponse(BaseModel):
    """Response schema for chatting with an agent."""

    conversation_id: UUID

    response: str
