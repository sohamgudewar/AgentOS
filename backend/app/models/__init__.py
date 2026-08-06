from app.models.user import User
from app.models.agent import Agent

# This ensures SQLAlchemy discovers the model when creating tables or generating migrations.

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.document import Document
from app.models.chunk import Chunk
