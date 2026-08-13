from dataclasses import dataclass


@dataclass
class ToolResult:
    tool: str
    success: bool
    content: str


class MCPService:
    def execute(self, user_id: str, message: str) -> list[ToolResult]:
        normalized_message = message.strip().lower()
        words = normalized_message.split()

        if "table" in words or "tables" in words:
            return [
                ToolResult(
                    tool="list_tables",
                    success=True,
                    content="""
Available tables:
- memories
""".strip(),
                )
            ]

        if "schema" in words:
            return [
                ToolResult(
                    tool="get_table_schema",
                    success=True,
                    content="""
Table memories:

id
user_id
role
content
embedding
created_at
""".strip(),
                )
            ]

        return []
