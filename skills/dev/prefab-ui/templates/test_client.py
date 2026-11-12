"""Smoke-test the MCP server without a host (in-process FastMCP client)."""
import asyncio
import json
from pathlib import Path

from fastmcp import Client


async def main() -> None:
    async with Client(Path(__file__).with_name("mcp_server.py")) as c:
        for t in await c.list_tools():
            print("TOOL", t.name, json.dumps((t.meta or {}).get("ui")))
        for name in ("team_table", "team_dashboard", "notes_app"):
            r = await c.call_tool(name, {})
            sc = r.structured_content
            print(name, "->", list(sc)[:4] if isinstance(sc, dict) else type(sc))
        print("add_note ->", (await c.call_tool("add_note", {"text": "from test"})).data)


asyncio.run(main())
