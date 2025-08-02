from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv
import asyncio
from fastmcp import Client
import re
import json

load_dotenv()

class LLMClient:
    def __init__(self):
        self.model_id = os.getenv("HF_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
        print(f"🔍 Using model: {self.model_id}")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id).to(self.device)

    def normalize_question(self, q):
        q = q.lower().strip()
        q = re.sub(r'[^\w\s]', '', q)  # remove punctuation
        return q

    def format_tool_descriptions(self, tools):
        return "\n".join([
            f"{i+1}. **{t.name}**\n   - Description: {t.description}\n   - Inputs: {', '.join(t.inputSchema.keys())}"
            for i, t in enumerate(tools)
        ])

    def build_system_prompt(self, tools):
        tool_descriptions = self.format_tool_descriptions(tools)
        examples = (
            "- User: \"What's 5 plus 3?\" → Call `add` with `a=5`, `b=3`\n"
            "- User: \"Can you tell me the weather in Tokyo?\" → Call `get_weather` with `location=\"Tokyo\"`\n"
            "- User: \"What’s the capital of France?\" → Respond directly: \"The capital of France is Paris.\"\n"
            "- User: \"Subtract 10 from 25\" → Call `subtract` with `a=25`, `b=10`\n"
            "- User: \"Multiply 7 and 8\" → Call `multiply` with `a=7`, `b=8`\n"
            "- User: \"What's the weather like in Mumbai?\" → Call `get_weather` with `location=\"Mumbai\"`"
        )
        return (
            "You are a helpful assistant with access to tools via the Model Context Protocol (MCP).\n"
            "Use tools when needed to answer user questions. If a tool is not required, respond directly.\n\n"
            f"Available tools:\n\n{tool_descriptions}\n\n"
            f"Examples:\n{examples}\n\n"
            "Always return a valid JSON object when using tools, like:\n"
            "{ \"tool\": \"add\", \"a\": 5, \"b\": 3 }\n"
            "Avoid natural language or Python-style syntax."
        )

    def classify_tool(self, question, tools):
        normalized_q = self.normalize_question(question)
        system = self.build_system_prompt(tools)

        print("\n--- SYSTEM PROMPT TO LLM ---\n", system)
        print("--- USER QUESTION ---\n", normalized_q)

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": normalized_q}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=1.0,
            do_sample=False
        )
        output = self.tokenizer.decode(output_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        print("--- RAW LLM RESPONSE ---\n", output.strip())
        return output.strip()

    def query(self, prompt):
        messages = [
            {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        output_ids = self.model.generate(**inputs, max_new_tokens=256)
        output = self.tokenizer.decode(output_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return output.strip()

    def extract_questions(self, prompt):
        system = (
            "You are a helpful assistant. Split the following prompt into clear, separate questions. "
            "Return each question on a new line."
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        output_ids = self.model.generate(**inputs, max_new_tokens=512)
        output = self.tokenizer.decode(output_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return [q.strip() for q in output.split('\n') if q.strip()]

async def process_prompt(prompt):
    llm = LLMClient()
    questions = llm.extract_questions(prompt)
    results = []

    async with Client("http://localhost:8081/sse") as client:
        tools = await client.list_tools()
        tool_name_map = {
            "add": "add_tool",
            "subtract": "subtract_tool",
            "multiply": "multiply_tool",
            "divide": "divide_tool",
            "get_weather": "weather_tool",
            "getNotes": "get_notes_tool",  # Add dynamic tools here
            "getNote": "get_note_tool"
        }

        for q in questions:
            q = q.strip()
            if not q:
                continue

            llm_response = llm.classify_tool(q, tools)

            # 🔍 Robust JSON extraction block
            tool_info = None
            match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if match:
                json_str = match.group(0).replace("“", "\"").replace("”", "\"").replace("'", "\"")
                try:
                    tool_info = json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing error: {e}")
            else:
                print("⚠️ No JSON block found in LLM response.")

            # 🔁 Retry with clarification if needed
            if not tool_info or "tool" not in tool_info:
                clarification_prompt = f"Please return a valid JSON object for tool invocation based on: '{q}'"
                clarified_response = llm.query(clarification_prompt)
                match = re.search(r'\{.*\}', clarified_response, re.DOTALL)
                if match:
                    json_str = match.group(0).replace("“", "\"").replace("”", "\"").replace("'", "\"")
                    try:
                        tool_info = json.loads(json_str)
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Retry JSON parsing failed: {e}")

            if not tool_info or "tool" not in tool_info:
                results.append(f"{q}: {llm.query(q)}")
                continue

            llm_tool_name = tool_info.get("tool")
            tool_name = tool_name_map.get(llm_tool_name)
            selected_tool = next((t for t in tools if t.name == tool_name), None)

            if not selected_tool:
                results.append(f"{q}: Tool '{tool_name}' not available on server.")
                continue

            try:
                if tool_name == "weather_tool":
                    city = tool_info.get("location")
                    result = await client.call_tool(tool_name, {"city": city})
                    results.append(f"{q}: {result.data}")
                elif tool_name in ["add_tool", "subtract_tool", "multiply_tool", "divide_tool"]:
                    a = tool_info.get("a")
                    b = tool_info.get("b")
                    arg_names = list(selected_tool.inputSchema.keys())
                    args = {arg_names[0]: a, arg_names[1]: b}
                    result = await client.call_tool(tool_name, args)
                    results.append(f"{q}: {result.data}")
                elif tool_name in ["get_notes_tool", "get_note_tool"]:
                    result = await client.call_tool(tool_name, tool_info.get("params", {}))
                    results.append(f"{q}: {result.data}")
                else:
                    results.append(f"{q}: Tool mapping not found.")
            except Exception as e:
                results.append(f"{q}: Tool invocation failed: {str(e)}")

    return "\n".join(results)