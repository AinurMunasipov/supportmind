class MemoryDecisionService:
    _CONVERSATIONAL_MESSAGES = {
        "hello",
        "hi",
        "thanks",
        "thank you",
        "goodbye",
        "bye",
        "ok",
        "okay",
    }

    def should_search_memories(self, message: str) -> bool:
        return message.strip().lower() not in self._CONVERSATIONAL_MESSAGES
