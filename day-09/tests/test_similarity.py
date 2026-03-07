"""Tests for cosine similarity computation and ranking logic."""

import pytest
from src.similarity import cosine_similarity, rank_candidates, SimilarityResult


def test_cosine_similarity_identical_vectors_returns_one():
    """Identical vectors must yield similarity of 1.0."""
    vec = [1.0, 2.0, 3.0]
    assert cosine_similarity(vec, vec) == pytest.approx(1.0, abs=1e-6)


def test_cosine_similarity_orthogonal_vectors_returns_zero():
    """Orthogonal vectors must yield similarity of 0.0."""
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0, abs=1e-6)


def test_cosine_similarity_opposite_vectors_returns_minus_one():
    """Opposite vectors must yield similarity of -1.0."""
    assert cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == pytest.approx(-1.0, abs=1e-6)


def test_cosine_similarity_zero_vector_returns_zero():
    """A zero vector must yield similarity of 0.0 to avoid division by zero."""
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0


def test_cosine_similarity_result_in_valid_range():
    """Cosine similarity must be in [-1.0, 1.0] for arbitrary vectors."""
    result = cosine_similarity([0.5, 0.3, 0.8], [0.1, 0.9, 0.4])
    assert -1.0 <= result <= 1.0


def test_rank_candidates_ordered_by_descending_score():
    """Candidates must be ranked from highest to lowest similarity score."""
    query = [1.0, 0.0]
    candidates = {"orthogonal": [0.0, 1.0], "identical": [1.0, 0.0], "diagonal": [0.5, 0.5]}

    results = rank_candidates(query, candidates)

    assert results[0].text == "identical"
    assert results[0].rank == 1
    assert results[-1].text == "orthogonal"


def test_rank_candidates_rank_numbers_are_sequential():
    """Rank numbers must start at 1 and increment by 1."""
    query = [1.0, 0.0]
    candidates = {"a": [1.0, 0.0], "b": [0.0, 1.0], "c": [-1.0, 0.0]}

    results = rank_candidates(query, candidates)

    assert [r.rank for r in results] == [1, 2, 3]


def test_rank_candidates_scores_match_cosine_similarity():
    """Each result score must equal cosine_similarity(query, candidate)."""
    query = [1.0, 0.0]
    candidates = {"a": [1.0, 0.0], "b": [0.5, 0.5]}

    results = rank_candidates(query, candidates)

    for r in results:
        expected = cosine_similarity(query, candidates[r.text])
        assert r.score == pytest.approx(expected, abs=1e-6)


def test_rank_candidates_single_candidate():
    """Ranking with a single candidate must return one result with rank 1."""
    query = [1.0, 0.0]
    results = rank_candidates(query, {"only": [0.5, 0.5]})

    assert len(results) == 1
    assert results[0].rank == 1
    assert results[0].text == "only"


def test_similarity_result_dataclass_fields():
    """SimilarityResult must expose rank, score, and text fields."""
    r = SimilarityResult(rank=1, score=0.95, text="hello")
    assert r.rank == 1
    assert r.score == 0.95
    assert r.text == "hello"
