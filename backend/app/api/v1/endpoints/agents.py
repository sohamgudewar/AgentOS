from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.agent_repository import AgentRepository
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.services.agent_service import AgentService

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new AI agent."""

    repository = AgentRepository(db)
    service = AgentService(repository)

    return await service.create_agent(
        agent_data,
        current_user,
    )


@router.get(
    "",
    response_model=list[AgentResponse],
)
async def get_my_agents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return all agents belonging to the authenticated user."""

    repository = AgentRepository(db)
    service = AgentService(repository)

    return await service.get_my_agents(current_user)


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
async def get_agent_by_id(
    agent_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return a single agent owned by authenticated user."""

    repository = AgentRepository(db)
    service = AgentService(repository)

    try:
        return await service.get_agent_by_id(
            agent_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
)
async def update_agent(
    agent_id: UUID,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing agent."""

    repository = AgentRepository(db)
    service = AgentService(repository)

    try:
        return await service.update_agent(
            agent_id,
            agent_data,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_agent(
    agent_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an existing agent."""

    repository = AgentRepository(db)
    service = AgentService(repository)

    try:
        await service.delete_agent(
            agent_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
