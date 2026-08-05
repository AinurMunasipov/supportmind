from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.repositories import memory_repository


class MemoryService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def save_memory(self, user_id: str, role: str, content: str) -> Memory:
        return memory_repository.create_memory(
            db=self._db,
            user_id=user_id,
            role=role,
            content=content,
        )

    def load_memories(self, user_id: str) -> list[Memory]:
        return memory_repository.get_user_memories(
            db=self._db,
            user_id=user_id,
        )

    def clear_memories(self, user_id: str) -> list[Memory]:
        return memory_repository.delete_user_memories(
            db=self._db,
            user_id=user_id,
        )
