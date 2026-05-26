"""Tool registry for day-16 project."""

from typing import Any, Callable, Dict, List, Optional


_registry: Dict[str, Dict[str, Any]] = {}


def tool(
    name: Optional[str] = None,
    description: str = "",
    parameters: Optional[List[Dict[str, str]]] = None,
) -> Callable:
    """Decorator that registers a function as a named tool."""
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        _registry[tool_name] = {
            "name": tool_name,
            "description": description,
            "parameters": parameters or [],
            "func": func,
        }
        return func
    return decorator


def list_tools() -> List[Dict[str, Any]]:
    """Return all registered tools without the callable, ready for JSON serialization."""
    return [
        {
            "name": entry["name"],
            "description": entry["description"],
            "parameters": entry["parameters"],
        }
        for entry in _registry.values()
    ]


def call_tool(name: str, arguments: Dict[str, Any]) -> str:
    """Dispatch a tool call by name with the given arguments."""
    if name not in _registry:
        raise ValueError(f"Unknown tool: '{name}'. Available tools: {list(_registry.keys())}")

    entry = _registry[name]
    required_params = {p["name"] for p in entry["parameters"]}
    missing = required_params - arguments.keys()
    if missing:
        raise ValueError(f"Missing required arguments for tool '{name}': {missing}")

    result = entry["func"](**arguments)
    return str(result)
