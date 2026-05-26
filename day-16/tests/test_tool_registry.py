"""Tests for tool_registry module."""

import pytest
from src.tool_registry import _registry, call_tool, list_tools, tool


@pytest.fixture(autouse=True)
def clean_registry():
    """Clear the registry before each test to avoid cross-test pollution."""
    original = dict(_registry)
    _registry.clear()
    yield
    _registry.clear()
    _registry.update(original)


def test_tool_decorator_registers_function():
    """Verifies that @tool adds the function to the registry with correct metadata."""
    @tool(description="A test tool.", parameters=[])
    def my_tool():
        return "ok"

    assert "my_tool" in _registry
    assert _registry["my_tool"]["description"] == "A test tool."
    assert _registry["my_tool"]["parameters"] == []


def test_tool_decorator_uses_explicit_name():
    """Verifies that an explicit name overrides the function name in the registry."""
    @tool(name="custom_name", description="Custom.", parameters=[])
    def some_func():
        return "x"

    assert "custom_name" in _registry
    assert "some_func" not in _registry


def test_tool_decorator_preserves_callable():
    """Verifies that decorated functions remain callable and return original values."""
    @tool(description="Returns 42.", parameters=[])
    def answer():
        return 42

    assert answer() == 42


def test_list_tools_returns_all_registered():
    """Verifies list_tools() returns one entry per registered tool."""
    @tool(description="Tool A.", parameters=[])
    def tool_a():
        return "a"

    @tool(description="Tool B.", parameters=[])
    def tool_b():
        return "b"

    result = list_tools()
    names = [t["name"] for t in result]
    assert "tool_a" in names
    assert "tool_b" in names


def test_list_tools_excludes_callable():
    """Verifies list_tools() output does not include the 'func' key."""
    @tool(description="No func key.", parameters=[])
    def my_tool():
        return "x"

    for entry in list_tools():
        assert "func" not in entry


def test_list_tools_is_json_serializable():
    """Verifies that list_tools() output can be serialized to JSON without errors."""
    import json

    @tool(description="Serializable.", parameters=[{"name": "x", "type": "string", "description": "An arg."}])
    def serializable_tool(x: str):
        return x

    json.dumps(list_tools())


def test_call_tool_dispatches_correctly():
    """Verifies call_tool() invokes the right function and returns a string result."""
    @tool(description="Adds two numbers.", parameters=[
        {"name": "a", "type": "number", "description": "First."},
        {"name": "b", "type": "number", "description": "Second."},
    ])
    def adder(a: int, b: int):
        return a + b

    result = call_tool("adder", {"a": 3, "b": 4})
    assert result == "7"


def test_call_tool_returns_string():
    """Verifies call_tool() always returns a str, even for numeric results."""
    @tool(description="Returns pi.", parameters=[])
    def pi_tool():
        return 3.14

    result = call_tool("pi_tool", {})
    assert isinstance(result, str)


def test_call_tool_raises_for_unknown_tool():
    """Verifies call_tool() raises ValueError for an unregistered tool name."""
    with pytest.raises(ValueError, match="Unknown tool"):
        call_tool("nonexistent_tool", {})


def test_call_tool_raises_for_missing_arguments():
    """Verifies call_tool() raises ValueError when required arguments are absent."""
    @tool(description="Needs x.", parameters=[{"name": "x", "type": "string", "description": "Required."}])
    def needs_x(x: str):
        return x

    with pytest.raises(ValueError, match="Missing required arguments"):
        call_tool("needs_x", {})


def test_call_tool_passes_extra_kwargs_through():
    """Verifies call_tool() passes only provided arguments to the function."""
    @tool(description="Uses x and y.", parameters=[
        {"name": "x", "type": "number", "description": "x"},
        {"name": "y", "type": "number", "description": "y"},
    ])
    def multiply(x: float, y: float):
        return x * y

    result = call_tool("multiply", {"x": 3.0, "y": 5.0})
    assert result == "15.0"
