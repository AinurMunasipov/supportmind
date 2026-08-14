from __future__ import annotations

import asyncio
import json
import os
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, TypeVar

import httpx
from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import TextContent, Tool

_T = TypeVar("_T")


@dataclass
class ToolResult:
    tool: str
    success: bool
    content: str


class MCPService:
    _SERVER_URL = "https://cockroachlabs.cloud/mcp"

    def _run_async(self, awaitable: Awaitable[_T]) -> _T:
        return asyncio.run(awaitable)

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

    async def _discover_tools(self, client: Client) -> dict[str, Tool]:
        result = await client.list_tools()
        return {tool.name: tool for tool in result.tools}

    async def _call_tool(
        self,
        client: Client,
        tools: dict[str, Tool],
        tool_name: str,
        arguments: dict[str, Any],
    ) -> list[ToolResult]:
        if tool_name not in tools:
            return [
                ToolResult(
                    tool=tool_name,
                    success=False,
                    content=f"MCP tool not found: {tool_name}",
                )
            ]

        try:
            response = await client.call_tool(tool_name, arguments)
            content = "\n".join(
                block.text
                for block in (response.content or [])
                if isinstance(block, TextContent) and block.text
            ).strip()

            if not content and response.structured_content is not None:
                content = json.dumps(
                    response.structured_content,
                    ensure_ascii=False,
                    default=str,
                )

            if response.is_error:
                return [
                    ToolResult(
                        tool=tool_name,
                        success=False,
                        content=content or "MCP tool returned an error.",
                    )
                ]

            if not content:
                return [
                    ToolResult(
                        tool=tool_name,
                        success=False,
                        content="MCP tool returned an empty response.",
                    )
                ]

            return [
                ToolResult(
                    tool=tool_name,
                    success=True,
                    content=content,
                )
            ]
        except Exception as exc:
            return [
                ToolResult(
                    tool=tool_name,
                    success=False,
                    content=str(exc) or "MCP tool call failed.",
                )
            ]

    def execute(self, user_id: str, message: str) -> list[ToolResult]:
        normalized_message = message.strip().lower()
        words = normalized_message.split()
        return self._dispatch(words)

    def _dispatch(self, words: list[str]) -> list[ToolResult]:
        if "table" in words or "tables" in words:
            return self._execute_table_workflow()

        if "schema" in words:
            return self._execute_table_workflow()

        return []

    def _execute_table_workflow(self) -> list[ToolResult]:
        try:
            cluster_results = self._list_clusters()
        except Exception:
            return []

        cluster_result = self._get_first_success(cluster_results)
        if cluster_result is None:
            return []

        cluster_name = self._get_cluster_name(cluster_result)
        if cluster_name is None:
            return []

        try:
            database_results = self._list_databases(cluster_name)
        except Exception:
            return []

        database_result = self._get_first_success(database_results)
        if database_result is None:
            return []

        database_name = self._get_database_name(database_result)
        if database_name is None:
            return []

        try:
            table_results = self._list_tables(cluster_name, database_name)
        except Exception:
            return []

        table_result = self._get_first_success(table_results)
        if table_result is None:
            return []

        table_name = self._get_table_name(table_result)
        if table_name is None:
            return []

        try:
            return [self._get_table_schema(database_name, table_name)]
        except Exception:
            return []

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

    def _parse_json_response(
        self,
        result: ToolResult,
    ) -> dict[str, Any] | None:
        if not result.success:
            return None

        try:
            parsed = json.loads(result.content)
        except (json.JSONDecodeError, TypeError):
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed

    def _get_first_row(
        self,
        result: ToolResult,
    ) -> dict[str, Any] | None:
        parsed = self._parse_json_response(result)
        if parsed is None:
            return None

        rows = parsed.get("rows")
        if not isinstance(rows, list) or not rows:
            return None

        first_row = rows[0]
        if not isinstance(first_row, dict):
            return None

        return first_row

    def _get_cluster_name(
        self,
        result: ToolResult,
    ) -> str | None:
        row = self._get_first_row(result)
        if row is None:
            return None

        name = row.get("name")
        if not isinstance(name, str):
            return None

        return name

    def _get_database_name(
        self,
        result: ToolResult,
    ) -> str | None:
        row = self._get_first_row(result)
        if row is None:
            return None

        name = row.get("database_name")
        if not isinstance(name, str):
            return None

        return name

    def _get_table_name(
        self,
        result: ToolResult,
    ) -> str | None:
        row = self._get_first_row(result)
        if row is None:
            return None

        table_name = row.get("table_name")
        if not isinstance(table_name, str):
            return None

        return table_name

    def _list_clusters(self) -> list[ToolResult]:
        return self._run_async(self._list_clusters_async())

    async def _list_clusters_async(self) -> list[ToolResult]:
        async with self._connected_client() as client:
            tools = await self._discover_tools(client)
            return await self._call_tool(
                client,
                tools,
                "list_clusters",
                {},
            )

    def _list_databases(self, cluster_name: str) -> list[ToolResult]:
        return self._run_async(self._list_databases_async(cluster_name))

    async def _list_databases_async(
        self,
        cluster_name: str,
    ) -> list[ToolResult]:
        async with self._connected_client() as client:
            tools = await self._discover_tools(client)
            return await self._call_tool(
                client,
                tools,
                "list_databases",
                {},
            )

    def _list_tables(
        self,
        cluster_name: str,
        database_name: str,
    ) -> list[ToolResult]:
        return self._run_async(
            self._list_tables_async(cluster_name, database_name)
        )

    async def _list_tables_async(
        self,
        cluster_name: str,
        database_name: str,
    ) -> list[ToolResult]:
        async with self._connected_client() as client:
            tools = await self._discover_tools(client)
            return await self._call_tool(
                client,
                tools,
                "list_tables",
                {"database": database_name},
            )

    def _get_table_schema(
        self,
        database_name: str = "defaultdb",
        table_name: str = "memories",
    ) -> ToolResult:
        return self._run_async(
            self._get_table_schema_async(database_name, table_name)
        )

    async def _get_table_schema_async(
        self,
        database_name: str,
        table_name: str,
    ) -> ToolResult:
        async with self._connected_client() as client:
            tools = await self._discover_tools(client)
            results = await self._call_tool(
                client,
                tools,
                "get_table_schema",
                {
                    "database": database_name,
                    "table": table_name,
                },
            )
            return results[0]
