"""Tests for searcher module."""

import pytest
from src.searcher import cosine_similarity, search, SearchResult
from src.index_loader import IndexEntry


def make_entry(id: str, text: str, embedding: list[float]) -> IndexEntry:
    return IndexEntry(id=id, text=text, embedding=embedding)


def test_cosine_similarity_identical_vectors_returns_one():
    """Verifies that two identical vectors produce a cosine similarity of 1.0."""
    v = [1.0, 0.0, 0.0]
    assert cosine_similarity(v, v) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors_returns_zero():
    """Verifies that two orthogonal vectors produce a cosine similarity of 0.0."""
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert cosine_similarity(a, b) == pytest.approx(0.0)


def test_cosine_similarity_opposite_vectors_returns_minus_one():
    """Verifies that two opposite vectors produce a cosine similarity of -1.0."""
    a = [1.0, 0.0]
    b = [-1.0, 0.0]
    assert cosine_similarity(a, b) == pytest.approx(-1.0)


def test_cosine_similarity_zero_vector_returns_zero():
    """Verifies that a zero vector produces a similarity of 0.0 to avoid division by zero."""
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0


def test_search_returns_top_n_results():
    """Verifies that search returns exactly top_n results."""
    query = [1.0, 0.0]
    entries = [
        make_entry("a", "text a", [1.0, 0.0]),
        make_entry("b", "text b", [0.0, 1.0]),
        make_entry("c", "text c", [0.5, 0.5]),
        make_entry("d", "text d", [0.9, 0.1]),
    ]
    results = search(query, entries, top_n=2)
    assert len(results) == 2


def test_search_results_sorted_descending_by_score():
    """Verifies that search results are ordered from highest to lowest similarity."""
    query = [1.0, 0.0]
    entries = [
        make_entry("low", "low", [0.0, 1.0]),
        make_entry("high", "high", [1.0, 0.0]),
        make_entry("mid", "mid", [0.7, 0.3]),
    ]
    results = search(query, entries, top_n=3)
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_search_rank_starts_at_one():
    """Verifies that the first result has rank 1."""
    query = [1.0, 0.0]
    entries = [make_entry("x", "text", [1.0, 0.0])]
    results = search(query, entries, top_n=1)
    assert results[0].rank == 1


def test_search_ranks_are_sequential():
    """Verifies that ranks increment sequentially starting from 1."""
    query = [1.0, 0.0]
    entries = [
        make_entry("a", "a", [1.0, 0.0]),
        make_entry("b", "b", [0.5, 0.5]),
        make_entry("c", "c", [0.0, 1.0]),
    ]
    results = search(query, entries, top_n=3)
    assert [r.rank for r in results] == [1, 2, 3]


def test_search_score_rounded_to_four_decimal_places():
    """Verifies that scores are rounded to 4 decimal places."""
    query = [1.0, 1.0]
    entries = [make_entry("a", "text", [1.0, 1.0])]
    results = search(query, entries, top_n=1)
    score_str = str(results[0].score)
    decimal_part = score_str.split(".")[-1] if "." in score_str else ""
    assert len(decimal_part) <= 4


def test_search_text_truncated_at_200_chars():
    """Verifies that text longer than 200 characters is truncated with ellipsis."""
    query = [1.0, 0.0]
    long_text = "x" * 250
    entries = [make_entry("a", long_text, [1.0, 0.0])]
    results = search(query, entries, top_n=1)
    assert len(results[0].text) == 203
    assert results[0].text.endswith("...")


def test_search_short_text_not_truncated():
    """Verifies that text at or below 200 characters is not modified."""
    query = [1.0, 0.0]
    short_text = "hello world"
    entries = [make_entry("a", short_text, [1.0, 0.0])]
    results = search(query, entries, top_n=1)
    assert results[0].text == short_text


def test_search_top_n_larger_than_entries_returns_all():
    """Verifies that requesting more results than entries returns all entries."""
    query = [1.0, 0.0]
    entries = [make_entry("a", "a", [1.0, 0.0]), make_entry("b", "b", [0.0, 1.0])]
    results = search(query, entries, top_n=10)
    assert len(results) == 2


def test_search_empty_entries_returns_empty_list():
    """Verifies that searching an empty entry list returns an empty result list."""
    results = search([1.0, 0.0], [], top_n=3)
    assert results == []
