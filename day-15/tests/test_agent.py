"""Tests for agent loop logic and response parsing in agent.py."""

import pytest
from unittest.mock import MagicMock, patch
from src.agent import parse_response, AgentResponse, ToolCall, build_prompt, run_agent


def test_parse_response_final_answer():
    """Verifies parse_response correctly parses a final_answer JSON response."""
    raw = '{"final_answer": "42"}'
    result = parse_response(raw)
    assert result.final_answer == "42"
    assert result.tool_call is None


def test_parse_response_tool_call():
    """Verifies parse_response correctly parses a tool_call JSON response."""
    raw = '{"tool_call": {"name": "calculator", "argument": "2 + 2"}}'
    result = parse_response(raw)
    assert result.tool_call is not None
    assert result.tool_call.name == "calculator"
    assert result.tool_call.argument == "2 + 2"
    assert result.final_answer is None


def test_parse_response_with_surrounding_text():
    """Verifies parse_response extracts JSON even when surrounded by extra text."""
    raw = 'Sure! {"final_answer": "done"} That is all.'
    result = parse_response(raw)
    assert result.final_answer == "done"


def test_parse_response_no_json_raises():
    """Verifies parse_response raises ValueError when no JSON is present."""
    with pytest.raises(ValueError):
        parse_response("no json here")


def test_parse_response_both_fields_raises():
    """Verifies parse_response raises ValidationError when both fields are set."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        parse_response('{"tool_call": {"name": "calculator", "argument": "1+1"}, "final_answer": "2"}')


def test_parse_response_neither_field_raises():
    """Verifies parse_response raises ValidationError when neither field is set."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        parse_response('{"other_field": "value"}')


def test_build_prompt_no_history():
    """Verifies build_prompt includes the task and no history section when history is empty."""
    prompt = build_prompt("What is 2+2?", [])
    assert "What is 2+2?" in prompt
    assert "History:" not in prompt


def test_build_prompt_with_history():
    """Verifies build_prompt includes the history entries when provided."""
    history = ["Step 1 — Called calculator('2+2') → 4"]
    prompt = build_prompt("What is 2+2?", history)
    assert "History:" in prompt
    assert "Step 1" in prompt


def test_run_agent_final_answer_on_first_step(capsys):
    """Verifies run_agent prints final answer and exits loop on first step."""
    client = MagicMock()
    client.ask.return_value = '{"final_answer": "The answer is 4."}'

    run_agent("What is 2+2?", max_iterations=5, client=client, model="test-model")

    captured = capsys.readouterr()
    assert "Final answer: The answer is 4." in captured.out
    assert client.ask.call_count == 1


def test_run_agent_tool_call_then_final_answer(capsys):
    """Verifies run_agent executes a tool call and continues to a final answer."""
    client = MagicMock()
    client.ask.side_effect = [
        '{"tool_call": {"name": "calculator", "argument": "2 + 2"}}',
        '{"final_answer": "The result is 4."}',
    ]

    run_agent("What is 2+2?", max_iterations=5, client=client, model="test-model")

    captured = capsys.readouterr()
    assert "Tool call: calculator" in captured.out
    assert "Observation: 4" in captured.out
    assert "Final answer: The result is 4." in captured.out
    assert client.ask.call_count == 2


def test_run_agent_max_iterations_reached(capsys):
    """Verifies run_agent prints timeout message when max iterations are exhausted."""
    client = MagicMock()
    client.ask.return_value = '{"tool_call": {"name": "calculator", "argument": "1+1"}}'

    run_agent("Loop forever", max_iterations=3, client=client, model="test-model")

    captured = capsys.readouterr()
    assert "Max iterations reached" in captured.out
    assert client.ask.call_count == 3


def test_run_agent_unknown_tool_produces_error_observation(capsys):
    """Verifies run_agent records an error observation for an unknown tool and continues."""
    client = MagicMock()
    client.ask.side_effect = [
        '{"tool_call": {"name": "nonexistent_tool", "argument": "x"}}',
        '{"final_answer": "I could not use the tool."}',
    ]

    run_agent("Use nonexistent_tool", max_iterations=5, client=client, model="test-model")

    captured = capsys.readouterr()
    assert "unknown tool" in captured.out
    assert "Final answer" in captured.out


def test_run_agent_observation_fed_into_next_iteration():
    """Verifies tool observation is included in the prompt for the next iteration."""
    client = MagicMock()
    client.ask.side_effect = [
        '{"tool_call": {"name": "word_count", "argument": "hello world"}}',
        '{"final_answer": "There are 2 words."}',
    ]

    run_agent("Count words in 'hello world'", max_iterations=5, client=client, model="test-model")

    second_call_prompt = client.ask.call_args_list[1][0][0]
    assert "word_count" in second_call_prompt
    assert "hello world" in second_call_prompt


def test_run_agent_parse_error_continues_loop(capsys):
    """Verifies run_agent continues the loop when LLM returns unparseable output."""
    client = MagicMock()
    client.ask.side_effect = [
        "this is not json at all",
        '{"final_answer": "recovered"}',
    ]

    run_agent("test task", max_iterations=5, client=client, model="test-model")

    captured = capsys.readouterr()
    assert "Parse error" in captured.out
    assert "Final answer: recovered" in captured.out
