"""Tests for main module entry point behaviour."""

import json
import pytest
from unittest.mock import patch, MagicMock
from src.main import run


def test_main_empty_query_exits_with_code_1(tmp_path, monkeypatch, capsys):
    """Verifies that an empty --query string causes sys.exit(1)."""
    index_file = tmp_path / "index.json"
    index_file.write_text(json.dumps([{"id": "a", "text": "hello", "embedding": [0.1, 0.2]}]))
    monkeypatch.setattr("sys.argv", ["main.py", "--index", str(index_file), "--query", "   "])
    with pytest.raises(SystemExit) as exc:
        run()
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_main_api_failure_exits_with_code_1(tmp_path, monkeypatch, capsys):
    """Verifies that an embedding API failure causes sys.exit(1)."""
    index_file = tmp_path / "index.json"
    index_file.write_text(json.dumps([{"id": "a", "text": "hello", "embedding": [0.1, 0.2]}]))
    monkeypatch.setattr("sys.argv", ["main.py", "--index", str(index_file), "--query", "test query"])
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    with patch("embedding_client.httpx.post") as mock_post:
        mock_post.side_effect = Exception("connection refused")
        with pytest.raises(SystemExit) as exc:
            run()
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_main_successful_search_prints_results(tmp_path, monkeypatch, capsys):
    """Verifies that a successful search prints ranked results to stdout."""
    entries = [
        {"id": "doc1", "text": "Python is a programming language", "embedding": [1.0, 0.0]},
        {"id": "doc2", "text": "Machine learning with Python", "embedding": [0.0, 1.0]},
    ]
    index_file = tmp_path / "index.json"
    index_file.write_text(json.dumps(entries))
    monkeypatch.setattr("sys.argv", ["main.py", "--index", str(index_file), "--query", "Python programming", "--top", "2"])
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"embedding": [1.0, 0.0]}]}
    mock_response.raise_for_status = MagicMock()

    with patch("embedding_client.httpx.post", return_value=mock_response):
        run()

    captured = capsys.readouterr()
    assert "Results:" in captured.out
    assert "doc1" in captured.out
    assert "1." in captured.out


def test_main_missing_index_file_exits_with_code_1(tmp_path, monkeypatch, capsys):
    """Verifies that a missing index file causes sys.exit(1)."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", str(tmp_path / "missing.json"), "--query", "hello"])
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    with pytest.raises(SystemExit) as exc:
        run()
    assert exc.value.code == 1
