mcp_llm_project/
├── .env                        # Secure environment variables (e.g. API keys)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Optional: containerized setup
│
├── llm_client.py               # LLM API handler with retry & logging
├── context_builder.py          # Creates enriched task prompts
├── main.py                     # MCP client orchestrating tools and LLM context
│
├── tests/                      # Unit tests for modular components
│   └── test_prompt_builder.py
│
└── llm_prompt_playground.ipynb # Notebook for tuning LLM prompts

# MCP + LLM Context Enrichment Project

This project integrates [FastMCP](https://github.com/fastmcp/fastmcp) with a Large Language Model (LLM) like OpenAI to enrich task requests with natural language context. It demonstrates how structured prompts and semantic understanding can enhance computation workflows.

---

## 🧠 Features

- MCP client that connects to a tool-based computation server
- Integration with LLMs (OpenAI by default) for context-aware enrichment
- Modular prompt generation and API handling
- Retry logic and logging for resiliency and observability
- `.env` secret management
- Jupyter notebook for prompt tuning and model comparison

---

## 📦 Installation

```bash
git clone https://github.com/your-username/mcp-llm-project
cd mcp_llm_project
pip install -r requirements.txt
