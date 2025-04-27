import logging
from mcp.server.stdio import stdio_server

logger = logging.getLogger(__name__)

class STDIOHandler:
    def __init__(self, server, init_options):
        self.server = server
        self.init_options = init_options
    
    async def handle_stdio(self):
        """Handle STDIO communication."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.init_options,
                raise_exceptions=True,
            )
