from app.llm.base import LLMProvider


class LLMService:
    """Service for interacting with LLM providers."""

    def __init__(
        self,
        provider: LLMProvider,
    ):
        self.provider = provider

    async def generate_response(
        self,
        prompt: str,
    ) -> str:
        """Generate a complete response from the LLM provider."""
        return await self.provider.generate(prompt)

    async def generate_stream(
        self,
        prompt: str,
    ):
        """Stream a response from the LLM provider."""
        async for chunk in self.provider.generate_stream(prompt):
            yield chunk
