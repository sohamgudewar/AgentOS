from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    agent_id: UUID
    filename: str
    file_path: str
    content_type: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
