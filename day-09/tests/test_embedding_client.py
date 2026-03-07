import pytest
from unittest.mock import patch, MagicMock
from src.embedding_client import EmbeddingClient


def _make_response(status_code: int, json_data: dict) -> MagicMock:
    """Build a mock httpx response."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.is_success = (200 <= status_code < 300)
    mock_resp.json.return_value = json_data
    mock_resp.text = str(json_data)
    return mock_resp


def test_embed_returns_embeddings_for_all_texts(monkeypatch):
    """Client must return one embedding vector per input text."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    embeddings = [[0.1, 0.2], [0.3, 0.4]]
    mock_resp = _make_response(200, {"data": [{"embedding": e} for e in embeddings]})

    with patch("embedding_client.httpx.post", return_value=mock_resp):
        client = EmbeddingClient()
        result = client.embed(["text one", "text two"], model="voyage-3")

    assert result == embeddings


def test_embed_raises_on_non_2xx_response(monkeypatch):
    """Client must raise RuntimeError when API returns a non-2xx status."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    mock_resp = _make_response(401, {"error": "unauthorized"})

    with patch("embedding_client.httpx.post", return_value=mock_resp):
        client = EmbeddingClient()
        with pytest.raises(RuntimeError, match="401"):
            client.embed(["text"], model="voyage-3")


def test_embed_raises_on_mismatched_embedding_count(monkeypatch):
    """Client must raise RuntimeError when API returns fewer embeddings than inputs."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    mock_resp = _make_response(200, {"data": [{"embedding": [0.1, 0.2]}]})

    with patch("embedding_client.httpx.post", return_value=mock_resp):
        client = EmbeddingClient()
        with pytest.raises(RuntimeError, match="Expected 2 embeddings"):
            client.embed(["text one", "text two"], model="voyage-3")


def test_embed_raises_on_empty_embedding_vector(monkeypatch):
    """Client must raise RuntimeError when any embedding vector is empty."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    mock_resp = _make_response(200, {"data": [{"embedding": []}]})

    with patch("embedding_client.httpx.post", return_value=mock_resp):
        client = EmbeddingClient()
        with pytest.raises(RuntimeError, match="empty or malformed"):
            client.embed(["text"], model="voyage-3")


def test_embed_raises_on_missing_embedding_key(monkeypatch):
    """Client must raise RuntimeError when embedding key is absent in response item."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    mock_resp = _make_response(200, {"data": [{"not_embedding": [0.1]}]})

    with patch("embedding_client.httpx.post", return_value=mock_resp):
        client = EmbeddingClient()
        with pytest.raises(RuntimeError, match="empty or malformed"):
            client.embed(["text"], model="voyage-3")


def test_client_raises_on_missing_api_key(monkeypatch):
    """EmbeddingClient must raise EnvironmentError if VOYAGE_API_KEY is not set."""
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    with pytest.raises(EnvironmentError, match="VOYAGE_API_KEY"):
        EmbeddingClient()


def test_embed_passes_correct_model_to_api(monkeypatch):
    """Client must send the requested model name in the API payload."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    mock_resp = _make_response(200, {"data": [{"embedding": [0.1, 0.2]}]})

    with patch("embedding_client.httpx.post", return_value=mock_resp) as mock_post:
        client = EmbeddingClient()
        client.embed(["text"], model="voyage-large-2")

    _, kwargs = mock_post.call_args
    assert kwargs["json"]["model"] == "voyage-large-2"
