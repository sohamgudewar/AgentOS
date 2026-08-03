from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base interface for all LLM providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str
    ) -> str:
        """Generate a response from LLM, based on the given prompt."""
        pass
