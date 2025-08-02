import json
import inspect

def register_openapi_tools(mcp, swagger_path):
    """
    Register MCP tools for all endpoints in a swagger.json file.
    Args:
        mcp: FastMCP instance
        swagger_path: Path to swagger.json file
    Returns:
        List of tool descriptions for system prompt
    """
    with open(swagger_path, "r") as f:
        spec = json.load(f)
    tools_summary = []
    paths = spec.get("paths", {})
    parameters_def = spec.get("parameters", {})
    def resolve_param(p):
        if "$ref" in p:
            ref = p["$ref"]
            if ref.startswith("#/parameters/"):
                pname = ref.split("/")[-1]
                return parameters_def.get(pname, {})
            else:
                return {}
        return p
    for path, methods in paths.items():
        for method, details in methods.items():
            op_id = details.get("operationId") or f"{method}_{path.replace('/', '_')}"
            description = details.get("description", "")
            params = details.get("parameters", [])
            input_args = {}
            for p in params:
                param = resolve_param(p)
                pname = param.get("name")
                ptype = param.get("type", "string")
                if pname:
                    input_args[pname] = ptype
            # Create tool function
            def make_tool(path, method, input_args):
                def tool_func(**kwargs):
                    import requests
                    url = spec.get("host", "localhost:8080")
                    base_path = spec.get("basePath", "")
                    full_url = f"http://{url}{base_path}{path}"
                    # Replace path params
                    for k, v in kwargs.items():
                        full_url = full_url.replace(f"{{{k}}}", str(v))
                    # Query params
                    if method.lower() == "get":
                        resp = requests.get(full_url, params=kwargs)
                    else:
                        resp = requests.request(method.upper(), full_url, json=kwargs)
                    try:
                        return resp.json()
                    except Exception:
                        return {"response": resp.text}
                # Set signature
                sig = inspect.Signature([
                    inspect.Parameter(k, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                    for k in input_args.keys()
                ])
                tool_func.__signature__ = sig
                return tool_func
            tool_func = make_tool(path, method, input_args)
            mcp.tool(name=op_id, description=description or f"Auto-generated tool for {method.upper()} {path}")(tool_func)
            tools_summary.append({
                "name": op_id,
                "description": description,
                "inputs": input_args
            })
    return tools_summary

def format_tools_for_prompt(tools_summary):
    """
    Format tool descriptions for system prompt.
    """
    lines = []
    for tool in tools_summary:
        lines.append(f"- {tool['name']}: {tool['description']} Inputs: {tool['inputs']}")
    return "\n".join(lines)