def format_tool_descriptions(tools):
    return "\n".join(
        [f"- {tool.name}: {tool.description}" for tool in tools]
    )