import sys, os

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from openapi_to_mcp_tools import register_openapi_tools, format_tools_for_prompt

mcp = FastMCP("Arithmetic Tool Server")

# Register OpenAPI tools from spec file (change path as needed)
openapi_tools = register_openapi_tools(mcp, os.path.join(os.path.dirname(__file__), "../myswagger.json"))
print("\nOpenAPI Tools Registered:")
print(format_tools_for_prompt(openapi_tools))

# Addition Tool
@mcp.tool(
    name="add_tool",
    description="Performs basic arithmetic addition. Accepts two float inputs and returns their sum."
)
def add_tool(num1: float, num2: float) -> dict:
    return {"sum": num1 + num2}

# Subtraction Tool
@mcp.tool(
    name="subtract_tool",
    description="Performs basic arithmetic subtraction. Accepts two float inputs and returns the difference."
)
def subtract_tool(num1: float, num2: float) -> dict:
    return {"difference": num1 - num2}

# Multiplication Tool
@mcp.tool(
    name="multiply_tool",
    description="Performs basic arithmetic multiplication. Accepts two float inputs and returns the product."
)
def multiply_tool(num1: float, num2: float) -> dict:
    return {"product": num1 * num2}

# Division Tool
@mcp.tool(
    name="divide_tool",
    description="Performs basic arithmetic division. Accepts two float inputs and returns the quotient."
)
def divide_tool(num1: float, num2: float) -> dict:
    if num2 == 0:
        raise ValueError("Division by zero is not allowed.")
    return {"quotient": num1 / num2}

@mcp.custom_route("/add", methods=["POST"])
async def add_endpoint(request: Request):
    data = await request.json()
    num1 = data.get("num1")
    num2 = data.get("num2")
    result = add_tool(num1, num2)
    return JSONResponse(result)

@mcp.tool(
    name="weather_tool",
    description="Fetches the current weather for a given city using Open-Meteo API."
)
def weather_tool(city: str) -> dict:
    # Open-Meteo API (free, no key required)
    # For demo: use geocoding to get lat/lon, then fetch weather
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_resp = requests.get(geo_url)
    geo_data = geo_resp.json()
    if not geo_data.get("results"):
        return {"error": f"City '{city}' not found."}
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_resp = requests.get(weather_url)
    weather_data = weather_resp.json()
    if "current_weather" in weather_data:
        return weather_data["current_weather"]
    return {"error": "Weather data not available."}

print("Registered tools:", mcp.tool)

if __name__ == "__main__":
    mcp.run(transport="sse", host="localhost", port=8081)