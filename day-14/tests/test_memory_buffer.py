"""Tests for the MemoryBuffer class."""

import pytest
from src.memory_buffer import MemoryBuffer


def test_append_user_message_adds_to_buffer():
    """Verifies that appending a user message stores it in the buffer."""
    buf = MemoryBuffer(max_turns=10)
    buf.append("user", "Hello")
    assert buf.get_messages() == [{"role": "user", "content": "Hello"}]


def test_append_preserves_insertion_order():
    """Verifies that messages are stored in insertion order."""
    buf = MemoryBuffer(max_turns=10)
    buf.append("user", "first")
    buf.append("assistant", "second")
    buf.append("user", "third")
    msgs = buf.get_messages()
    assert msgs[0]["content"] == "first"
    assert msgs[1]["content"] == "second"
    assert msgs[2]["content"] == "third"


def test_sliding_window_drops_oldest_pair_when_limit_exceeded():
    """Verifies that the oldest user+assistant pair is dropped when max_turns is exceeded."""
    buf = MemoryBuffer(max_turns=2)
    buf.append("user", "turn1-user")
    buf.append("assistant", "turn1-assistant")
    buf.append("user", "turn2-user")
    buf.append("assistant", "turn2-assistant")
    buf.append("user", "turn3-user")
    buf.append("assistant", "turn3-assistant")
    msgs = buf.get_messages()
    assert len(msgs) == 4
    assert msgs[0]["content"] == "turn2-user"
    assert msgs[1]["content"] == "turn2-assistant"


def test_sliding_window_max_turns_1_keeps_only_last_pair():
    """Verifies that max_turns=1 keeps only the single most recent turn pair."""
    buf = MemoryBuffer(max_turns=1)
    buf.append("user", "old")
    buf.append("assistant", "old reply")
    buf.append("user", "new")
    buf.append("assistant", "new reply")
    msgs = buf.get_messages()
    assert len(msgs) == 2
    assert msgs[0]["content"] == "new"
    assert msgs[1]["content"] == "new reply"


def test_clear_resets_buffer_to_empty():
    """Verifies that /clear empties the message buffer."""
    buf = MemoryBuffer(max_turns=10)
    buf.append("user", "hello")
    buf.append("assistant", "hi")
    buf.clear()
    assert buf.get_messages() == []


def test_clear_does_not_remove_system_prompt():
    """Verifies that clearing the buffer preserves the system prompt property."""
    buf = MemoryBuffer(max_turns=10, system_prompt="You are a pirate.")
    buf.append("user", "hello")
    buf.clear()
    assert buf.system_prompt == "You are a pirate."
    assert buf.get_messages() == []


def test_system_prompt_is_none_by_default():
    """Verifies that system_prompt is None when not provided."""
    buf = MemoryBuffer(max_turns=10)
    assert buf.system_prompt is None


def test_system_prompt_stored_correctly():
    """Verifies that the system prompt is stored and returned unchanged."""
    buf = MemoryBuffer(max_turns=10, system_prompt="Be concise.")
    assert buf.system_prompt == "Be concise."


def test_get_messages_returns_copy():
    """Verifies that mutating the returned list does not affect the internal buffer."""
    buf = MemoryBuffer(max_turns=10)
    buf.append("user", "hello")
    msgs = buf.get_messages()
    msgs.clear()
    assert len(buf.get_messages()) == 1


def test_empty_buffer_returns_empty_list():
    """Verifies that get_messages returns an empty list on a fresh buffer."""
    buf = MemoryBuffer(max_turns=10)
    assert buf.get_messages() == []


def test_trim_only_drops_complete_pairs():
    """Verifies that a partial turn (only user, no assistant yet) is not trimmed prematurely."""
    buf = MemoryBuffer(max_turns=1)
    buf.append("user", "turn1-user")
    buf.append("assistant", "turn1-assistant")
    buf.append("user", "turn2-user")
    msgs = buf.get_messages()
    assert len(msgs) == 3
