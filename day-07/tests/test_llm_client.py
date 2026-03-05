"""Tests for the LLMClient module."""

from unittest.mock import MagicMock, patch

import pytest

from src.llm_client import LLMClient


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    return LLMClient(model="claude-haiku-4-5-20251001")


def _mock_response(text: str) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = {"content": [{"text": text}]}
    mock.raise_for_status.return_value = None
    return mock


def test_ask_returns_response_text(client):
    """Verifies that ask() returns the text from the LLM response."""
    with patch("llm_client.httpx.post", return_value=_mock_response("Hello back")):
        text, _ = client.ask("Hello")
    assert text == "Hello back"


def test_ask_returns_positive_latency(client):
    """Verifies that ask() returns a non-negative latency value in milliseconds."""
    with patch("llm_client.httpx.post", return_value=_mock_response("ok")):
        _, latency_ms = client.ask("ping")
    assert latency_ms >= 0


def test_ask_raises_on_http_error(client):
    """Verifies that ask() propagates HTTP errors raised by httpx."""
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("HTTP 429")
    with patch("llm_client.httpx.post", return_value=mock):
        with pytest.raises(Exception, match="HTTP 429"):
            client.ask("fail prompt")


def test_ask_sends_correct_model(client):
    """Verifies that ask() sends the model specified at construction time."""
    with patch("llm_client.httpx.post", return_value=_mock_response("ok")) as mock_post:
        client.ask("test")
    payload = mock_post.call_args[1]["json"]
    assert payload["model"] == "claude-haiku-4-5-20251001"


def test_ask_sends_prompt_in_messages(client):
    """Verifies that ask() includes the prompt in the messages payload."""
    with patch("llm_client.httpx.post", return_value=_mock_response("ok")) as mock_post:
        client.ask("my test prompt")
    payload = mock_post.call_args[1]["json"]
    assert payload["messages"][0]["content"] == "my test prompt"


def test_ask_uses_api_key_from_env(monkeypatch):
    """Verifies that LLMClient reads the API key from the ANTHROPIC_API_KEY env var."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret-key-xyz")
    c = LLMClient(model="claude-haiku-4-5-20251001")
    with patch("llm_client.httpx.post", return_value=_mock_response("ok")) as mock_post:
        c.ask("prompt")
    headers = mock_post.call_args[1]["headers"]
    assert headers["x-api-key"] == "secret-key-xyz"
