from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.mcp_service import MCPService


def main() -> None:
    load_dotenv(ENV_PATH)

    service = MCPService()
    results = service.execute(
        user_id="debug",
        message="show me tables",
    )

    print(f"ToolResult count: {len(results)}")
    for result in results:
        print(f"tool: {result.tool}")
        print(f"success: {result.success}")
        print(f"content: {result.content}")


if __name__ == "__main__":
    main()
