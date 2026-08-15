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
        effective_mcp_results = (
            mcp_results if mcp_results is not None else tool_results
        )
        mcp_context = "\n\n".join(
            (
                f"Tool: {result.tool}\n"
                f"Success: {result.success}\n"
                f"Content:\n{result.content}"
            )
            for result in effective_mcp_results
        )
        context = (
            f"=== System Prompt ===\n\n"
            f"Core instructions that define the assistant's role and behavior.\n\n"
            f"{system_prompt.rstrip()}\n\n"
            f"=== Recent Memory ===\n\n"
            f"Recent conversation history with this user.\n\n"
            f"{recent_context}\n\n"
            f"=== Relevant Memory ===\n\n"
            f"Past memories retrieved by semantic similarity.\n\n"
            f"{relevant_context}\n\n"
            f"=== External System Context (CockroachDB MCP) ===\n\n"
            f"Trusted information retrieved from CockroachDB MCP tools.\n"
            f"Use it as factual external context.\n\n"
            f"{mcp_context}"
        )
        user_context = (
            f"=== User Message ===\n\n"
            f"Current user request.\n\n"
            f"{user_message}"
        )

        return [
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": user_context,
            },
        ]
