"""JSON index storage and similarity search for day-12 project."""

import json
import math
import uuid
from pathlib import Path


def load_index(index_path: str) -> list[dict]:
    """Load the embedding index from a JSON file, or return an empty list."""
    path = Path(index_path)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index: list[dict], index_path: str) -> None:
    """Persist the embedding index to a JSON file."""
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def get_indexed_texts(index: list[dict]) -> set[str]:
    """Return the set of text values already present in the index."""
    return {entry["text"] for entry in index}


def add_entry(index: list[dict], text: str, embedding: list[float]) -> dict:
    """Create a new index entry and append it to the index list."""
    entry = {
        "id": str(uuid.uuid4()),
        "text": text,
        "embedding": embedding,
    }
    index.append(entry)
    return entry


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def query_index(index: list[dict], query_embedding: list[float], top_n: int) -> list[dict]:
    """Return the top-N entries by cosine similarity to the query embedding."""
    scored = [
        {"score": cosine_similarity(query_embedding, entry["embedding"]), "text": entry["text"]}
        for entry in index
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]
