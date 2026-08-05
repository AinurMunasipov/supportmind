from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory


def create_memory(
    db: Session,
    user_id: str,
    role: str,
    content: str,
) -> Memory:
    memory = Memory(user_id=user_id, role=role, content=content)
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


def get_user_memories(db: Session, user_id: str) -> list[Memory]:
    statement = select(Memory).where(Memory.user_id == user_id)
    return list(db.scalars(statement).all())


def delete_user_memories(db: Session, user_id: str) -> list[Memory]:
    memories = get_user_memories(db, user_id)
    for memory in memories:
        db.delete(memory)

    db.commit()
    return memories
