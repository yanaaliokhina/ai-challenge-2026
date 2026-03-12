"""Tests for the interactive chat loop in main.py."""

import pytest
from unittest.mock import MagicMock, patch
from src.memory_buffer import MemoryBuffer
from src.main import run_chat


def _make_client(reply: str = "ok") -> MagicMock:
    client = MagicMock()
    client.chat.return_value = reply
    return client


def test_run_chat_exit_command_prints_goodbye(capsys):
    """Verifies that typing 'exit' prints Goodbye. and stops the loop."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client()
    with patch("builtins.input", side_effect=["exit"]):
        run_chat(buf, client)
    assert "Goodbye." in capsys.readouterr().out


def test_run_chat_quit_command_prints_goodbye(capsys):
    """Verifies that typing 'quit' prints Goodbye. and stops the loop."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client()
    with patch("builtins.input", side_effect=["quit"]):
        run_chat(buf, client)
    assert "Goodbye." in capsys.readouterr().out


def test_run_chat_keyboard_interrupt_prints_goodbye(capsys):
    """Verifies that KeyboardInterrupt is caught and prints Goodbye."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client()
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        run_chat(buf, client)
    assert "Goodbye." in capsys.readouterr().out


def test_run_chat_user_message_appended_to_buffer():
    """Verifies that a user message is added to the buffer before the LLM call."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client("pong")
    with patch("builtins.input", side_effect=["ping", "exit"]):
        run_chat(buf, client)
    msgs = buf.get_messages()
    assert any(m["role"] == "user" and m["content"] == "ping" for m in msgs)


def test_run_chat_assistant_reply_appended_to_buffer():
    """Verifies that the assistant reply is stored in the buffer after the LLM call."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client("pong")
    with patch("builtins.input", side_effect=["ping", "exit"]):
        run_chat(buf, client)
    msgs = buf.get_messages()
    assert any(m["role"] == "assistant" and m["content"] == "pong" for m in msgs)


def test_run_chat_clear_command_resets_buffer(capsys):
    """Verifies that /clear empties the buffer and prints [Memory cleared]."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client()
    with patch("builtins.input", side_effect=["hello", "/clear", "exit"]):
        run_chat(buf, client)
    assert buf.get_messages() == []
    assert "[Memory cleared]" in capsys.readouterr().out


def test_run_chat_history_command_prints_messages(capsys):
    """Verifies that /history prints all buffered messages with role prefixes."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client("world")
    with patch("builtins.input", side_effect=["hello", "/history", "exit"]):
        run_chat(buf, client)
    out = capsys.readouterr().out
    assert "[user]: hello" in out
    assert "[assistant]: world" in out


def test_run_chat_empty_input_is_skipped():
    """Verifies that empty input lines do not trigger an LLM call."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client()
    with patch("builtins.input", side_effect=["", "exit"]):
        run_chat(buf, client)
    client.chat.assert_not_called()


def test_run_chat_passes_system_prompt_to_client():
    """Verifies that the system prompt is forwarded to LLMClient.chat() on each turn."""
    buf = MemoryBuffer(max_turns=10, system_prompt="Be a pirate.")
    client = _make_client("Arr!")
    with patch("builtins.input", side_effect=["hello", "exit"]):
        run_chat(buf, client)
    _, kwargs = client.chat.call_args
    assert kwargs.get("system") == "Be a pirate."


def test_run_chat_history_empty_when_buffer_cleared(capsys):
    """Verifies that /history after /clear prints nothing."""
    buf = MemoryBuffer(max_turns=10)
    client = _make_client()
    with patch("builtins.input", side_effect=["hello", "/clear", "/history", "exit"]):
        run_chat(buf, client)
    out = capsys.readouterr().out
    assert "[user]" not in out.split("[Memory cleared]")[1]
