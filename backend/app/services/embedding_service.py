from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_embedding(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            input=text,
            model=OPENAI_EMBEDDING_MODEL,
        )
        return response.data[0].embedding
