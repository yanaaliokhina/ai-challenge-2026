"""Tests for the text chunker module."""

import pytest
from src.chunker import chunk_text


def test_chunk_text_basic_splits_correctly():
    """Verifies that a simple text is split into correct number of chunks."""
    text = " ".join(str(i) for i in range(10))
    chunks = chunk_text(text, chunk_size=5, overlap=0)
    assert len(chunks) == 2
    assert chunks[0]["text"] == "0 1 2 3 4"
    assert chunks[1]["text"] == "5 6 7 8 9"


def test_chunk_text_overlap_repeats_words():
    """Verifies that overlapping words appear in consecutive chunks."""
    text = " ".join(str(i) for i in range(10))
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert chunks[0]["text"] == "0 1 2 3 4"
    assert chunks[1]["text"].startswith("3 4")


def test_chunk_text_assigns_sequential_indices():
    """Verifies that each chunk receives a sequential index starting at 0."""
    text = " ".join(["word"] * 20)
    chunks = chunk_text(text, chunk_size=5, overlap=0)
    for i, chunk in enumerate(chunks):
        assert chunk["index"] == i


def test_chunk_text_covers_full_document():
    """Verifies all words from the document appear in at least one chunk."""
    words = [str(i) for i in range(25)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=10, overlap=3)
    covered = set()
    for chunk in chunks:
        covered.update(chunk["text"].split())
    assert covered == set(words)


def test_chunk_text_empty_text_returns_empty_list():
    """Verifies that empty input returns an empty list."""
    assert chunk_text("", chunk_size=10, overlap=2) == []


def test_chunk_text_whitespace_only_returns_empty_list():
    """Verifies that whitespace-only input returns an empty list."""
    assert chunk_text("   \n\t  ", chunk_size=10, overlap=2) == []


def test_chunk_text_text_shorter_than_chunk_size_returns_one_chunk():
    """Verifies that text shorter than chunk_size produces exactly one chunk."""
    text = "hello world"
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) == 1
    assert chunks[0]["text"] == "hello world"
    assert chunks[0]["index"] == 0


def test_chunk_text_no_overlap_non_overlapping():
    """Verifies that with overlap=0 chunks do not share words."""
    text = " ".join(str(i) for i in range(6))
    chunks = chunk_text(text, chunk_size=3, overlap=0)
    assert chunks[0]["text"] == "0 1 2"
    assert chunks[1]["text"] == "3 4 5"


def test_chunk_text_invalid_chunk_size_raises():
    """Verifies that chunk_size <= 0 raises ValueError."""
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("some text", chunk_size=0, overlap=0)


def test_chunk_text_negative_overlap_raises():
    """Verifies that negative overlap raises ValueError."""
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("some text", chunk_size=5, overlap=-1)


def test_chunk_text_overlap_gte_chunk_size_raises():
    """Verifies that overlap >= chunk_size raises ValueError."""
    with pytest.raises(ValueError, match="overlap"):
        chunk_text("some text", chunk_size=5, overlap=5)
