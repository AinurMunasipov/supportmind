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
        return self._dispatch(words)

    def _dispatch(self, words: list[str]) -> list[ToolResult]:
        if "table" in words or "tables" in words:
            cluster_results = self._list_clusters()
            cluster_name = cluster_results[0].content
            database_results = self._list_databases(cluster_name)
            database_name = database_results[0].content
            return self._list_tables(cluster_name, database_name)

        if "schema" in words:
            return [self._get_table_schema()]

        return []

    def _list_clusters(self) -> list[ToolResult]:
        return [
            ToolResult(
                tool="list_clusters",
                success=True,
                content="supportmind-cluster",
            )
        ]

    def _list_databases(self, cluster_name: str) -> list[ToolResult]:
        return [
            ToolResult(
                tool="list_databases",
                success=True,
                content="defaultdb",
            )
        ]

    def _list_tables(
        self,
        cluster_name: str,
        database_name: str,
    ) -> list[ToolResult]:
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

    def _get_table_schema(self) -> ToolResult:
        return ToolResult(
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
