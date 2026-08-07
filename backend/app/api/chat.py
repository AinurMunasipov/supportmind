from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
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
    return ChatResponse(
        response=service.generate_response(payload.user_id, payload.message)
    )
