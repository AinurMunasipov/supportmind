from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import OPENAI_API_KEY
from app.core.prompts import SUPPORTMIND_SYSTEM_PROMPT
from app.services.agent_context_decision import AgentContextDecision
from app.services.mcp_decision_service import MCPDecisionService
from app.services.mcp_service import MCPService
from app.services.memory_decision_service import (
    MemoryDecisionService,
    RetrievalDecision,
)
from app.services.memory_service import MemoryService
from app.services.memory_storage_decision_service import (
    MemoryDecision,
    MemoryStorageDecisionService,
)
from app.services.prompt_builder import PromptBuilder


class ChatService:
    def __init__(self, db: Session) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._mcp_decision_service = MCPDecisionService()
        self._mcp_service = MCPService()
        self._memory_decision_service = MemoryDecisionService()
        self._memory_service = MemoryService(db)
        self._memory_storage_decision_service = MemoryStorageDecisionService()
        self._prompt_builder = PromptBuilder()

    def generate_response(self, user_id: str, message: str) -> str:
        recent_memories = self._memory_service.recent_memories(user_id)
        relevant_memories = []
        context_decision = AgentContextDecision(
            retrieve_memory=(
                self._memory_decision_service.should_search_memories(message)
                is RetrievalDecision.RETRIEVE
            ),
            use_mcp=self._mcp_decision_service.should_use_mcp(message),
        )
        if context_decision.retrieve_memory:
            relevant_memories = self._memory_service.search_memories(
                user_id,
                message,
            )
        if context_decision.use_mcp:
            mcp_results = self._mcp_service.execute(
                user_id,
                message,
            )
        else:
            mcp_results = []
        messages = self._prompt_builder.build_messages(
            system_prompt=SUPPORTMIND_SYSTEM_PROMPT,
            recent_memories=recent_memories,
            relevant_memories=relevant_memories,
            tool_results=mcp_results,
            user_message=message,
            mcp_results=mcp_results,
        )

        completion = self._client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=messages,
        )
        assistant_response = completion.choices[0].message.content or ""

        decision = self._memory_storage_decision_service.should_store_memory(
            message
        )
        if decision is MemoryDecision.STORE:
            self._memory_service.save_memory(user_id, "user", message)
            self._memory_service.save_memory(
                user_id,
                "assistant",
                assistant_response,
            )

        return assistant_response
