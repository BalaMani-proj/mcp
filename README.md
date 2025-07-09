# mcp

## Project Overview

mcp is a demonstration project for the Model Context Protocol (MCP), showcasing how to build interoperable microservices and tools using Python. The project provides both a REST API and an MCP tool server, allowing clients to interact with the service via standard HTTP or the MCP protocol. It includes example implementations of an MCP server, a REST API, and a client that consumes MCP tools.

## What is Model Context Protocol (MCP)?

Model Context Protocol (MCP) is a protocol for exposing and consuming tools and resources in a standardized way, enabling interoperability between different services and clients. MCP allows you to define tools (such as functions or APIs) and resources (such as data or models) that can be discovered and invoked by clients.

## Features
- REST API to add two numbers (with OpenAPI/Swagger UI)
- MCP tool server exposing the same add functionality as an MCP tool
- Example MCP client for discovering and invoking MCP tools
- Demonstrates how to define, expose, and consume MCP tools and resources

## Directory Structure
```
├── src/
│   ├── api/           # REST API logic
│   ├── app/           # Connexion/Flask app
│   ├── mcp_server/    # FastMCP tool server (MCP implementation)
│   ├── client.py      # Example MCP client
│   └── openapi.yaml   # OpenAPI spec
├── requirements.txt   # Python dependencies
├── setup.bat          # Windows setup script
```

## Setup
1. Clone the repository.
2. Run `setup.bat` (Windows) or manually create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

## Running the REST API
```
cd src/app
python app.py
```
- The API will be available at `http://localhost:8080/v1/add?num1=1&num2=2`
- Swagger UI: `http://localhost:8080/ui/`

## Running the MCP Tool Server
```
cd src/mcp_server
python server.py
```
- The MCP server will listen on `http://localhost:8081/sse`
- The server exposes the `add` tool as an MCP tool, which can be discovered and invoked by MCP clients.

## Example MCP Client
```
cd src
python client.py
```
- The client demonstrates how to discover and invoke MCP tools (such as the `add` tool) from the MCP server.

## Tools and Resources
- **Tools:** The MCP server exposes the `add` tool, which takes two numbers and returns their sum. Tools are defined according to the MCP specification and can be discovered by clients.
- **Resources:** The project can be extended to expose additional resources (such as models or datasets) via MCP.

## API Usage
- **Endpoint:** `/v1/add`
- **Method:** GET
- **Parameters:**
  - `num1` (number, required)
  - `num2` (number, required)
- **Response:** `{ "sum": <number> }`

## License
MIT License