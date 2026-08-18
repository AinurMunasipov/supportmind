import logging
import re


logger = logging.getLogger("uvicorn.error").getChild(__name__)


class MCPDecisionService:
    _MCP_KEYWORDS = {
        "count",
        "database",
        "databases",
        "table",
        "tables",
        "schema",
        "column",
        "columns",
        "structure",
        "index",
        "indexes",
        "cluster",
        "clusters",
    }
    _MCP_PHRASES = {"how many"}

    def should_use_mcp(self, message: str) -> bool:
        normalized_message = message.strip().lower()
        words = set(re.findall(r"[a-z0-9_]+", normalized_message))
        decision = bool(words & self._MCP_KEYWORDS) or any(
            phrase in normalized_message
            for phrase in self._MCP_PHRASES
        )
        logger.info("MCP decision use_mcp=%s", decision)
        return decision
