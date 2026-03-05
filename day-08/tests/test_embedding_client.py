"""Tests for EmbeddingClient."""

from unittest.mock import MagicMock, patch

import pytest

from src.embedding_client import EmbeddingClient, EmbeddingResult

FAKE_API_RESPONSE = {
    "data": [
        {"index": 0, "embedding": [0.1, 0.2, 0.3, 0.4, 0.5]},
        {"index": 1, "embedding": [0.6, 0.7, 0.8, 0.9, 1.0]},
    ]
}


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")


def _mock_response(data: dict) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = data
    mock.raise_for_status = MagicMock()
    return mock


def test_embed_single_text_returns_one_result():
    """Embedding a single text produces exactly one EmbeddingResult."""
    single_response = {"data": [{"index": 0, "embedding": [0.1, 0.2, 0.3]}]}
    with patch("embedding_client.httpx.post", return_value=_mock_response(single_response)):
        client = EmbeddingClient()
        results = client.embed(["hello"], "voyage-3-lite")
    assert len(results) == 1
    assert isinstance(results[0], EmbeddingResult)
    assert results[0].text == "hello"
    assert results[0].model == "voyage-3-lite"
    assert results[0].embedding == [0.1, 0.2, 0.3]


def test_embed_batch_texts_returns_all_results():
    """Embedding two texts returns two EmbeddingResults in index order."""
    with patch("embedding_client.httpx.post", return_value=_mock_response(FAKE_API_RESPONSE)):
        client = EmbeddingClient()
        results = client.embed(["first", "second"], "voyage-3-lite")
    assert len(results) == 2
    assert results[0].text == "first"
    assert results[1].text == "second"


def test_embed_result_contains_correct_embedding_values():
    """EmbeddingResult stores the exact float values returned by the API."""
    single_response = {"data": [{"index": 0, "embedding": [0.11, -0.22, 0.33]}]}
    with patch("embedding_client.httpx.post", return_value=_mock_response(single_response)):
        client = EmbeddingClient()
        results = client.embed(["test"], "voyage-3-lite")
    assert results[0].embedding == [0.11, -0.22, 0.33]


def test_embed_missing_api_key_raises_environment_error(monkeypatch):
    """Missing VOYAGE_API_KEY raises EnvironmentError before making any HTTP call."""
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    with pytest.raises(EnvironmentError, match="VOYAGE_API_KEY"):
        EmbeddingClient()


def test_embed_api_http_error_propagates(monkeypatch):
    """An HTTP error from the API propagates as an exception."""
    import httpx

    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "401", request=MagicMock(), response=MagicMock()
    )
    with patch("embedding_client.httpx.post", return_value=mock_resp):
        client = EmbeddingClient()
        with pytest.raises(Exception):
            client.embed(["hello"], "voyage-3-lite")


def test_embed_passes_correct_model_in_payload():
    """The model name from the caller is forwarded verbatim in the API payload."""
    single_response = {"data": [{"index": 0, "embedding": [0.5]}]}
    with patch("embedding_client.httpx.post", return_value=_mock_response(single_response)) as mock_post:
        client = EmbeddingClient()
        client.embed(["text"], "voyage-3")
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["model"] == "voyage-3"
