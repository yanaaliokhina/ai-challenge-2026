"""Tests for the CLI entry point and file loading logic."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.main import load_candidates, print_results, main
from src.similarity import SimilarityResult


def test_load_candidates_returns_lines(tmp_path):
    """load_candidates must return all non-empty lines from the file."""
    f = tmp_path / "candidates.txt"
    f.write_text("apple\nbanana\ncherry\n")
    result = load_candidates(str(f))
    assert result == ["apple", "banana", "cherry"]


def test_load_candidates_skips_blank_lines(tmp_path):
    """load_candidates must skip blank lines in the file."""
    f = tmp_path / "candidates.txt"
    f.write_text("apple\n\nbanana\n")
    result = load_candidates(str(f))
    assert result == ["apple", "banana"]


def test_load_candidates_raises_file_not_found():
    """load_candidates must raise FileNotFoundError for a missing file."""
    with pytest.raises(FileNotFoundError, match="not found"):
        load_candidates("/nonexistent/path/file.txt")


def test_load_candidates_raises_for_fewer_than_two_lines(tmp_path):
    """load_candidates must raise ValueError when file has fewer than 2 lines."""
    f = tmp_path / "candidates.txt"
    f.write_text("only one line\n")
    with pytest.raises(ValueError, match="at least 2"):
        load_candidates(str(f))


def test_load_candidates_raises_for_empty_file(tmp_path):
    """load_candidates must raise ValueError for an empty file."""
    f = tmp_path / "candidates.txt"
    f.write_text("")
    with pytest.raises(ValueError, match="at least 2"):
        load_candidates(str(f))


def test_print_results_outputs_all_ranks(capsys):
    """print_results must output a row for each SimilarityResult."""
    results = [
        SimilarityResult(rank=1, score=0.9512, text="first candidate"),
        SimilarityResult(rank=2, score=0.7231, text="second candidate"),
    ]
    print_results(results)
    captured = capsys.readouterr()
    assert "1" in captured.out
    assert "0.9512" in captured.out
    assert "first candidate" in captured.out
    assert "second candidate" in captured.out


def test_print_results_truncates_long_text(capsys):
    """print_results must truncate text longer than 80 characters in the display."""
    long_text = "x" * 100
    results = [SimilarityResult(rank=1, score=0.5, text=long_text)]
    print_results(results)
    captured = capsys.readouterr()
    assert "x" * 80 in captured.out
    assert "x" * 100 not in captured.out


def test_main_exits_with_error_on_missing_file(tmp_path, monkeypatch):
    """main() must exit with code 1 when --file points to a nonexistent file."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--query", "test query", "--file", "/nonexistent/file.txt"],
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_main_exits_with_error_on_missing_api_key(tmp_path, monkeypatch):
    """main() must exit with code 1 when VOYAGE_API_KEY is not set."""
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    f = tmp_path / "candidates.txt"
    f.write_text("line one\nline two\n")
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--query", "test query", "--file", str(f)],
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_main_prints_ranked_table(tmp_path, monkeypatch, capsys):
    """main() must print a ranked table when all inputs are valid."""
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    f = tmp_path / "candidates.txt"
    f.write_text("deep learning is amazing\nthe sky is blue\n")
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--query", "machine learning", "--file", str(f)],
    )

    mock_resp = MagicMock()
    mock_resp.is_success = True
    mock_resp.json.return_value = {
        "data": [
            {"embedding": [1.0, 0.0]},
            {"embedding": [0.9, 0.1]},
            {"embedding": [0.0, 1.0]},
        ]
    }

    with patch("embedding_client.httpx.post", return_value=mock_resp):
        main()

    captured = capsys.readouterr()
    assert "Rank" in captured.out
    assert "Score" in captured.out
    assert "1" in captured.out
