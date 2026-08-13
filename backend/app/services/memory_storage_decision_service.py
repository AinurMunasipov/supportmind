class MemoryStorageDecisionService:
    _LOW_VALUE_MESSAGES = {
        "hello",
        "hi",
        "thanks",
        "thank you",
        "goodbye",
        "bye",
        "ok",
        "okay",
        "yes",
        "no",
        "sure",
    }

    def should_store_memory(self, message: str) -> bool:
        return message.strip().lower() not in self._LOW_VALUE_MESSAGES
