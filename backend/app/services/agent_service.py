# AgentService
#       │
#       ├── AgentRepository
#       ├── ConversationRepository
#       └── MessageRepository

# The service will become the orchestrator:

# Find the agent.
# Create or load a conversation.
# Save the user's message.
# Load conversation history.
# Send history to Gemini.
# Save Gemini's reply.
# Return the response.

from uuid import UUID

from app.llm.embedding_service import EmbeddingService
from app.models.message import Message
from app.models.conversation import Conversation
from app.models.agent import Agent
from app.models.user import User
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.agent_repository import AgentRepository
from app.schemas.agent import AgentCreate, AgentUpdate

from app.llm.gemini_provider import GeminiProvider
from app.llm.service import LLMService
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

from collections.abc import AsyncGenerator


class AgentService:
    """Business logic for Agent operations."""

    def __init__(
        self,
        agent_repository: AgentRepository,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        chunk_repository: ChunkRepository,
    ):
        self.agent_repository = agent_repository
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.chunk_repository = chunk_repository

        provider = GeminiProvider()
        self.llm_service = LLMService(provider)
        self.embedding_service = EmbeddingService()

    async def create_agent(
        self,
        agent_data: AgentCreate,
        current_user: User,
    ) -> Agent:
        """Create a new agent for the authenticated user."""

        agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            model=agent_data.model,
            owner_id=current_user.id,  # the frontend never gets to choose theowner.
        )

        print(type(self.agent_repository))
        print(self.agent_repository)
        return await self.agent_repository.create_agent(agent)

    async def get_my_agents(
        self,
        current_user: User,
    ) -> list[Agent]:
        """Return all agents owned by the current user."""

        return await self.agent_repository.get_agents_by_owner(
            current_user.id,
        )

    async def get_agent_by_id(
        self,
        agent_id: UUID,
        current_user: User,
    ) -> Agent:
        """Return a single agent owned by the authenticated user."""

        agent = await self.agent_repository.get_agent_by_id(agent_id)

        if agent is None:
            raise ValueError("Agent not found.")

        if agent.owner_id != current_user.id:
            raise ValueError("You do not have permission to access this agent.")

        return agent

    async def update_agent(
        self,
        agent_id: UUID,
        agent_data: AgentUpdate,
        current_user: User,
    ) -> Agent:
        """Update an existing agent."""

        agent = await self.get_agent_by_id(
            agent_id,
            current_user,
        )

        if agent_data.name is not None:
            agent.name = agent_data.name

        if agent_data.description is not None:
            agent.description = agent_data.description

        if agent_data.model is not None:
            agent.model = agent_data.model

        return await self.agent_repository.update_agent(agent)

    async def delete_agent(
        self,
        agent_id,
        current_user: User,
    ) -> None:
        """Delete an existing agent."""

        agent = await self.get_agent_by_id(
            agent_id,
            current_user,
        )

        await self.agent_repository.delete_agent(agent)

    async def chat_with_agent(
        self,
        agent_id: UUID,
        message: str,
        current_user: User,
        conversation_id: UUID | None = None,
    ) -> tuple[UUID, str]:
        """Chat with an AI agent, while maintaining conversation history."""

        agent = await self.get_agent_by_id(
            agent_id,
            current_user,
        )

        # Create/ load conversation history
        if conversation_id is None:
            conversation = Conversation(
                agent_id=agent.id,
            )
            conversation = await self.conversation_repository.create_conversation(
                conversation,
            )
        else:
            conversation = (
                await self.conversation_repository.get_conversation_by_id(
                    conversation_id,
                )
            )

            if conversation is None:
                raise ValueError("Conversation not found.")

        # save user msg
        await self.message_repository.create_message(
            Message(
                conversation_id=conversation.id,
                role="user",
                content=message,
            )
        )

        # load history
        history = await self.message_repository.get_conversation_messages(
            conversation.id,
        )

        query_embedding = await self.embedding_service.embed(message)

        relevant_chunks = await self.chunk_repository.search_similar_chunks(
            agent_id=agent.id,
            query_embedding=query_embedding,
            limit=5,
        )

        document_context = "\n\n".join(
            chunk.content for chunk in relevant_chunks
        )

        # Build prompt
        prompt = f"You are {agent.name}\n\n"

        if document_context:
            prompt += (
                "Use the following document context when answering."
                "If the answer is not in the context, say that clearly.\n\n"
                f"Document context:\n{document_context}\n\n"
            )

        if agent.description:
            prompt += f"{agent.description}\n\n"

        prompt += "Conversation:\n"

        for msg in history:
            prompt += f"{msg.role}: {msg.content}\n"

        # generate AI response
        ai_response = await self.llm_service.generate_response(prompt)

        # save assistant msg
        await self.message_repository.create_message(
            Message(
                conversation_id=conversation.id,
                role="assistant",
                content=ai_response,
            )
        )

        return conversation.id, ai_response


    async def stream_chat_with_agent(
        self,
        agent_id: UUID,
        message: str,
        current_user: User,
        conversation_id: UUID | None = None,
    ) -> AsyncGenerator[str, None]:
        """Chat with an AI agent, while maintaining conversation history."""

        agent = await self.get_agent_by_id(
            agent_id,
            current_user,
        )

        # Create/ load conversation history
        if conversation_id is None:
            conversation = Conversation(
                agent_id=agent.id,
            )
            conversation = await self.conversation_repository.create_conversation(
                conversation,
            )
        else:
            conversation = (
                await self.conversation_repository.get_conversation_by_id(
                    conversation_id,
                )
            )

            if conversation is None:
                raise ValueError("Conversation not found.")

        # save user msg
        await self.message_repository.create_message(
            Message(
                conversation_id=conversation.id,
                role="user",
                content=message,
            )
        )

        # load history
        history = await self.message_repository.get_conversation_messages(
            conversation.id,
        )

        query_embedding = await self.embedding_service.embed(message)

        relevant_chunks = await self.chunk_repository.search_similar_chunks(
            agent_id=agent.id,
            query_embedding=query_embedding,
            limit=5,
        )

        document_context = "\n\n".join(
            chunk.content for chunk in relevant_chunks
        )

        # Build prompt
        prompt = f"You are {agent.name}\n\n"

        if document_context:
            prompt += (
        "Use the following document context when answering. "
        "If the answer is not in the context, say that clearly.\n\n"
        f"Document context:\n{document_context}\n\n"
        )

        if agent.description:
            prompt += f"{agent.description}\n\n"

        prompt += "Conversation:\n"

        for msg in history:
            prompt += f"{msg.role}: {msg.content}\n"

        # generate AI response
        full_response = ""

        async for chunk in self.llm_service.generate_stream(prompt):
            full_response += chunk
            yield chunk

        # save assistant msg
        await self.message_repository.create_message(
            Message(
                conversation_id=conversation.id,
                role="assistant",
                content=full_response,
            )
        )


# {
#   "id": "46b81e98-c1f8-41b4-a026-dd2a4af55ff4",
#   "name": "RAG Assistant",
#   "description": "Answers questions from uploaded documents",
#   "model": "gemini-3.5-flash",
#   "owner_id": "dd317514-e184-4602-91d1-aa0c5aa57d2b",
#   "created_at": "2026-08-06T05:00:58.312407Z",
#   "updated_at": "2026-08-06T05:00:58.312407Z"
# }
#  "id": "1068c8b3-83dd-4baa-ac0b-40b73aab31e3",

#   "name": "Research Assistant",

#   "description": "Helps answer questions and summarize documents",

#   "model": "gemini-3.5-flash",

#   "owner_id": "609632c8-f558-4be8-8b11-9d3f1639cba8",

#   "created_at": "2026-08-01T23:50:29.777139Z",

#   "updated_at": "2026-08-01T23:50:29.777139Z"

# # User Message
#       │
#       ▼
# Create Conversation (if new)
#       │
#       ▼
# Save User Message
#       │
#       ▼
# Load All Previous Messages
#       │
#       ▼
# Build Prompt
#       │
#       ▼
# Gemini
#       │
#       ▼
# Save Assistant Message
#       │
#       ▼
# Return Response
# "conversation_id": "85422d93-6ae0-4d13-968f-cb5b86a943da",
#   "response": "That's awesome! As your Research Assistant, I'd love to help you dive deeper into their content. \n\nIf you'd like, I can:\n1. **Summarize their videos** (if you paste a transcript or share the main points of a specific video).\n2. **Research topics** they frequently cover (like gaming, retro culture, or Star Wars/LEGO, depending on their latest focus).\n3. **Find similar creators** or recommendations based on what you enjoy about their channel.\n\nHow can I help you today?"
# }