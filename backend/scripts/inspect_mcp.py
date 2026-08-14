from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client


SERVER_URL = "https://cockroachlabs.cloud/mcp"
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


async def main() -> None:
    load_dotenv(ENV_PATH)

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
            SERVER_URL,
            http_client=http_client,
        )
        async with Client(transport) as client:
            result = await client.list_tools()

            for tool in result.tools:
                print(f"Name: {tool.name}")
                if tool.description:
                    print(f"Description: {tool.description}")
                print("Input schema:")
                print(
                    json.dumps(
                        tool.input_schema,
                        indent=2,
                        ensure_ascii=False,
                        default=str,
                    )
                )
                print()

            response = await client.call_tool(
                "list_clusters",
                {},
            )
            print("========================")
            print("list_clusters response")
            print("========================")
            print(f"is_error: {response.is_error}")
            print(f"content: {response.content}")
            print("structured_content:")
            print(
                json.dumps(
                    response.structured_content,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )

            response = await client.call_tool("get_cluster", {})
            print("========================")
            print("get_cluster response")
            print("========================")
            print(f"is_error: {response.is_error}")
            print(f"content: {response.content}")
            print("structured_content:")
            print(
                json.dumps(
                    response.structured_content,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )

            response = await client.call_tool(
                "list_tables",
                {"database": "defaultdb"},
            )
            print("========================")
            print("list_tables response")
            print("========================")
            print(f"is_error: {response.is_error}")
            print(f"content: {response.content}")
            print("structured_content:")
            print(
                json.dumps(
                    response.structured_content,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )

            response = await client.call_tool(
                "get_table_schema",
                {
                    "database": "defaultdb",
                    "table": "memories",
                },
            )
            print("========================")
            print("get_table_schema response")
            print("========================")
            print(f"is_error: {response.is_error}")
            print(f"content: {response.content}")
            print("structured_content:")
            print(
                json.dumps(
                    response.structured_content,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
