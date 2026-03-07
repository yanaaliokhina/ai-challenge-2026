from typing import TypedDict


class Chunk(TypedDict):
    """A text chunk with its position index."""

    index: int
    text: str


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[Chunk]:
    """Split text into overlapping word-count-based chunks.

    Args:
        text: The full document text.
        chunk_size: Number of words per chunk.
        overlap: Number of words to overlap between consecutive chunks.

    Returns:
        List of chunks, each with an index and text string.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks: list[Chunk] = []
    index = 0
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append({"index": index, "text": " ".join(chunk_words)})
        index += 1
        if end == len(words):
            break
        start += step

    return chunks
