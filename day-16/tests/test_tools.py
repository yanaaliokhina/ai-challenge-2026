"""Tests for built-in demo tools."""

import importlib

import pytest
from tool_registry import _registry, call_tool


@pytest.fixture(autouse=True)
def load_demo_tools():
    """Reload tools module to re-register all demo tools before each test."""
    import tools
    importlib.reload(tools)
    yield
    for name in ("get_current_datetime", "word_count", "celsius_to_fahrenheit"):
        _registry.pop(name, None)


def test_get_current_datetime_is_registered():
    """Verifies the datetime tool is present in the registry."""
    assert "get_current_datetime" in _registry


def test_word_count_is_registered():
    """Verifies the word_count tool is present in the registry."""
    assert "word_count" in _registry


def test_celsius_to_fahrenheit_is_registered():
    """Verifies the celsius_to_fahrenheit tool is present in the registry."""
    assert "celsius_to_fahrenheit" in _registry


def test_get_current_datetime_returns_string():
    """Verifies the datetime tool returns a non-empty string."""
    result = call_tool("get_current_datetime", {})
    assert isinstance(result, str)
    assert len(result) > 0


def test_word_count_counts_correctly():
    """Verifies word_count returns the correct count for a known string."""
    result = call_tool("word_count", {"text": "hello world foo"})
    assert result == "3"


def test_word_count_empty_string():
    """Verifies word_count handles an empty string and returns zero."""
    result = call_tool("word_count", {"text": ""})
    assert result == "0"


def test_word_count_single_word():
    """Verifies word_count handles a single word."""
    result = call_tool("word_count", {"text": "hello"})
    assert result == "1"


def test_celsius_to_fahrenheit_freezing():
    """Verifies 0°C converts to 32°F."""
    result = call_tool("celsius_to_fahrenheit", {"celsius": 0})
    assert float(result) == pytest.approx(32.0)


def test_celsius_to_fahrenheit_boiling():
    """Verifies 100°C converts to 212°F."""
    result = call_tool("celsius_to_fahrenheit", {"celsius": 100})
    assert float(result) == pytest.approx(212.0)


def test_celsius_to_fahrenheit_negative():
    """Verifies negative Celsius values convert correctly."""
    result = call_tool("celsius_to_fahrenheit", {"celsius": -40})
    assert float(result) == pytest.approx(-40.0)


def test_word_count_missing_argument_raises():
    """Verifies word_count raises ValueError when 'text' argument is missing."""
    with pytest.raises(ValueError, match="Missing required arguments"):
        call_tool("word_count", {})


def test_celsius_to_fahrenheit_missing_argument_raises():
    """Verifies celsius_to_fahrenheit raises ValueError when 'celsius' is missing."""
    with pytest.raises(ValueError, match="Missing required arguments"):
        call_tool("celsius_to_fahrenheit", {})
