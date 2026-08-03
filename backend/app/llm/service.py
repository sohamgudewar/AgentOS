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
        prompt: str
    ) -> str:
        """Generate a response from the LLM provider, based on the given prompt."""

        return await self.provider.generate(prompt)
