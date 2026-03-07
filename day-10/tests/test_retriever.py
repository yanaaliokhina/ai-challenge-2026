"""Tests for the retriever module."""

import pytest
from src.retriever import cosine_similarity, retrieve_top_k, ChunkWithEmbedding


def test_cosine_similarity_identical_vectors_returns_one():
    """Verifies that identical vectors have similarity of 1.0."""
    v = [1.0, 2.0, 3.0]
    assert cosine_similarity(v, v) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors_returns_zero():
    """Verifies that orthogonal vectors have similarity of 0.0."""
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_similarity_opposite_vectors_returns_minus_one():
    """Verifies that opposite vectors have similarity of -1.0."""
    assert cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == pytest.approx(-1.0)


def test_cosine_similarity_zero_vector_returns_zero():
    """Verifies that a zero vector produces similarity of 0.0."""
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == pytest.approx(0.0)


def test_retrieve_top_k_returns_k_results():
    """Verifies that retrieve_top_k returns exactly k chunks."""
    query_emb = [1.0, 0.0]
    chunk_map: list[ChunkWithEmbedding] = [
        {"index": i, "text": f"chunk {i}", "embedding": [float(i), 0.0]}
        for i in range(5)
    ]
    result = retrieve_top_k(query_emb, chunk_map, k=3)
    assert len(result) == 3


def test_retrieve_top_k_sorted_by_descending_score():
    """Verifies that results are sorted from highest to lowest similarity."""
    query_emb = [1.0, 0.0]
    chunk_map: list[ChunkWithEmbedding] = [
        {"index": 0, "text": "chunk 0", "embedding": [0.1, 0.0]},
        {"index": 1, "text": "chunk 1", "embedding": [0.9, 0.0]},
        {"index": 2, "text": "chunk 2", "embedding": [0.5, 0.0]},
        {"index": 3, "text": "chunk 3", "embedding": [0.3, 0.0]},
    ]
    result = retrieve_top_k(query_emb, chunk_map, k=4)
    scores = [r["score"] for r in result]
    assert scores == sorted(scores, reverse=True)


def test_retrieve_top_k_selects_most_similar_chunk():
    """Verifies that the highest-scored chunk is the one most aligned with the query."""
    query_emb = [1.0, 0.0]
    chunk_map: list[ChunkWithEmbedding] = [
        {"index": 0, "text": "low similarity", "embedding": [0.1, 0.9]},
        {"index": 1, "text": "high similarity", "embedding": [0.9, 0.1]},
    ]
    result = retrieve_top_k(query_emb, chunk_map, k=1)
    assert result[0]["index"] == 1


def test_retrieve_top_k_includes_score_in_result():
    """Verifies that each result contains a 'score' field."""
    query_emb = [1.0, 0.0]
    chunk_map: list[ChunkWithEmbedding] = [
        {"index": 0, "text": "a", "embedding": [1.0, 0.0]},
    ]
    result = retrieve_top_k(query_emb, chunk_map, k=1)
    assert "score" in result[0]


def test_retrieve_top_k_clamps_to_available_chunks():
    """Verifies that k larger than number of chunks returns all chunks."""
    query_emb = [1.0, 0.0]
    chunk_map: list[ChunkWithEmbedding] = [
        {"index": 0, "text": "only", "embedding": [1.0, 0.0]},
    ]
    result = retrieve_top_k(query_emb, chunk_map, k=10)
    assert len(result) == 1
