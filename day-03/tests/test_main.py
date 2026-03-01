import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.main import main


def make_mock_async_client(response_text: str) -> AsyncMock:
    """Return a mock async context manager httpx.AsyncClient returning given LLM text."""
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {"content": [{"type": "text", "text": response_text}]}

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post.return_value = response
    return mock_client


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    """Inject a dummy API key for all CLI tests."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")


def test_cli_routes_sentiment_task_and_prints_json(capsys):
    """Verifies that --task sentiment calls the API and prints valid indented JSON."""
    json_text = '{"sentiment": "positive", "confidence": 0.95, "reasoning": "Happy."}'
    mock_client = make_mock_async_client(json_text)

    with patch("sys.argv", ["main", "--task", "sentiment", "--input", "I love this!"]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            main()

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["sentiment"] == "positive"
    assert result["confidence"] == 0.95


def test_cli_routes_facts_task_and_prints_json(capsys):
    """Verifies that --task facts calls the API and prints valid indented JSON."""
    json_text = '{"facts": ["Fact one.", "Fact two."], "source_topic": "Science"}'
    mock_client = make_mock_async_client(json_text)

    with patch("sys.argv", ["main", "--task", "facts", "--input", "Some science text."]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            main()

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert "facts" in result
    assert result["source_topic"] == "Science"


def test_cli_output_is_indented_json(capsys):
    """Verifies that the CLI output is formatted with indentation (not a single-line JSON)."""
    json_text = '{"sentiment": "neutral", "confidence": 0.5, "reasoning": "Flat."}'
    mock_client = make_mock_async_client(json_text)

    with patch("sys.argv", ["main", "--task", "sentiment", "--input", "test"]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            main()

    captured = capsys.readouterr()
    assert "\n" in captured.out
    assert "  " in captured.out


def test_cli_exits_with_code_1_on_json_decode_error(capsys):
    """Verifies that the CLI exits with code 1 when the LLM returns non-JSON text."""
    mock_client = make_mock_async_client("not valid json at all")

    with patch("sys.argv", ["main", "--task", "sentiment", "--input", "test"]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            with pytest.raises(SystemExit) as exc_info:
                main()

    assert exc_info.value.code == 1


def test_cli_exits_with_code_1_on_validation_error(capsys):
    """Verifies that the CLI exits with code 1 when JSON does not match the expected schema."""
    mock_client = make_mock_async_client('{"wrong": "field"}')

    with patch("sys.argv", ["main", "--task", "sentiment", "--input", "test"]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            with pytest.raises(SystemExit) as exc_info:
                main()

    assert exc_info.value.code == 1


def test_cli_prints_error_to_stderr_on_json_decode_error(capsys):
    """Verifies that the CLI prints a non-empty error message to stderr on JSON decode failure."""
    mock_client = make_mock_async_client("totally not json")

    with patch("sys.argv", ["main", "--task", "sentiment", "--input", "test"]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            with pytest.raises(SystemExit):
                main()

    captured = capsys.readouterr()
    assert len(captured.err) > 0


def test_cli_prints_error_to_stderr_on_validation_error(capsys):
    """Verifies that the CLI prints a non-empty error message to stderr on schema mismatch."""
    mock_client = make_mock_async_client('{"bad_key": 123}')

    with patch("sys.argv", ["main", "--task", "facts", "--input", "test"]):
        with patch("httpx.AsyncClient", return_value=mock_client):
            with pytest.raises(SystemExit):
                main()

    captured = capsys.readouterr()
    assert len(captured.err) > 0
