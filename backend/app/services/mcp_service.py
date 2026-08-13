from dataclasses import dataclass


@dataclass
class ToolResult:
    tool: str
    success: bool
    content: str


class MCPService:
    def execute(self, user_id: str, message: str) -> list[ToolResult]:
        return []
