from enum import Enum, auto


class MemoryDecision(Enum):
    STORE = auto()
    SKIP = auto()


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

    def should_store_memory(self, message: str) -> MemoryDecision:
        return (
            MemoryDecision.STORE
            if message.strip().lower() not in self._LOW_VALUE_MESSAGES
            else MemoryDecision.SKIP
        )
