"""Tests for prompt construction in main.py."""

from src.main import build_prompt
from src.retriever import RankedChunk


def test_build_prompt_contains_query():
    """Verifies that the constructed prompt includes the user query."""
    chunks: list[RankedChunk] = [{"index": 0, "text": "Some context.", "score": 0.9}]
    prompt = build_prompt("What is this about?", chunks)
    assert "What is this about?" in prompt


def test_build_prompt_contains_chunk_text():
    """Verifies that the prompt includes the text of each retrieved chunk."""
    chunks: list[RankedChunk] = [{"index": 0, "text": "The sky is blue.", "score": 0.85}]
    prompt = build_prompt("What color is the sky?", chunks)
    assert "The sky is blue." in prompt


def test_build_prompt_contains_all_chunks():
    """Verifies that all top-k chunks appear in the prompt."""
    chunks: list[RankedChunk] = [
        {"index": 0, "text": "First chunk text.", "score": 0.9},
        {"index": 1, "text": "Second chunk text.", "score": 0.8},
        {"index": 2, "text": "Third chunk text.", "score": 0.7},
    ]
    prompt = build_prompt("Tell me everything.", chunks)
    for c in chunks:
        assert c["text"] in prompt


def test_build_prompt_includes_context_instruction():
    """Verifies that the prompt instructs the LLM to use only provided context."""
    chunks: list[RankedChunk] = [{"index": 0, "text": "Context here.", "score": 0.8}]
    prompt = build_prompt("Query?", chunks)
    assert "context" in prompt.lower()


def test_build_prompt_single_chunk_no_error():
    """Verifies that build_prompt works correctly with a single chunk."""
    chunks: list[RankedChunk] = [{"index": 0, "text": "Only chunk.", "score": 1.0}]
    prompt = build_prompt("Question?", chunks)
    assert "Only chunk." in prompt
    assert "Question?" in prompt


def test_build_prompt_chunk_indices_appear_in_context():
    """Verifies that chunk indices are embedded in the prompt context."""
    chunks: list[RankedChunk] = [
        {"index": 3, "text": "Chunk three.", "score": 0.9},
    ]
    prompt = build_prompt("Query?", chunks)
    assert "[3]" in prompt
