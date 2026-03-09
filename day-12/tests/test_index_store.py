"""Tests for the index_store module."""

import json
import pytest
from unittest.mock import patch, mock_open
from src.index_store import (
    load_index,
    save_index,
    get_indexed_texts,
    add_entry,
    cosine_similarity,
    query_index,
)


def test_load_index_returns_empty_list_when_file_missing(tmp_path):
    """Verifies that loading a non-existent file returns an empty list."""
    result = load_index(str(tmp_path / "missing.json"))
    assert result == []


def test_load_index_returns_parsed_entries(tmp_path):
    """Verifies that existing index data is loaded and parsed correctly."""
    data = [{"id": "1", "text": "hello", "embedding": [0.1, 0.2]}]
    index_file = tmp_path / "index.json"
    index_file.write_text(json.dumps(data))
    result = load_index(str(index_file))
    assert result == data


def test_save_index_writes_valid_json(tmp_path):
    """Verifies that save_index writes correctly formatted JSON."""
    index = [{"id": "abc", "text": "chunk", "embedding": [0.5, 0.5]}]
    path = str(tmp_path / "index.json")
    save_index(index, path)
    with open(path) as f:
        loaded = json.load(f)
    assert loaded == index


def test_save_and_load_roundtrip(tmp_path):
    """Verifies that data saved and then loaded is identical."""
    index = [{"id": "x", "text": "some text", "embedding": [1.0, 0.0]}]
    path = str(tmp_path / "index.json")
    save_index(index, path)
    assert load_index(path) == index


def test_get_indexed_texts_returns_set_of_texts():
    """Verifies that get_indexed_texts extracts the text field from each entry."""
    index = [
        {"id": "1", "text": "alpha", "embedding": []},
        {"id": "2", "text": "beta", "embedding": []},
    ]
    result = get_indexed_texts(index)
    assert result == {"alpha", "beta"}


def test_get_indexed_texts_empty_index():
    """Verifies that an empty index yields an empty set."""
    assert get_indexed_texts([]) == set()


def test_add_entry_appends_to_index():
    """Verifies that add_entry adds a new entry to the index list."""
    index = []
    add_entry(index, "hello world", [0.1, 0.9])
    assert len(index) == 1
    assert index[0]["text"] == "hello world"
    assert index[0]["embedding"] == [0.1, 0.9]
    assert "id" in index[0]


def test_add_entry_returns_the_new_entry():
    """Verifies that add_entry returns the newly created entry dict."""
    index = []
    entry = add_entry(index, "test", [1.0])
    assert entry is index[0]


def test_add_entry_unique_ids():
    """Verifies that each call to add_entry produces a unique id."""
    index = []
    add_entry(index, "a", [0.0])
    add_entry(index, "b", [1.0])
    assert index[0]["id"] != index[1]["id"]


def test_cosine_similarity_identical_vectors():
    """Verifies that identical vectors have similarity of 1.0."""
    v = [1.0, 0.0, 0.0]
    assert abs(cosine_similarity(v, v) - 1.0) < 1e-9


def test_cosine_similarity_orthogonal_vectors():
    """Verifies that orthogonal vectors have similarity of 0.0."""
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert abs(cosine_similarity(a, b)) < 1e-9


def test_cosine_similarity_opposite_vectors():
    """Verifies that opposite vectors have similarity of -1.0."""
    a = [1.0, 0.0]
    b = [-1.0, 0.0]
    assert abs(cosine_similarity(a, b) - (-1.0)) < 1e-9


def test_cosine_similarity_zero_vector_returns_zero():
    """Verifies that a zero vector yields similarity of 0.0."""
    assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_query_index_returns_top_n_results():
    """Verifies that query_index returns exactly top_n results."""
    index = [
        {"id": "1", "text": "one", "embedding": [1.0, 0.0]},
        {"id": "2", "text": "two", "embedding": [0.0, 1.0]},
        {"id": "3", "text": "three", "embedding": [0.7, 0.7]},
    ]
    query_emb = [1.0, 0.0]
    results = query_index(index, query_emb, top_n=2)
    assert len(results) == 2


def test_query_index_sorted_by_score_descending():
    """Verifies that results are ordered by score from highest to lowest."""
    index = [
        {"id": "1", "text": "low", "embedding": [0.0, 1.0]},
        {"id": "2", "text": "high", "embedding": [1.0, 0.0]},
    ]
    query_emb = [1.0, 0.0]
    results = query_index(index, query_emb, top_n=2)
    assert results[0]["text"] == "high"
    assert results[0]["score"] > results[1]["score"]


def test_query_index_top_n_greater_than_entries():
    """Verifies that top_n larger than index size returns all entries."""
    index = [{"id": "1", "text": "only", "embedding": [1.0, 0.0]}]
    results = query_index(index, [1.0, 0.0], top_n=10)
    assert len(results) == 1


def test_query_index_empty_index_returns_empty():
    """Verifies that querying an empty index returns an empty list."""
    results = query_index([], [1.0, 0.0], top_n=3)
    assert results == []
