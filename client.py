from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  
    args=["run_stdio.py"],
    env=None, 
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()

            for tool in tools:
                print(tool)
            
            # Communication loop
            try:
                while True:
                    # Get user input
                    message = input("\nEnter a message (or 'exit' to quit): ")
                    
                    # Check if user wants to exit
                    if message.lower() == 'exit':
                        print("Exiting...")
                        break
                    
                    # Call the echo tool
                    try:
                        result = await session.call_tool("echo", arguments={"message": message})
                        print(f"Server response:\n {result.content[0].text}")
                    except Exception as e:
                        print(f"Error calling tool: {e}")
                        
            except KeyboardInterrupt:
                print("\nLoop interrupted. Exiting...")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
