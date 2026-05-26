"""Tests for main.py LLM integration flow."""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.main import select_and_run_tool


def _make_llm_response(tool_name: str, arguments: dict) -> str:
    return json.dumps({"tool_name": tool_name, "arguments": arguments})


def test_select_and_run_tool_word_count():
    """Verifies the full flow selects word_count and returns the correct result."""
    mock_client = MagicMock()
    mock_client.ask.return_value = _make_llm_response("word_count", {"text": "hello world"})

    tool_name, args, result = select_and_run_tool("How many words in 'hello world'?", mock_client)

    assert tool_name == "word_count"
    assert args == {"text": "hello world"}
    assert result == "2"


def test_select_and_run_tool_celsius_to_fahrenheit():
    """Verifies the full flow selects celsius_to_fahrenheit and converts correctly."""
    mock_client = MagicMock()
    mock_client.ask.return_value = _make_llm_response("celsius_to_fahrenheit", {"celsius": 0})

    tool_name, args, result = select_and_run_tool("Convert 0 Celsius to Fahrenheit.", mock_client)

    assert tool_name == "celsius_to_fahrenheit"
    assert float(result) == pytest.approx(32.0)


def test_select_and_run_tool_get_current_datetime():
    """Verifies the full flow selects get_current_datetime and returns a string."""
    mock_client = MagicMock()
    mock_client.ask.return_value = _make_llm_response("get_current_datetime", {})

    tool_name, args, result = select_and_run_tool("What time is it?", mock_client)

    assert tool_name == "get_current_datetime"
    assert isinstance(result, str)


def test_select_and_run_tool_raises_on_invalid_json():
    """Verifies select_and_run_tool raises ValueError when LLM returns non-JSON."""
    mock_client = MagicMock()
    mock_client.ask.return_value = "This is not JSON at all."

    with pytest.raises(ValueError, match="non-JSON"):
        select_and_run_tool("Some prompt.", mock_client)


def test_select_and_run_tool_raises_on_missing_tool_name():
    """Verifies select_and_run_tool raises ValueError when tool_name is absent in LLM response."""
    mock_client = MagicMock()
    mock_client.ask.return_value = json.dumps({"arguments": {}})

    with pytest.raises(ValueError, match="missing 'tool_name'"):
        select_and_run_tool("Some prompt.", mock_client)


def test_select_and_run_tool_raises_on_unknown_tool():
    """Verifies select_and_run_tool propagates ValueError for an unregistered tool name."""
    mock_client = MagicMock()
    mock_client.ask.return_value = _make_llm_response("nonexistent_tool", {})

    with pytest.raises(ValueError, match="Unknown tool"):
        select_and_run_tool("Some prompt.", mock_client)


def test_select_and_run_tool_passes_tool_list_to_llm():
    """Verifies the LLM prompt includes the serialized tool list."""
    mock_client = MagicMock()
    mock_client.ask.return_value = _make_llm_response("word_count", {"text": "hi"})

    select_and_run_tool("Count words.", mock_client)

    call_args = mock_client.ask.call_args[0][0]
    assert "word_count" in call_args
    assert "celsius_to_fahrenheit" in call_args
    assert "get_current_datetime" in call_args
