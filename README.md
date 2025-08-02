# 🧠 MCP LLM Project for Insurance P&C (Guidewire)

This project demonstrates how to build a Model Context Protocol (MCP) server for the Insurance Property & Casualty (P&C) domain, specifically for Guidewire REST APIs. It dynamically registers tools from an OpenAPI (Swagger) spec and enables prompt-based tool invocation using a configurable LLM (default: `Qwen2.5-0.5B-Instruct`, but can be replaced with OpenAI GPT, Claude Sonnet, or other models).

---

## 🚀 Features

- MCP server with arithmetic and weather tools
- Dynamic tool registration from Guidewire Swagger/OpenAPI spec (Insurance P&C domain)
- LLM client parses natural language and invokes tools
- LLM model is configurable: use Qwen, OpenAI GPT, Claude Sonnet, or any Hugging Face model
- Robust JSON parsing and fallback handling
- SSE transport for real-time tool calls

---

## 📁 Project Structure

```
mcp_llm_project/
├── server.py                 # MCP server with tool registration
├── openapi_to_mcp_tools.py   # Converts Swagger spec to MCP tools
├── myswagger.json            # Guidewire Swagger 2.0 spec for Notes API (Insurance P&C)
├── llm_client.py             # LLM client that classifies prompts and invokes tools
├── .env                      # Environment config (e.g., HF_MODEL)
└── README.md                 # Project documentation
```

---

## 🛠 Tools Registered

### Static Tools

- `add_tool`: Performs basic arithmetic addition (num1, num2)
- `subtract_tool`: Performs basic arithmetic subtraction (num1, num2)
- `multiply_tool`: Performs basic arithmetic multiplication (num1, num2)
- `divide_tool`: Performs basic arithmetic division (num1, num2)
- `weather_tool`: Fetches weather using Open-Meteo API (city)

### Dynamic Tools (from Guidewire Swagger)

- `getNotes`: Retrieves notes for a given insurance claim number. If a user prompt mentions a claim or claimNumber, the LLM will extract the value and invoke this tool with the claimNumber parameter. This enables dynamic retrieval of claim-related notes based on natural language input.
- `getNote`: Retrieves details for a specific note (activityId)
- `generateDocs`: Returns Swagger schema

---

## 🤖 Prompt Design & LLM Behavior

The LLM client is designed to:
- Parse user prompts for intent and parameters
- Automatically select the correct tool (e.g., if a prompt mentions "claim" or "claim number", it will call `getNotes` and extract the claimNumber)
- Pass extracted parameters to the tool and return the result

**Example Prompts:**
- "Get me the claim notes for claim 222323435" → invokes `getNotes` with claimNumber=222323435
- "What's 5 plus 3?" → invokes `add_tool` with num1=5, num2=3
- "What's the weather in Tokyo?" → invokes `weather_tool` with city="Tokyo"
- "Subtract 10 from 25" → invokes `subtract_tool` with num1=25, num2=10

---

## ⚙️ Setup Instructions

1. Clone the Repo

```bash
git clone https://github.com/BalaMani-proj/mcp.git
cd mcp/mcp_llm_project
pip install -r requirements.txt
```

2. Create a `.env` file:
```
HF_MODEL=Qwen/Qwen2.5-0.5B-Instruct  # Or set to OpenAI, Claude, or any supported model
```

3. Run MCP server:
```
python server.py
```

4. Run LLM client:
```python
from llm_client import process_prompt
import asyncio
prompt = "Get me the claim notes for claim 222323435"
result = asyncio.run(process_prompt(prompt))
print(result)
```

---

## 🧠 How It Works

- The MCP server loads the Guidewire Swagger spec and registers all endpoints as tools.
- The LLM client analyzes user prompts, extracts relevant parameters (e.g., claim number), and invokes the correct tool.
- This enables natural language access to Insurance P&C APIs, making it easy to retrieve claim notes, note details, and more.

---

## 🏢 Domain Context

This solution is tailored for the Insurance Property & Casualty (P&C) domain and works with Guidewire REST APIs. The provided `myswagger.json` is a sample Guidewire Notes API spec, but the approach can be extended to other Guidewire modules and insurance APIs.

---

## 📝 Example Prompts
- What's 5 plus 3?
- Get me the claim notes for claim 222323435
- What's the weather in Tokyo?
- Subtract 10 from 25

---

## 🛡️ Error Handling
- Malformed JSON from LLM is retried with clarification
- Missing tools are logged and skipped
- Division by zero is gracefully handled

---

## 📌 Notes
- Uses Qwen2.5-0.5B-Instruct for local inference by default, but you can configure any LLM (OpenAI GPT, Claude Sonnet, Hugging Face, etc.)
- Compatible with other Hugging Face models
- Swagger spec must follow OpenAPI v2.0

---

