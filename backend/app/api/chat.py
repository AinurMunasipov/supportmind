from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    McpInspectorItem,
    MemoryInspectorItem,
)
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_chat_service(db: DatabaseSession) -> ChatService:
    return ChatService(db)


ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]


@router.post("", response_model=ChatResponse)
def create_chat(
    payload: ChatRequest,
    service: ChatServiceDependency,
) -> ChatResponse:
    result = service.generate_response_with_context(
        payload.user_id,
        payload.message,
    )
    return ChatResponse(
        response=result.response,
        recent_memories=[
            MemoryInspectorItem(
                id=str(memory.id),
                role=memory.role,
                content=memory.content,
                created_at=memory.created_at,
                importance=memory.importance,
                summary=memory.summary,
            )
            for memory in result.recent_memories
        ],
        relevant_memories=[
            MemoryInspectorItem(
                id=str(memory.id),
                role=memory.role,
                content=memory.content,
                created_at=memory.created_at,
                importance=memory.importance,
                summary=memory.summary,
            )
            for memory in result.relevant_memories
        ],
        mcp_results=[
            McpInspectorItem(
                tool=tool_result.tool,
                success=tool_result.success,
                content=tool_result.content,
            )
            for tool_result in result.mcp_results
        ],
    )
