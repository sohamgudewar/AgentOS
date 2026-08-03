from google import genai

from app.core.config import settings
from app.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider implementation."""

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    async def generate(
        self,
        prompt: str
    ) -> str:
        """Generate a response from Google Gemini LLM, based on the given prompt."""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        return response.text

# eddie
