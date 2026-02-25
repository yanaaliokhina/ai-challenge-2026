import sys
import os
from typing import Optional
import pytest
import httpx
from unittest.mock import patch, MagicMock

from src.client.models import LLMRequest, LLMResponse
from src.client import send_request


MOCK_RESPONSE_BODY = {
    "id": "msg_123",
    "type": "message",
    "role": "assistant",
    "content": [{"type": "text", "text": "A large language model is..."}],
    "model": "claude-sonnet-4-6-20251001",
    "usage": {"input_tokens": 12, "output_tokens": 8},
}


def _make_mock_response(status_code: int = 200, body: Optional[dict] = None) -> MagicMock:
    mock = MagicMock(spec=httpx.Response)
    mock.status_code = status_code
    mock.json.return_value = body or MOCK_RESPONSE_BODY
    mock.text = str(body or MOCK_RESPONSE_BODY)
    return mock


def test_send_request_success(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("httpx.post", return_value=_make_mock_response()) as mock_post:
        request = LLMRequest(model="claude-sonnet-4-6", prompt="Hello", max_tokens=100, temperature=1.0)
        result = send_request(request)

    assert isinstance(result, LLMResponse)
    assert result.content == "A large language model is..."
    assert result.input_tokens == 12
    assert result.output_tokens == 8
    mock_post.assert_called_once()


def test_send_request_missing_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    request = LLMRequest(model="claude-sonnet-4-6", prompt="Hello", max_tokens=100, temperature=1.0)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        send_request(request)


def test_send_request_empty_api_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "   ")
    request = LLMRequest(model="claude-sonnet-4-6", prompt="Hello", max_tokens=100, temperature=1.0)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        send_request(request)


def test_send_request_http_error(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    error_body = {"error": {"type": "authentication_error", "message": "invalid x-api-key"}}
    with patch("httpx.post", return_value=_make_mock_response(status_code=401, body=error_body)):
        request = LLMRequest(model="claude-sonnet-4-6", prompt="Hello", max_tokens=100, temperature=1.0)
        with pytest.raises(RuntimeError, match="401"):
            send_request(request)


def test_send_request_network_error(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("httpx.post", side_effect=httpx.RequestError("connection refused")):
        request = LLMRequest(model="claude-sonnet-4-6", prompt="Hello", max_tokens=100, temperature=1.0)
        with pytest.raises(RuntimeError, match="Network error"):
            send_request(request)


def test_llm_request_fields():
    req = LLMRequest(model="claude-sonnet-4-6", prompt="test", max_tokens=512, temperature=0.5)
    assert req.model == "claude-sonnet-4-6"
    assert req.prompt == "test"
    assert req.max_tokens == 512
    assert req.temperature == 0.5


def test_llm_response_fields():
    resp = LLMResponse(content="hello", model="claude-sonnet-4-6", input_tokens=5, output_tokens=3)
    assert resp.content == "hello"
    assert resp.model == "claude-sonnet-4-6"
    assert resp.input_tokens == 5
    assert resp.output_tokens == 3
