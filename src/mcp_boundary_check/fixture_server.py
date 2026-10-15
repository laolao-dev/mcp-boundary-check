"""Official SDK transport adapter; synthetic, process-local fixture only."""
import asyncio
import json
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

from .core import PermissionCore, SCHEMAS

core = PermissionCore()
audit_path = Path(os.environ["MBC_DEMO_AUDIT"])


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name=name, description="Local synthetic " + name, input_schema=schema)
        for name, schema in SCHEMAS.items()
    ])


async def call_tool(ctx, params):
    meta = params.meta or {}

    def handler_entered(**event):
        event.update(case_id=meta.get("demo_case"), request_id=str(ctx.request_id),
                     event="handler_entered")
        with audit_path.open("a", encoding="utf-8") as audit:
            audit.write(json.dumps(event, sort_keys=True) + "\n")
            audit.flush()

    data, error = core.invoke(params.name, params.arguments, meta.get("demo_token"),
                              handler_entered)
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(data))],
                          structured_content=data, is_error=error)


server = Server("MCP-Boundary-Check-Demo", version="0.1.0",
                on_list_tools=list_tools, on_call_tool=call_tool)


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
