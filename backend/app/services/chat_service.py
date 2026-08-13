from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import OPENAI_API_KEY
from app.core.prompts import SUPPORTMIND_SYSTEM_PROMPT
from app.services.mcp_service import MCPService
from app.services.memory_decision_service import MemoryDecisionService
from app.services.memory_service import MemoryService
from app.services.memory_storage_decision_service import MemoryStorageDecisionService
from app.services.prompt_builder import PromptBuilder


class ChatService:
    def __init__(self, db: Session) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._mcp_service = MCPService()
        self._memory_decision_service = MemoryDecisionService()
        self._memory_service = MemoryService(db)
        self._memory_storage_decision_service = MemoryStorageDecisionService()
        self._prompt_builder = PromptBuilder()

    def generate_response(self, user_id: str, message: str) -> str:
        recent_memories = self._memory_service.recent_memories(user_id)
        relevant_memories = []
        if self._memory_decision_service.should_search_memories(message):
            relevant_memories = self._memory_service.search_memories(
                user_id,
                message,
            )
        # Future CockroachDB Managed MCP integration point; tool results will be
        # passed to PromptBuilder in a later milestone.
        tool_results = self._mcp_service.execute(user_id, message)
        messages = self._prompt_builder.build_messages(
            system_prompt=SUPPORTMIND_SYSTEM_PROMPT,
            recent_memories=recent_memories,
            relevant_memories=relevant_memories,
            user_message=message,
        )

        completion = self._client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=messages,
        )
        assistant_response = completion.choices[0].message.content or ""

        if self._memory_storage_decision_service.should_store_memory(message):
            self._memory_service.save_memory(user_id, "user", message)
            self._memory_service.save_memory(
                user_id,
                "assistant",
                assistant_response,
            )

        return assistant_response
