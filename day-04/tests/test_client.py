"""Tests for AsyncLLMClient."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.client import AsyncLLMClient, DEFAULT_MODEL, DEFAULT_MAX_TOKENS


def _make_mock_cm(mock_http_client):
    """Return an async context manager mock that yields mock_http_client."""
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_http_client)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def test_ask_returns_response_text_on_success():
    """Verifies ask() extracts and returns the text field from a successful API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"content": [{"text": "Hello there!"}]}
    mock_response.raise_for_status = MagicMock()

    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=mock_response)

    async def inner():
        with patch("client.httpx.AsyncClient", return_value=_make_mock_cm(mock_http)):
            result = await AsyncLLMClient(api_key="test-key").ask("What is 2+2?")
        assert result == "Hello there!"

    asyncio.run(inner())


def test_ask_raises_on_http_error():
    """Verifies ask() propagates HTTP errors raised by raise_for_status."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "401", request=MagicMock(), response=MagicMock()
    )

    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=mock_response)

    async def inner():
        with patch("client.httpx.AsyncClient", return_value=_make_mock_cm(mock_http)):
            with pytest.raises(httpx.HTTPStatusError):
                await AsyncLLMClient(api_key="test-key").ask("fail")

    asyncio.run(inner())


def test_ask_sends_correct_headers_and_payload():
    """Verifies ask() sends the API key, version header, model, max_tokens, and message."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"content": [{"text": "ok"}]}
    mock_response.raise_for_status = MagicMock()

    mock_http = AsyncMock()
    mock_http.post = AsyncMock(return_value=mock_response)

    async def inner():
        with patch("client.httpx.AsyncClient", return_value=_make_mock_cm(mock_http)):
            await AsyncLLMClient(api_key="my-key", model="test-model", max_tokens=128).ask("hello")

        _, kwargs = mock_http.post.call_args
        assert kwargs["headers"]["x-api-key"] == "my-key"
        assert kwargs["headers"]["anthropic-version"] == "2023-06-01"
        assert kwargs["json"]["model"] == "test-model"
        assert kwargs["json"]["max_tokens"] == 128
        assert kwargs["json"]["messages"] == [{"role": "user", "content": "hello"}]

    asyncio.run(inner())


def test_ask_uses_default_model_and_max_tokens():
    """Verifies AsyncLLMClient defaults to DEFAULT_MODEL and DEFAULT_MAX_TOKENS."""
    client = AsyncLLMClient(api_key="key")
    assert client._model == DEFAULT_MODEL
    assert client._max_tokens == DEFAULT_MAX_TOKENS
