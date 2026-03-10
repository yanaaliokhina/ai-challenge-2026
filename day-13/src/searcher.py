import numpy as np
from dataclasses import dataclass
from index_loader import IndexEntry
from constants import TEXT_TRUNCATE_LENGTH


@dataclass
class SearchResult:
    rank: int
    id: str
    score: float
    text: str


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    norm_a = np.linalg.norm(va)
    norm_b = np.linalg.norm(vb)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(va, vb) / (norm_a * norm_b))


def search(query_vector: list[float], entries: list[IndexEntry], top_n: int) -> list[SearchResult]:
    scored = [
        (cosine_similarity(query_vector, entry.embedding), entry)
        for entry in entries
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for rank, (score, entry) in enumerate(scored[:top_n], start=1):
        text = entry.text
        if len(text) > TEXT_TRUNCATE_LENGTH:
            text = text[:TEXT_TRUNCATE_LENGTH] + "..."
        results.append(SearchResult(rank=rank, id=entry.id, score=round(score, 4), text=text))
    return results
