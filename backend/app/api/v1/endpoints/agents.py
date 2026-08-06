from uuid import UUID

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.api.dependencies.services import get_agent_service, get_document_service
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.schemas.chat import ChatRequest, ChatResponse
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
    service: AgentService = Depends(get_agent_service),
):
    """Create a new AI agent."""

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
    service: AgentService = Depends(get_agent_service),
):
    """Return all agents belonging to the authenticated user."""

    return await service.get_my_agents(current_user)


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
async def get_agent_by_id(
    agent_id: UUID,
    current_user: User = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
):
    """Return a single agent owned by authenticated user."""

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
    service: AgentService = Depends(get_agent_service),
):
    """Update an existing agent."""

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
    service: AgentService = Depends(get_agent_service),
):
    """Delete an existing agent."""

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


@router.post(
    "/{agent_id}/chat",
    response_model=ChatResponse,
)
async def chat_with_agent(
    agent_id: UUID,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
):
    """Chat with an AI agent."""

    try:
        conversation_id, response = await service.chat_with_agent(
            agent_id=agent_id,
            message=chat_request.message,
            current_user=current_user,
            conversation_id=chat_request.conversation_id,
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=response,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{agent_id}/documents",
    response_model=DocumentResponse,
)
async def upload_document(
    agent_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):
    """Upload a document to an agent."""

    try:
        return await service.upload_document(
            agent_id,
            file,
            current_user,
        )

    except ValueError as e:
        detail = str(e)

        if detail == "Agent not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


@router.post(
    "/{agent_id}/chat/stream",
)
async def stream_chat_with_agent(
    agent_id: UUID,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
):
    try:

        stream = service.stream_chat_with_agent(
            agent_id=agent_id,
            message=chat_request.message,
            current_user=current_user,
            conversation_id=chat_request.conversation_id,
        )

        return StreamingResponse(
            stream,
            media_type="text/plain",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{agent_id}/documents",
    response_model=list[DocumentResponse],
)
async def get_agent_documents(
    agent_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):

    try:
        return await service.get_agent_documents(
            agent_id,
            current_user,
        )

    except ValueError as e:
        detail= str(e)

        if detail == "Agent not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):

    try:
        await service.delete_document(
            document_id,
            current_user,
        )

    except ValueError as e:
        detail = str(e)

        if detail in (
            "Document not found.",
            "Agent not found.",
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
