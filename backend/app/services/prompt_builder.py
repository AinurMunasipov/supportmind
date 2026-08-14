from app.models.memory import Memory
from app.services.mcp_service import ToolResult


class PromptBuilder:
    def build_messages(
        self,
        system_prompt: str,
        recent_memories: list[Memory],
        relevant_memories: list[Memory],
        tool_results: list[ToolResult],
        user_message: str,
        mcp_results: list[ToolResult] | None = None,
    ) -> list[dict]:
        recent_context = "\n".join(
            f"{memory.role}: {memory.content}"
            for memory in sorted(
                recent_memories,
                key=lambda memory: memory.created_at,
            )
        )
        relevant_context = "\n".join(
            f"{memory.role}: {memory.content}"
            for memory in sorted(
                relevant_memories,
                key=lambda memory: memory.created_at,
            )
        )
        tool_context = "\n".join(
            result.content
            for result in tool_results
        )
        context = (
            f"{system_prompt.rstrip()}\n\n"
            f"=== Recent Conversation ===\n\n"
            f"{recent_context}\n\n"
            f"=== Relevant Memories ===\n\n"
            f"{relevant_context}\n\n"
            f"=== Tool Results ===\n\n"
            f"{tool_context}"
        )
        if mcp_results:
            mcp_context = "\n\n".join(
                (
                    f"Tool: {result.tool}\n"
                    f"Success: {result.success}\n"
                    f"Content:\n{result.content}"
                )
                for result in mcp_results
                if result.success
            )
            context += f"\n\n=== MCP Results ===\n\n{mcp_context}"

        return [
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]
