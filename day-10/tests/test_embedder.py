"""Tests for the EmbeddingClient module."""

import httpx
import pytest
from unittest.mock import patch, MagicMock
from src.embedder import EmbeddingClient


def _make_response(embeddings: list[list[float]]) -> MagicMock:
    """Build a mock httpx response for the OpenAI embeddings endpoint."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {"index": i, "embedding": emb}
            for i, emb in enumerate(embeddings)
        ]
    }
    mock_response.raise_for_status.return_value = None
    return mock_response


def test_embed_returns_one_vector_per_text():
    """Verifies that embed() returns one embedding vector per input text."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        with patch("embedder.httpx.post") as mock_post:
            mock_post.return_value = _make_response([[0.1, 0.2], [0.3, 0.4]])
            client = EmbeddingClient()
            result = client.embed(["hello", "world"])
    assert len(result) == 2


def test_embed_returns_vectors_in_input_order():
    """Verifies that embed() returns vectors ordered by input index."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        with patch("embedder.httpx.post") as mock_post:
            mock_post.return_value = _make_response([[0.1, 0.2], [0.3, 0.4]])
            client = EmbeddingClient()
            result = client.embed(["first", "second"])
    assert result[0] == [0.1, 0.2]
    assert result[1] == [0.3, 0.4]


def test_embed_uses_correct_model_and_url():
    """Verifies that embed() calls the OpenAI endpoint with the correct model."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        with patch("embedder.httpx.post") as mock_post:
            mock_post.return_value = _make_response([[0.0]])
            client = EmbeddingClient()
            client.embed(["test"])
            call_args = mock_post.call_args
    assert "openai.com" in call_args[0][0]
    assert call_args[1]["json"]["model"] == "text-embedding-3-small"


def test_embed_raises_on_http_error():
    """Verifies that embed() propagates HTTP errors from the API."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        with patch("embedder.httpx.post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "error", request=MagicMock(), response=MagicMock()
            )
            mock_post.return_value = mock_response
            client = EmbeddingClient()
            with pytest.raises(httpx.HTTPStatusError):
                client.embed(["fail"])


def test_embed_sends_api_key_in_header():
    """Verifies that the Authorization header contains the API key."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "my-secret-key"}):
        with patch("embedder.httpx.post") as mock_post:
            mock_post.return_value = _make_response([[0.0]])
            client = EmbeddingClient()
            client.embed(["text"])
            headers = mock_post.call_args[1]["headers"]
    assert "my-secret-key" in headers["Authorization"]
