import asyncio
from fastmcp import Client
from llm_client import LLMClient
from context_builder import ContextBuilder
import re
import json

async def main():
    llm = LLMClient()

    async with Client("http://localhost:8081/sse") as client:
        tools = await client.list_tools()

        print("🔧 Available Tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        # Step 1: Get user query
        user_query = input("\n🗣️ What do you want to ask or do? ")

        # Step 2: Build prompt using context builder
        prompt = ContextBuilder.build_decision_prompt(user_query, tools)
        print("\n📨 Prompt sent to LLM:\n", prompt)

        # Step 3: LLM handles reasoning
        response = llm.query(prompt)
        print("\n🧠 LLM Response:\n", response)

        # Step 4: Parse LLM response for tool calls and invoke MCP tool if needed
        # Try JSON first
        tool_name_map = {
            "add": "add_tool",
            "subtract": "subtract_tool",
            "multiply": "multiply_tool",
            "divide": "divide_tool",
            "get_weather": "weather_tool"
        }
        match = re.search(r"{.*?}", response)
        if match:
            try:
                json_str = match.group().replace("'", '"')
                tool_info = json.loads(json_str)
                llm_tool_name = tool_info.get("tool")
                tool_name = tool_name_map.get(llm_tool_name)
                if tool_name == "weather_tool":
                    city = tool_info.get("location")
                    result = await client.call_tool(tool_name, {"city": city})
                    print(f"\n🌦️ Weather Tool Result for {city}:\n", result.data)
                    return
                if tool_name in ["add_tool", "subtract_tool", "multiply_tool", "divide_tool"]:
                    a = tool_info.get("a")
                    b = tool_info.get("b")
                    result = await client.call_tool(tool_name, {"num1": a, "num2": b})
                    print(f"\n🧮 Math Tool Result:\n", result.data)
                    return
            except Exception as e:
                print("\n⚠️ Error parsing tool call from LLM response:", e)
        # Try Python-style function call for weather
        func_match = re.search(r"get_weather\s*\(\s*location\s*=\s*['\"]([^'\"]+)['\"]\s*\)", response)
        if func_match:
            city = func_match.group(1)
            result = await client.call_tool("weather_tool", {"city": city})
            print(f"\n🌦️ Weather Tool Result for {city}:\n", result.data)
            return
        print("\nℹ️ No tool call detected or tool not available. LLM response shown above.")

asyncio.run(main())
