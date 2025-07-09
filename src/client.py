import asyncio
from fastmcp import Client

async def main():
    # Connect to your MCP server over SSE transport
    async with Client("http://localhost:8081/sse") as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", [tool.name for tool in tools])

        # Invoke add_tool
        if "add_tool" in [tool.name for tool in tools]:
            result = await client.call_tool("add_tool", {"num1": 20, "num2": 5})
            print("Tool result:", result.data)
        else:
            print("'add_tool' not found in registered tools.")

# Run the async main function
asyncio.run(main())
