from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent


class AgentRepository:
    """Repository for Agent database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_agent(
        self,
        agent: Agent,
    ) -> Agent:
        print(">>> create_agent called", self, agent)

        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)

        return agent

    async def get_agent_by_id(
        self,
        agent_id: UUID,
    ) -> Agent | None:
        """Get an agent by ID."""

        result = await self.db.execute(
            select(Agent).where(
                Agent.id == agent_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_agents_by_owner(
        self,
        owner_id: UUID,
    ) -> list[Agent]:
        """Get all agents owned by a user."""

        result = await self.db.execute(
            select(Agent).where(
                Agent.owner_id == owner_id,
            )
        )

        return list(result.scalars().all())

    async def update_agent(
        self,
        agent: Agent,
    ) -> Agent:
        """Update an existing agent."""

        await self.db.commit()
        await self.db.refresh(agent)

        return agent

    async def delete_agent(
        self,
        agent: Agent,
    ) -> None:
        """Delete an existing agent."""

        await self.db.delete(agent)
        await self.db.commit()
