"""Tests for llm_client.py — verifies HTTP interaction and error handling."""

import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from llm_client import LLMClient
from constants import ANTHROPIC_API_VERSION, DEFAULT_MODEL, MAX_TOKENS


def _make_response(text: str, status_code: int = 200) -> MagicMock:
    """Build a mock httpx response."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = {"content": [{"text": text}]}
    mock.text = json.dumps({"error": "bad"})
    return mock


@pytest.fixture()
def client(monkeypatch):
    """LLMClient with a fake API key injected via environment."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    return LLMClient()


def test_init_raises_when_api_key_missing(monkeypatch):
    """LLMClient raises RuntimeError when ANTHROPIC_API_KEY is not set."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        LLMClient()


def test_ask_returns_text(client):
    """ask() returns the text from the first content block."""
    mock_resp = _make_response("Hello there!")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        result = client.ask("Hi")
    assert result == "Hello there!"


def test_ask_sends_correct_headers(client):
    """ask() sends x-api-key, anthropic-version, and content-type headers."""
    mock_resp = _make_response("ok")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        client.ask("Hi")
    _, kwargs = mock_post.call_args
    headers = kwargs["headers"]
    assert headers["x-api-key"] == "test-key"
    assert headers["anthropic-version"] == ANTHROPIC_API_VERSION
    assert headers["content-type"] == "application/json"


def test_ask_uses_default_model_when_none_passed(client):
    """ask() uses DEFAULT_MODEL when model argument is None."""
    mock_resp = _make_response("ok")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        client.ask("Hi")
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["model"] == DEFAULT_MODEL


def test_ask_uses_provided_model(client):
    """ask() uses the caller-supplied model name."""
    mock_resp = _make_response("ok")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        client.ask("Hi", model="claude-opus-4-6")
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["model"] == "claude-opus-4-6"


def test_ask_sends_max_tokens(client):
    """ask() sends MAX_TOKENS in the request body."""
    mock_resp = _make_response("ok")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        client.ask("Hi")
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["max_tokens"] == MAX_TOKENS


def test_ask_includes_system_when_provided(client):
    """ask() includes the system key when a system prompt is given."""
    mock_resp = _make_response("ok")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        client.ask("Hi", system="You are helpful")
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["system"] == "You are helpful"


def test_ask_omits_system_when_none(client):
    """ask() does not include the system key when system is None."""
    mock_resp = _make_response("ok")
    with patch("llm_client.httpx.post", return_value=mock_resp) as mock_post:
        client.ask("Hi")
    _, kwargs = mock_post.call_args
    assert "system" not in kwargs["json"]


def test_ask_raises_on_non_200(client):
    """ask() raises RuntimeError with status code on non-2xx responses."""
    mock_resp = _make_response("", status_code=401)
    with patch("llm_client.httpx.post", return_value=mock_resp):
        with pytest.raises(RuntimeError, match="401"):
            client.ask("Hi")


def test_ask_raises_on_500(client):
    """ask() raises RuntimeError on a 500 server error."""
    mock_resp = _make_response("", status_code=500)
    with patch("llm_client.httpx.post", return_value=mock_resp):
        with pytest.raises(RuntimeError, match="500"):
            client.ask("Hi")
