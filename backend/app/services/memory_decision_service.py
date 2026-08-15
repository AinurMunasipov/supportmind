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
            if message.strip().lower() not in self._CONVERSATIONAL_MESSAGES
            else RetrievalDecision.SKIP
        )
