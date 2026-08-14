from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx
from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import Tool


@dataclass
class ToolResult:
    tool: str
    success: bool
    content: str


class MCPService:
    _SERVER_URL = "https://cockroachlabs.cloud/mcp"

    @asynccontextmanager
    async def _connected_client(self) -> AsyncIterator[Client]:
        api_key = os.getenv("COCKROACH_MCP_API_KEY", "").strip()
        if not api_key:
            raise ValueError("COCKROACH_MCP_API_KEY is not configured.")

        headers = {"Authorization": f"Bearer {api_key}"}
        cluster_id = os.getenv("COCKROACH_MCP_CLUSTER_ID", "").strip()
        if cluster_id:
            headers["mcp-cluster-id"] = cluster_id

        async with httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
        ) as http_client:
            transport = streamable_http_client(
                self._SERVER_URL,
                http_client=http_client,
            )
            async with Client(transport) as client:
                yield client

    async def _discover_tools(self) -> dict[str, Tool]:
        async with self._connected_client() as client:
            result = await client.list_tools()
            return {tool.name: tool for tool in result.tools}

    def execute(self, user_id: str, message: str) -> list[ToolResult]:
        normalized_message = message.strip().lower()
        words = normalized_message.split()
        return self._dispatch(words)

    def _dispatch(self, words: list[str]) -> list[ToolResult]:
        if "table" in words or "tables" in words:
            return self._execute_table_workflow()

        if "schema" in words:
            return [self._get_table_schema()]

        return []

    def _execute_table_workflow(self) -> list[ToolResult]:
        cluster_results = self._list_clusters()
        cluster_result = self._get_first_success(cluster_results)
        cluster_name = self._get_content(cluster_result)
        if cluster_name is None:
            return []

        database_results = self._list_databases(cluster_name)
        database_result = self._get_first_success(database_results)
        database_name = self._get_content(database_result)
        if database_name is None:
            return []

        table_results = self._list_tables(cluster_name, database_name)
        table_result = self._get_first_success(table_results)
        if table_result is None:
            return []

        return [table_result]

    def _get_first_success(
        self,
        results: list[ToolResult],
    ) -> ToolResult | None:
        return next(
            (result for result in results if result.success),
            None,
        )

    def _get_content(self, result: ToolResult | None) -> str | None:
        return result.content if result is not None else None

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
