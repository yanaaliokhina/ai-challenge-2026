"""Tests for main module helper functions."""

import json

import pytest

from src.embedding_client import EmbeddingResult
from src.main import load_texts_from_file, print_summary, save_results


def test_load_texts_from_file_returns_lines(tmp_path):
    """load_texts_from_file returns a list of non-empty stripped lines."""
    f = tmp_path / "inputs.txt"
    f.write_text("hello\nworld\n")
    result = load_texts_from_file(str(f))
    assert result == ["hello", "world"]


def test_load_texts_from_file_skips_blank_lines(tmp_path):
    """load_texts_from_file ignores blank and whitespace-only lines."""
    f = tmp_path / "inputs.txt"
    f.write_text("line1\n\n   \nline2\n")
    result = load_texts_from_file(str(f))
    assert result == ["line1", "line2"]


def test_load_texts_from_file_not_found_raises():
    """load_texts_from_file raises FileNotFoundError for a missing file."""
    with pytest.raises(FileNotFoundError, match="not found"):
        load_texts_from_file("/nonexistent/path/file.txt")


def test_load_texts_from_file_empty_raises(tmp_path):
    """load_texts_from_file raises ValueError when file has no non-blank lines."""
    f = tmp_path / "empty.txt"
    f.write_text("\n\n")
    with pytest.raises(ValueError, match="empty"):
        load_texts_from_file(str(f))


def test_print_summary_single_result(capsys):
    """print_summary prints correct metadata for a single result."""
    results = [EmbeddingResult(text="hi", model="voyage-3-lite", embedding=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6])]
    print_summary(results)
    out = capsys.readouterr().out
    assert "Inputs processed : 1" in out
    assert "Model            : voyage-3-lite" in out
    assert "Embedding dim    : 6" in out
    assert "[0] preview" in out


def test_print_summary_shows_preview_only_five_values(capsys):
    """print_summary truncates embedding preview to EMBEDDING_PREVIEW_COUNT values."""
    embedding = [float(i) for i in range(20)]
    results = [EmbeddingResult(text="t", model="m", embedding=embedding)]
    print_summary(results)
    out = capsys.readouterr().out
    assert "..." in out


def test_print_summary_multiple_results(capsys):
    """print_summary prints one preview line per result."""
    results = [
        EmbeddingResult(text="a", model="m", embedding=[0.1, 0.2, 0.3, 0.4, 0.5]),
        EmbeddingResult(text="b", model="m", embedding=[0.6, 0.7, 0.8, 0.9, 1.0]),
    ]
    print_summary(results)
    out = capsys.readouterr().out
    assert "Inputs processed : 2" in out
    assert "[0] preview" in out
    assert "[1] preview" in out


def test_print_summary_empty_list_prints_nothing(capsys):
    """print_summary produces no output when results list is empty."""
    print_summary([])
    out = capsys.readouterr().out
    assert out == ""


def test_save_results_creates_json_file(tmp_path):
    """save_results writes a JSON file at the given path."""
    results = [EmbeddingResult(text="hello", model="voyage-3-lite", embedding=[0.1, 0.2])]
    out_path = tmp_path / "out.json"
    save_results(results, str(out_path))
    assert out_path.exists()


def test_save_results_json_structure(tmp_path):
    """save_results produces a list of objects with text, model, and embedding keys."""
    results = [
        EmbeddingResult(text="hello", model="voyage-3-lite", embedding=[0.1, 0.2, 0.3]),
        EmbeddingResult(text="world", model="voyage-3-lite", embedding=[0.4, 0.5, 0.6]),
    ]
    out_path = tmp_path / "out.json"
    save_results(results, str(out_path))
    data = json.loads(out_path.read_text())
    assert isinstance(data, list)
    assert len(data) == 2
    for item in data:
        assert "text" in item
        assert "model" in item
        assert "embedding" in item


def test_save_results_preserves_embedding_values(tmp_path):
    """save_results stores the exact embedding values in the JSON output."""
    embedding = [0.123, -0.456, 0.789]
    results = [EmbeddingResult(text="t", model="m", embedding=embedding)]
    out_path = tmp_path / "out.json"
    save_results(results, str(out_path))
    data = json.loads(out_path.read_text())
    assert data[0]["embedding"] == embedding
