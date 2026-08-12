from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import OPENAI_API_KEY
from app.core.prompts import SUPPORTMIND_SYSTEM_PROMPT
from app.services.memory_service import MemoryService
from app.services.prompt_builder import PromptBuilder


class ChatService:
    def __init__(self, db: Session) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._memory_service = MemoryService(db)
        self._prompt_builder = PromptBuilder()

    def generate_response(self, user_id: str, message: str) -> str:
        memories = self._memory_service.search_memories(user_id, message)
        messages = self._prompt_builder.build_messages(
            system_prompt=SUPPORTMIND_SYSTEM_PROMPT,
            memories=memories,
            user_message=message,
        )

        completion = self._client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=messages,
        )
        assistant_response = completion.choices[0].message.content or ""

        self._memory_service.save_memory(user_id, "user", message)
        self._memory_service.save_memory(
            user_id,
            "assistant",
            assistant_response,
        )

        return assistant_response
