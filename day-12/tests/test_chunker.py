"""Tests for the text chunker module."""

import pytest
from src.chunker import chunk_text


def test_chunk_text_splits_into_equal_chunks():
    """Verifies that text is split into chunks of the specified size."""
    text = "a" * 900
    chunks = chunk_text(text, chunk_size=300)
    assert len(chunks) == 3
    assert all(len(c) == 300 for c in chunks)


def test_chunk_text_last_chunk_shorter():
    """Verifies that the last chunk can be shorter than chunk_size."""
    text = "a" * 350
    chunks = chunk_text(text, chunk_size=300)
    assert len(chunks) == 2
    assert len(chunks[0]) == 300
    assert len(chunks[1]) == 50


def test_chunk_text_empty_string_returns_empty_list():
    """Verifies that an empty input produces an empty list."""
    assert chunk_text("") == []


def test_chunk_text_whitespace_only_returns_empty_list():
    """Verifies that whitespace-only input produces an empty list."""
    assert chunk_text("   \n\t  ") == []


def test_chunk_text_shorter_than_chunk_size_returns_single_chunk():
    """Verifies that text shorter than chunk_size returns a single chunk."""
    text = "hello world"
    chunks = chunk_text(text, chunk_size=300)
    assert chunks == ["hello world"]


def test_chunk_text_default_chunk_size():
    """Verifies that the default chunk size is 300 characters."""
    text = "x" * 600
    chunks = chunk_text(text)
    assert len(chunks) == 2


def test_chunk_text_exact_chunk_size_boundary():
    """Verifies that text exactly divisible by chunk_size produces equal chunks."""
    text = "b" * 300
    chunks = chunk_text(text, chunk_size=300)
    assert len(chunks) == 1
    assert chunks[0] == "b" * 300
