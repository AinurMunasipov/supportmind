from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service() -> ChatService:
    return ChatService()


ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]


@router.post("", response_model=ChatResponse)
def create_chat(
    payload: ChatRequest,
    service: ChatServiceDependency,
) -> ChatResponse:
    return ChatResponse(response=service.generate_response(payload.message))
