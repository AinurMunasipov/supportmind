from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import OPENAI_API_KEY
from app.core.prompts import SUPPORTMIND_SYSTEM_PROMPT
from app.services.memory_service import MemoryService


class ChatService:
    def __init__(self, db: Session) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._memory_service = MemoryService(db)

    def generate_response(self, user_id: str, message: str) -> str:
        memories = self._memory_service.load_memories(user_id)
        messages = [
            {
                "role": "system",
                "content": SUPPORTMIND_SYSTEM_PROMPT,
            }
        ]
        messages.extend(
            {
                "role": memory.role,
                "content": memory.content,
            }
            for memory in sorted(memories, key=lambda memory: memory.created_at)
        )
        messages.append(
            {
                "role": "user",
                "content": message,
            }
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
