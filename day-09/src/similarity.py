from dataclasses import dataclass
import numpy as np


@dataclass
class SimilarityResult:
    """Holds a candidate text and its cosine similarity score to the query."""

    rank: int
    score: float
    text: str


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two vectors using numpy.

    Returns a float in [-1.0, 1.0].
    """
    a = np.array(vec_a, dtype=np.float64)
    b = np.array(vec_b, dtype=np.float64)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def rank_candidates(
    query_embedding: list[float],
    candidates: dict[str, list[float]],
) -> list[SimilarityResult]:
    scored = sorted(
        ((cosine_similarity(query_embedding, emb), text) for text, emb in candidates.items()),
        key=lambda x: x[0],
        reverse=True,
    )
    return [
        SimilarityResult(rank=i + 1, score=score, text=text)
        for i, (score, text) in enumerate(scored)
    ]
