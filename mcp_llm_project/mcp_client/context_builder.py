class ContextBuilder:
    @staticmethod
    def build_decision_prompt(user_query: str, tools: list) -> str:
        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in tools]
        )

        return (
            f"You are a helpful math assistant. The user asked:\n"
            f"{user_query}\n\n"
            f"Available tools:\n{tool_descriptions}\n\n"
            "Always use tool. "
            "If you use a tool, explain why. If no tool fits the task, answer directly. "
            "Do not hallucinate tool capabilities. give prefence for available tool."
        )
