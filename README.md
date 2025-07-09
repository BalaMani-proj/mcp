# mcp

## Project Overview

mcp is a simple microservice project that demonstrates how to build and expose an API for adding two numbers using Python, Connexion (Flask), and FastMCP. It includes both a REST API and an MCP tool server for interoperability.

## Features
- REST API to add two numbers (with OpenAPI/Swagger UI)
- FastMCP tool server exposing the same functionality
- Example client for calling the MCP tool

## Directory Structure
```
├── src/
│   ├── api/           # REST API logic
│   ├── app/           # Connexion/Flask app
│   ├── mcp_server/    # FastMCP tool server
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

## Example MCP Client
```
cd src
python client.py
```

## API Usage
- **Endpoint:** `/v1/add`
- **Method:** GET
- **Parameters:**
  - `num1` (number, required)
  - `num2` (number, required)
- **Response:** `{ "sum": <number> }`

## License
MIT License