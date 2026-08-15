from enum import Enum, auto


class RetrievalDecision(Enum):
    RETRIEVE = auto()
    SKIP = auto()


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

    def should_search_memories(self, message: str) -> RetrievalDecision:
        return (
            RetrievalDecision.RETRIEVE
            if self._should_retrieve(message)
            else RetrievalDecision.SKIP
        )

    def _should_retrieve(self, message: str) -> bool:
        normalized_message = message.strip().lower()
        return normalized_message not in self._CONVERSATIONAL_MESSAGES
