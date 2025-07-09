import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastmcp import FastMCP

mcp = FastMCP("Add Tool Server")

@mcp.tool(description="Adds two numbers and returns their sum")
def add_tool(num1: float, num2: float) -> dict:
    return {"sum": num1 + num2}

print("Registered tools:", mcp.tool)

    # Or return dict directly if api.add_numbers already formats it
    

if __name__ == "__main__":
    
    mcp.run(transport="sse", host="localhost", port=8081)
