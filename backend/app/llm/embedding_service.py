from google import genai

from app.core.config import settings


class EmbeddingService:
    """Generate vector embeddings using Gemini."""

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    async def embed(
            self,
            text: str,
    ) -> list[float]:
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        return response.embeddings[0].values
