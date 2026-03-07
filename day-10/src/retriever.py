"""Retriever for day-10 Mini RAG Script."""

from typing import TypedDict
import numpy as np


class ChunkWithEmbedding(TypedDict):
    """A chunk paired with its embedding vector."""

    index: int
    text: str
    embedding: list[float]


class RankedChunk(TypedDict):
    """A chunk enriched with its similarity score."""

    index: int
    text: str
    score: float


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    norm_a = np.linalg.norm(va)
    norm_b = np.linalg.norm(vb)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(va, vb) / (norm_a * norm_b))


def retrieve_top_k(
    query_embedding: list[float],
    chunk_map: list[ChunkWithEmbedding],
    k: int,
) -> list[RankedChunk]:
    """Return the top-k chunks most similar to the query.

    Args:
        query_embedding: Embedding vector for the user query.
        chunk_map: List of chunks each paired with their embedding vector.
        k: Number of top results to return.

    Returns:
        List of RankedChunk sorted by descending similarity score.
    """
    scored: list[RankedChunk] = []
    for item in chunk_map:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append({"index": item["index"], "text": item["text"], "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]
