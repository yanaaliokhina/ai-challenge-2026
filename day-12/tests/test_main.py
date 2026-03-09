"""Integration tests for main.py workflow."""

import json
import pytest
from unittest.mock import patch
from src.main import run


def make_args(file=None, query=None, top_n=3, index=None, chunk_size=300):
    class Args:
        pass
    args = Args()
    args.file = file
    args.query = query
    args.top_n = top_n
    args.index = index
    args.chunk_size = chunk_size
    return args


FAKE_EMBEDDING = [1.0, 0.0, 0.0]


@pytest.fixture
def mock_client():
    with patch("src.main.EmbeddingClient") as MockClass:
        instance = MockClass.return_value
        instance.embed.return_value = FAKE_EMBEDDING
        yield instance


def test_run_file_creates_index(tmp_path, mock_client):
    """Verifies that --file mode writes a populated index.json."""
    text_file = tmp_path / "sample.txt"
    text_file.write_text("Hello world. " * 30)
    index_path = str(tmp_path / "index.json")

    run(make_args(file=str(text_file), index=index_path))

    with open(index_path) as f:
        index = json.load(f)
    assert len(index) > 0
    assert "text" in index[0]
    assert "embedding" in index[0]
    assert "id" in index[0]


def test_run_file_deduplication(tmp_path, mock_client):
    """Verifies that re-running --file does not create duplicate entries."""
    text_file = tmp_path / "sample.txt"
    text_file.write_text("A" * 300)
    index_path = str(tmp_path / "index.json")

    run(make_args(file=str(text_file), index=index_path))
    run(make_args(file=str(text_file), index=index_path))

    with open(index_path) as f:
        index = json.load(f)
    assert len(index) == 1


def test_run_file_skips_embedding_for_existing_chunk(tmp_path, mock_client):
    """Verifies that embed() is not called for already-indexed chunks."""
    text_file = tmp_path / "sample.txt"
    text_file.write_text("B" * 300)
    index_path = str(tmp_path / "index.json")

    run(make_args(file=str(text_file), index=index_path))
    call_count_first = mock_client.embed.call_count

    run(make_args(file=str(text_file), index=index_path))
    call_count_second = mock_client.embed.call_count

    assert call_count_second == call_count_first


def test_run_query_prints_results(tmp_path, mock_client, capsys):
    """Verifies that --query mode prints top-N results to stdout."""
    index = [{"id": "1", "text": "relevant chunk", "embedding": [1.0, 0.0, 0.0]}]
    index_path = str(tmp_path / "index.json")
    with open(index_path, "w") as f:
        json.dump(index, f)

    run(make_args(query="test query", top_n=1, index=index_path))

    out = capsys.readouterr().out
    assert "relevant chunk" in out
    assert "Score:" in out


def test_run_file_then_query(tmp_path, mock_client, capsys):
    """Verifies that running --file and --query together indexes first then queries."""
    text_file = tmp_path / "doc.txt"
    text_file.write_text("C" * 300)
    index_path = str(tmp_path / "index.json")

    run(make_args(file=str(text_file), query="anything", top_n=1, index=index_path))

    out = capsys.readouterr().out
    assert "Indexed" in out
    assert "Score:" in out


def test_run_query_empty_index_exits(tmp_path, capsys):
    """Verifies that --query on an empty index exits with an error message."""
    index_path = str(tmp_path / "index.json")
    with patch("src.main.EmbeddingClient"):
        with pytest.raises(SystemExit):
            run(make_args(query="something", index=index_path))
