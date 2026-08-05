from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.memory import MemoryCreate, MemoryDeleteResponse, MemoryResponse
from app.services.memory_service import MemoryService


router = APIRouter(prefix="/memory", tags=["memory"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=MemoryResponse)
def create_memory(payload: MemoryCreate, db: DatabaseSession) -> MemoryResponse:
    service = MemoryService(db)
    return service.save_memory(
        user_id=payload.user_id,
        role=payload.role,
        content=payload.content,
    )


@router.get("/{user_id}", response_model=list[MemoryResponse])
def get_user_memories(user_id: str, db: DatabaseSession) -> list[MemoryResponse]:
    service = MemoryService(db)
    return service.load_memories(user_id)


@router.delete("/{user_id}", response_model=MemoryDeleteResponse)
def delete_user_memories(
    user_id: str,
    db: DatabaseSession,
) -> MemoryDeleteResponse:
    service = MemoryService(db)
    service.clear_memories(user_id)
    return MemoryDeleteResponse(status="success")
