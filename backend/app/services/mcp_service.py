from __future__ import annotations

import asyncio
import json
import logging
import os
import re
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, TypeVar

import httpx
from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import TextContent, Tool

_T = TypeVar("_T")
logger = logging.getLogger("uvicorn.error").getChild(__name__)


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

        logger.info(
            "Initializing MCP HTTP transport cluster_id_configured=%s",
            bool(cluster_id),
        )
        async with httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
        ) as http_client:
            transport = streamable_http_client(
                self._SERVER_URL,
                http_client=http_client,
            )
            connected = False
            try:
                logger.info("Connecting MCP client")
                async with Client(transport) as client:
                    connected = True
                    logger.info("MCP client connected")
                    yield client
            except Exception as exc:
                stage = (
                    "connected client session"
                    if connected
                    else "client protocol initialization"
                )
                details = self._format_exception(exc)
                logger.exception("MCP %s failed: %s", stage, details)
                hint = (
                    " Verify deployed COCKROACH_MCP_API_KEY and "
                    "COCKROACH_MCP_CLUSTER_ID values."
                    if "MCPError" in details
                    else ""
                )
                raise RuntimeError(
                    f"MCP {stage} failed: {details}.{hint}"
                ) from exc

    async def _discover_tools(self, client: Client) -> dict[str, Tool]:
        logger.info("Discovering MCP tools")
        result = await client.list_tools()
        tools = {tool.name: tool for tool in result.tools}
        logger.info("MCP tool discovery complete tool_count=%s", len(tools))
        return tools

    async def _call_tool(
        self,
        client: Client,
        tools: dict[str, Tool],
        tool_name: str,
        arguments: dict[str, Any],
    ) -> list[ToolResult]:
        if tool_name not in tools:
            return [
                self._create_result(
                    tool=tool_name,
                    success=False,
                    content=f"MCP tool not found: {tool_name}",
                )
            ]

        try:
            logger.info("Executing MCP tool tool=%s", tool_name)
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
                    self._create_result(
                        tool=tool_name,
                        success=False,
                        content=content or "MCP tool returned an error.",
                    )
                ]

            if not content:
                return [
                    self._create_result(
                        tool=tool_name,
                        success=False,
                        content="MCP tool returned an empty response.",
                    )
                ]

            return [
                self._create_result(
                    tool=tool_name,
                    success=True,
                    content=content,
                )
            ]
        except Exception as exc:
            logger.exception("MCP tool execution error tool=%s", tool_name)
            return [
                self._create_result(
                    tool=tool_name,
                    success=False,
                    content=self._format_exception(exc),
                )
            ]

    def _format_exception(self, error: BaseException) -> str:
        if isinstance(error, BaseExceptionGroup):
            details = [
                self._format_exception(nested)
                for nested in error.exceptions
            ]
            return "; ".join(dict.fromkeys(details))

        message = str(error).strip() or "No error details provided."
        code = getattr(error, "code", None)
        code_details = f" code={code}" if code is not None else ""
        return f"{type(error).__name__}{code_details}: {message}"

    def _create_result(
        self,
        tool: str,
        success: bool,
        content: str,
    ) -> ToolResult:
        result = ToolResult(
            tool=tool,
            success=success,
            content=content,
        )
        log_method = logger.info if success else logger.error
        log_method(
            "MCP execution result tool=%s success=%s content_length=%s",
            tool,
            success,
            len(content),
        )
        return result

    def execute(self, user_id: str, message: str) -> list[ToolResult]:
        normalized_message = message.strip().lower()
        words = re.findall(r"[a-z0-9_]+", normalized_message)
        return self._dispatch(words)

    def _dispatch(self, words: list[str]) -> list[ToolResult]:
        workflow = self._get_workflow(words)
        logger.info("MCP workflow selected workflow=%s", workflow)

        if workflow == "table":
            return self._execute_table_workflow()

        return []

    def _get_workflow(self, words: list[str]) -> str | None:
        routes = {
            "column": "table",
            "columns": "table",
            "database": "table",
            "databases": "table",
            "table": "table",
            "tables": "table",
            "schema": "table",
            "structure": "table",
        }
        return next(
            (routes[word] for word in words if word in routes),
            None,
        )

    def _execute_table_workflow(self) -> list[ToolResult]:
        workflow_results: list[ToolResult] = []

        try:
            cluster_results = self._list_clusters()
        except Exception as exc:
            logger.exception("MCP workflow error tool=list_clusters")
            return [
                self._create_result(
                    tool="list_clusters",
                    success=False,
                    content=self._format_exception(exc),
                )
            ]

        workflow_results.extend(cluster_results)

        cluster_result = self._get_first_success(cluster_results)
        if cluster_result is None:
            if not cluster_results:
                workflow_results.append(
                    self._create_result(
                        tool="list_clusters",
                        success=False,
                        content="list_clusters returned no results.",
                    )
                )
            return workflow_results

        cluster_name = self._get_cluster_name(cluster_result)
        if cluster_name is None:
            workflow_results.append(
                self._create_result(
                    tool="list_clusters",
                    success=False,
                    content="Unable to extract cluster name from list_clusters response.",
                )
            )
            return workflow_results

        try:
            database_results = self._list_databases(cluster_name)
        except Exception as exc:
            logger.exception("MCP workflow error tool=list_databases")
            workflow_results.append(
                self._create_result(
                    tool="list_databases",
                    success=False,
                    content=self._format_exception(exc),
                )
            )
            return workflow_results

        workflow_results.extend(database_results)

        database_result = self._get_first_success(database_results)
        if database_result is None:
            if not database_results:
                workflow_results.append(
                    self._create_result(
                        tool="list_databases",
                        success=False,
                        content="list_databases returned no results.",
                    )
                )
            return workflow_results

        database_name = self._get_database_name(database_result)
        if database_name is None:
            workflow_results.append(
                self._create_result(
                    tool="list_databases",
                    success=False,
                    content=(
                        "Unable to extract database name from "
                        "list_databases response."
                    ),
                )
            )
            return workflow_results

        try:
            table_results = self._list_tables(cluster_name, database_name)
        except Exception as exc:
            logger.exception("MCP workflow error tool=list_tables")
            workflow_results.append(
                self._create_result(
                    tool="list_tables",
                    success=False,
                    content=self._format_exception(exc),
                )
            )
            return workflow_results

        workflow_results.extend(table_results)

        table_result = self._get_first_success(table_results)
        if table_result is None:
            if not table_results:
                workflow_results.append(
                    self._create_result(
                        tool="list_tables",
                        success=False,
                        content="list_tables returned no results.",
                    )
                )
            return workflow_results

        table_name = self._get_table_name(table_result)
        if table_name is None:
            workflow_results.append(
                self._create_result(
                    tool="list_tables",
                    success=False,
                    content="Unable to extract table name from list_tables response.",
                )
            )
            return workflow_results

        try:
            schema_result = self._get_table_schema(database_name, table_name)
        except Exception as exc:
            logger.exception("MCP workflow error tool=get_table_schema")
            workflow_results.append(
                self._create_result(
                    tool="get_table_schema",
                    success=False,
                    content=self._format_exception(exc),
                )
            )
            return workflow_results

        workflow_results.append(schema_result)
        return workflow_results

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
