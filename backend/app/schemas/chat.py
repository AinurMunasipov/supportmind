from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str


class MemoryInspectorItem(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
    importance: int
    summary: str | None


class McpInspectorItem(BaseModel):
    tool: str
    success: bool
    content: str


class ChatResponse(BaseModel):
    response: str
    recent_memories: list[MemoryInspectorItem] | None = None
    relevant_memories: list[MemoryInspectorItem] | None = None
    mcp_results: list[McpInspectorItem] | None = None
