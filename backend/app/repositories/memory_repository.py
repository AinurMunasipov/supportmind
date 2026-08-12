from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory


def create_memory(
    db: Session,
    user_id: str,
    role: str,
    content: str,
    embedding: list[float],
) -> Memory:
    memory = Memory(
        user_id=user_id,
        role=role,
        content=content,
        embedding=embedding,
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


def get_user_memories(db: Session, user_id: str) -> list[Memory]:
    statement = select(Memory).where(Memory.user_id == user_id)
    return list(db.scalars(statement).all())


def get_recent_memories(
    db: Session,
    user_id: str,
    limit: int = 6,
) -> list[Memory]:
    statement = (
        select(Memory)
        .where(Memory.user_id == user_id)
        .order_by(Memory.created_at.desc())
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def search_similar_memories(
    db: Session,
    user_id: str,
    embedding: list[float],
    limit: int = 5,
) -> list[Memory]:
    distance = Memory.embedding.cosine_distance(embedding)
    statement = (
        select(Memory)
        .where(Memory.user_id == user_id)
        .order_by(distance)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def delete_user_memories(db: Session, user_id: str) -> list[Memory]:
    memories = get_user_memories(db, user_id)
    for memory in memories:
        db.delete(memory)

    db.commit()
    return memories
