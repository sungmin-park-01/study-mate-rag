from openai import OpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBEDDING_MODEL

    def create_embedding(self, text: str) -> list[float]:
        """
        Create a single embedding vector for the given text.

        This service keeps API key handling outside the application code
        and uses the model configured through environment variables.
        """
        clean_text = text.strip()

        if not clean_text:
            raise ValueError("Text for embedding cannot be empty.")

        response = self.client.embeddings.create(
            model=self.model,
            input=clean_text,
        )

        return response.data[0].embedding

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Create embedding vectors for multiple text chunks.

        Empty chunks are rejected before calling the embedding API.
        """
        clean_texts = [text.strip() for text in texts if text.strip()]

        if not clean_texts:
            raise ValueError("No valid text chunks were provided for embedding.")

        response = self.client.embeddings.create(
            model=self.model,
            input=clean_texts,
        )

        return [item.embedding for item in response.data]