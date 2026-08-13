from app.models.memory import Memory


class PromptBuilder:
    def build_messages(
        self,
        system_prompt: str,
        recent_memories: list[Memory],
        relevant_memories: list[Memory],
        tool_results: list[str],
        user_message: str,
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
        tool_context = "\n".join(tool_results)
        context = (
            f"{system_prompt.rstrip()}\n\n"
            f"=== Recent Conversation ===\n\n"
            f"{recent_context}\n\n"
            f"=== Relevant Memories ===\n\n"
            f"{relevant_context}\n\n"
            f"=== Tool Results ===\n\n"
            f"{tool_context}"
        )

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
