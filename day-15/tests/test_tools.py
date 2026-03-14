"""Tests for built-in tools in tools.py."""

import pytest
from src.tools import calculator, word_count, reverse_string, TOOL_REGISTRY


def test_calculator_simple_addition():
    """Verifies calculator correctly evaluates a simple addition expression."""
    assert calculator("2 + 3") == "5"


def test_calculator_complex_expression():
    """Verifies calculator correctly evaluates a complex arithmetic expression."""
    assert calculator("3 * (4 + 2)") == "18"


def test_calculator_division():
    """Verifies calculator correctly evaluates division."""
    assert calculator("10 / 4") == "2.5"


def test_calculator_power():
    """Verifies calculator correctly evaluates exponentiation."""
    assert calculator("2 ** 8") == "256"


def test_calculator_negative_unary():
    """Verifies calculator handles unary negation."""
    assert calculator("-5 + 3") == "-2"


def test_calculator_invalid_expression():
    """Verifies calculator returns an error string for invalid expressions."""
    result = calculator("import os")
    assert result.startswith("Error:")


def test_calculator_empty_expression():
    """Verifies calculator returns an error for an empty expression."""
    result = calculator("")
    assert result.startswith("Error:")


def test_word_count_normal_sentence():
    """Verifies word_count returns the correct count for a normal sentence."""
    assert word_count("the quick brown fox") == "4"


def test_word_count_single_word():
    """Verifies word_count returns 1 for a single word."""
    assert word_count("hello") == "1"


def test_word_count_empty_string():
    """Verifies word_count returns 0 for an empty string."""
    assert word_count("") == "0"


def test_word_count_extra_spaces():
    """Verifies word_count handles multiple spaces between words."""
    assert word_count("  hello   world  ") == "2"


def test_reverse_string_normal():
    """Verifies reverse_string correctly reverses a normal string."""
    assert reverse_string("hello world") == "dlrow olleh"


def test_reverse_string_single_char():
    """Verifies reverse_string returns same character for single-char input."""
    assert reverse_string("a") == "a"


def test_reverse_string_empty():
    """Verifies reverse_string returns empty string for empty input."""
    assert reverse_string("") == ""


def test_reverse_string_palindrome():
    """Verifies reverse_string on a palindrome returns the same string."""
    assert reverse_string("racecar") == "racecar"


def test_tool_registry_contains_all_tools():
    """Verifies TOOL_REGISTRY contains all three required tools."""
    assert "calculator" in TOOL_REGISTRY
    assert "word_count" in TOOL_REGISTRY
    assert "reverse_string" in TOOL_REGISTRY


def test_tool_registry_callables():
    """Verifies all tools in TOOL_REGISTRY are callable."""
    for name, fn in TOOL_REGISTRY.items():
        assert callable(fn), f"Tool '{name}' is not callable"
