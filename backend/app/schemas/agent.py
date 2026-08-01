# AgentCreate → used when creating an agent.
# AgentUpdate → used when editing an agent.
# AgentResponse → what the API returns.

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    """Schema for creating an agent."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    model: str = Field(..., max_length=100)


class AgentUpdate(BaseModel):
    """Schema for updating an agent."""

    name: str | None = None
    description: str | None = None
    model: str | None = None


class AgentResponse(BaseModel):
    """Schema returned to the client."""

    id: UUID
    name: str
    description: str | None
    model: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
