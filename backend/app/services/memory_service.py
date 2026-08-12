from typing import Optional

from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.repositories import memory_repository
from app.services.embedding_service import EmbeddingService


def _create_embedding_service() -> EmbeddingService:
    return EmbeddingService()


class MemoryService:
    def __init__(
        self,
        db: Session,
        embedding_service: Optional[EmbeddingService] = None,
    ) -> None:
        self._db = db
        self._embedding_service = (
            embedding_service
            if embedding_service is not None
            else _create_embedding_service()
        )

    def save_memory(self, user_id: str, role: str, content: str) -> Memory:
        embedding = self._embedding_service.generate_embedding(content)
        return memory_repository.create_memory(
            db=self._db,
            user_id=user_id,
            role=role,
            content=content,
            embedding=embedding,
        )

    def load_memories(self, user_id: str) -> list[Memory]:
        return memory_repository.get_user_memories(
            db=self._db,
            user_id=user_id,
        )

    def recent_memories(
        self,
        user_id: str,
        limit: int = 6,
    ) -> list[Memory]:
        return memory_repository.get_recent_memories(
            db=self._db,
            user_id=user_id,
            limit=limit,
        )

    def search_memories(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
    ) -> list[Memory]:
        embedding = self._embedding_service.generate_embedding(query)
        return memory_repository.search_similar_memories(
            db=self._db,
            user_id=user_id,
            embedding=embedding,
            limit=limit,
        )

    def clear_memories(self, user_id: str) -> list[Memory]:
        return memory_repository.delete_user_memories(
            db=self._db,
            user_id=user_id,
        )
