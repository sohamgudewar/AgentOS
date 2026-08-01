from uuid import UUID

from app.models.agent import Agent
from app.models.user import User
from app.repositories.agent_repository import AgentRepository
from app.schemas.agent import AgentCreate
from app.schemas.agent import AgentUpdate


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


# # recent error
# (backend) PS C:\Users\soham\OneDrive\Desktop\AgentOS\backend> uv run uvicorn app.main:app --reload
# INFO:     Will watch for changes in these directories: ['C:\\Users\\soham\\OneDrive\\Desktop\\AgentOS\\backend']
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [18572] using StatReload
# 2026-08-01 11:45:41 | INFO     | app.main:<module>:16 - AgentOS backend app is starting...
# INFO:     Started server process [14956]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     127.0.0.1:53212 - "GET /docs HTTP/1.1" 200 OK
# INFO:     127.0.0.1:53212 - "GET /openapi.json HTTP/1.1" 200 OK
# INFO:     127.0.0.1:63226 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
# INFO:     127.0.0.1:58993 - "PUT /api/v1/agents/6c75760c-b85e-411f-b194-6d39cfe6ab37 HTTP/1.1" 500 Internal Server Error
# ERROR:    Exception in ASGI application
# Traceback (most recent call last):
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 416, in run_asgi
#     result = await app(  # type: ignore[func-returns-value]
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 63, in __call__
#     return await self.app(scope, receive, send)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\applications.py", line 1163, in __call__
#     await super().__call__(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
#     await self.middleware_stack(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
#     raise exc
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
#     await self.app(scope, receive, _send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
#     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
#     raise exc
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
#     await app(scope, receive, sender)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
#     await self.app(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
#     await self.middleware_stack(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 2683, in app
#     await route.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1753, in handle
#     await self.original_router.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 2738, in handle
#     await included_router._handle_selected(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1764, in _handle_selected
#     await route.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1753, in handle
#     await self.original_router.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 2738, in handle
#     await included_router._handle_selected(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1764, in _handle_selected
#     await route.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1753, in handle
#     await self.original_router.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 2738, in handle
#     await included_router._handle_selected(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1773, in _handle_selected
#     await original_route.handle(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 1264, in handle
#     await app(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 150, in app
#     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
#     raise exc
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
#     await app(scope, receive, sender)
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 136, in app
#     response = await f(request)
#                ^^^^^^^^^^^^^^^^
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 690, in app
#     raw_response = await run_endpoint_function(
#                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\.venv\Lib\site-packages\fastapi\routing.py", line 344, in run_endpoint_function
#     return await dependant.call(**values)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\soham\OneDrive\Desktop\AgentOS\backend\app\api\v1\endpoints\agents.py", line 99, in update_agent
#     return await service.update_agent(
#                  ^^^^^^^^^^^^^^^^^^^^^
# TypeError: AgentService.update_agent() missing 2 required positional arguments: 'agent_data' and 'current_user'
