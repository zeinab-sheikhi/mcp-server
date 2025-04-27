from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

from mcp.types import (
    Tool, 
    TextContent,
)
from pydantic import BaseModel
from enum import Enum


class EchoTool(BaseModel):
    message: str


class Tools(str, Enum):
    ECHO = "echo"


def create_server():
    server = Server("simple-mcp-server")
    
    init_options = InitializationOptions(
        server_name="simple-mcp-server",
        server_version="0.1.0",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        ),
    )

    @server.call_tool()
    async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
        """
        Handle tool execution requests.
        Tools can modify server state and notify clients of changes.
        """
        match name:
            case Tools.ECHO:
                message = arguments.get("message")
                return [
                    TextContent(
                        type="text",
                        text=str(message),
                    )
                ]
            case _:
                raise ValueError(f"Unknown tool: {name}")


    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """
        List available tools.
        Each tool specifies its arguments using JSON Schema validation.
        """
        return [
            Tool(
                name=Tools.ECHO,
                description="Echo a message back to the client",
                inputSchema=EchoTool.schema()
            )
        ]
    
    return server, init_options