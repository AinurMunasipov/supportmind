from app.models.memory import Memory


class PromptBuilder:
    def build_messages(
        self,
        system_prompt: str,
        memories: list[Memory],
        user_message: str,
    ) -> list[dict]:
        messages = [
            {
                "role": "system",
                "content": system_prompt,
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
                "content": user_message,
            }
        )
        return messages
