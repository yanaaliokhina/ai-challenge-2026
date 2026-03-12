"""Tests for LLMClient.chat() — all HTTP calls are mocked."""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.llm_client import LLMClient


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    """Set a fake API key for all tests in this module."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")


def _mock_response(text: str) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = {"content": [{"text": text}]}
    mock.raise_for_status.return_value = None
    return mock


def test_chat_sends_messages_and_returns_reply():
    """Verifies that chat() posts messages and returns the assistant text."""
    with patch("llm_client.httpx.post") as mock_post:
        mock_post.return_value = _mock_response("Hello back!")
        client = LLMClient()
        result = client.chat([{"role": "user", "content": "Hello"}])
    assert result == "Hello back!"


def test_chat_includes_system_prompt_in_payload():
    """Verifies that the system prompt is included in the request payload when provided."""
    with patch("llm_client.httpx.post") as mock_post:
        mock_post.return_value = _mock_response("Arr!")
        client = LLMClient()
        client.chat([{"role": "user", "content": "Hi"}], system="You are a pirate.")
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["system"] == "You are a pirate."


def test_chat_omits_system_key_when_not_provided():
    """Verifies that 'system' key is absent from payload when system=None."""
    with patch("llm_client.httpx.post") as mock_post:
        mock_post.return_value = _mock_response("Hi")
        client = LLMClient()
        client.chat([{"role": "user", "content": "Hi"}])
    _, kwargs = mock_post.call_args
    assert "system" not in kwargs["json"]


def test_chat_sends_full_message_history():
    """Verifies that the complete messages list is forwarded to the API."""
    messages = [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "reply"},
        {"role": "user", "content": "second"},
    ]
    with patch("llm_client.httpx.post") as mock_post:
        mock_post.return_value = _mock_response("answer")
        client = LLMClient()
        client.chat(messages)
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["messages"] == messages


def test_chat_raises_on_http_error():
    """Verifies that HTTP errors from the API are propagated."""
    with patch("llm_client.httpx.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = Exception("HTTP 500")
        client = LLMClient()
        with pytest.raises(Exception, match="HTTP 500"):
            client.chat([{"role": "user", "content": "test"}])
