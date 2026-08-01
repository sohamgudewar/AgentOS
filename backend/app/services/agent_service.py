from app.models.agent import Agent
from app.models.user import User
from app.repositories.agent_repository import AgentRepository
from app.schemas.agent import AgentCreate


class AgentService:
    """Business logic for Agent operations."""

    def __init__(
        self,
        agent_repository: AgentRepository,
    ):
        self.agent_repository = agent_repository

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
