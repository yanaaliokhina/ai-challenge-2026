"""Tests for the embedding_client module."""

import pytest
from unittest.mock import patch, MagicMock
from src.embedding_client import EmbeddingClient


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    return EmbeddingClient()


def test_embed_returns_list_of_floats(client):
    """Verifies that embed() returns a list of floats from a successful API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"embedding": [0.1, 0.2, 0.3]}]}
    mock_response.raise_for_status = MagicMock()

    with patch("src.embedding_client.httpx.post", return_value=mock_response) as mock_post:
        result = client.embed("hello")

    assert result == [0.1, 0.2, 0.3]


def test_embed_sends_correct_payload(client):
    """Verifies that embed() sends the text in the API request payload."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"embedding": [0.5]}]}
    mock_response.raise_for_status = MagicMock()

    with patch("src.embedding_client.httpx.post", return_value=mock_response) as mock_post:
        client.embed("test input")
        call_kwargs = mock_post.call_args

    assert call_kwargs.kwargs["json"]["input"] == ["test input"]


def test_embed_uses_correct_api_key(client):
    """Verifies that embed() sends the Authorization header with the API key."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"embedding": [0.0]}]}
    mock_response.raise_for_status = MagicMock()

    with patch("src.embedding_client.httpx.post", return_value=mock_response) as mock_post:
        client.embed("x")
        headers = mock_post.call_args.kwargs["headers"]

    assert headers["Authorization"] == "Bearer test-key"


def test_embed_raises_on_http_error(client):
    """Verifies that embed() propagates HTTP errors from raise_for_status."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP 401")

    with patch("src.embedding_client.httpx.post", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP 401"):
            client.embed("bad call")


def test_client_reads_api_key_from_env(monkeypatch):
    """Verifies that EmbeddingClient reads VOYAGE_API_KEY from environment."""
    monkeypatch.setenv("VOYAGE_API_KEY", "my-voyage-key")
    c = EmbeddingClient()
    assert c._api_key == "my-voyage-key"


def test_client_raises_if_api_key_missing(monkeypatch):
    """Verifies that EmbeddingClient raises KeyError when VOYAGE_API_KEY is unset."""
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    with pytest.raises(KeyError):
        EmbeddingClient()
