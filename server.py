from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

import mcp.types as types


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
    async def handle_call_tool(name: str, arguments: dict | None):
        """
        Handle tool execution requests.
        Tools can modify server state and notify clients of changes.
        """
        try:
            print(f"handle_call_tool {name}")
            if name == "echo":
                message = arguments.get("message")
                response = [
                    types.TextContent(
                        type="text",
                        text=str(message),
                    )
                ]
                return response
        except Exception as e:
            print(f"Error handling tool call {name}: {e}")
            raise e
        
    
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        List available tools.
        Each tool specifies its arguments using JSON Schema validation.
        """
        return [
            types.Tool(
                name="echo",
                description="Echo a message back to the client",
                inputSchema={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                },
            )
        ]
    
    return server, init_options