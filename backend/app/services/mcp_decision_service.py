class MCPDecisionService:
    _MCP_KEYWORDS = {
        "count",
        "how many",
        "database",
        "table",
        "tables",
        "schema",
        "column",
        "columns",
        "index",
        "indexes",
        "show",
        "list",
        "cluster",
        "clusters",
    }

    def should_use_mcp(self, message: str) -> bool:
        normalized_message = message.strip().lower()
        words = normalized_message.split()
        return any(
            (
                keyword in normalized_message
                if " " in keyword
                else keyword in words
            )
            for keyword in self._MCP_KEYWORDS
        )
