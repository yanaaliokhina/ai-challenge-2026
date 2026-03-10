"""Tests for index_loader module."""

import json
import pytest
from unittest.mock import patch
from pathlib import Path
from src.index_loader import load_index, IndexEntry


def test_load_index_valid_file_returns_entries(tmp_path):
    """Verifies that a valid index JSON file is loaded and parsed into IndexEntry objects."""
    data = [
        {"id": "a", "text": "hello world", "embedding": [0.1, 0.2, 0.3]},
        {"id": "b", "text": "foo bar", "embedding": [0.4, 0.5, 0.6]},
    ]
    f = tmp_path / "index.json"
    f.write_text(json.dumps(data))
    entries = load_index(str(f))
    assert len(entries) == 2
    assert entries[0].id == "a"
    assert entries[1].text == "foo bar"
    assert entries[0].embedding == [0.1, 0.2, 0.3]


def test_load_index_missing_file_exits_with_code_1(tmp_path):
    """Verifies that a missing index file causes sys.exit(1)."""
    with pytest.raises(SystemExit) as exc:
        load_index(str(tmp_path / "nonexistent.json"))
    assert exc.value.code == 1


def test_load_index_invalid_json_exits_with_code_1(tmp_path):
    """Verifies that invalid JSON in the index file causes sys.exit(1)."""
    f = tmp_path / "index.json"
    f.write_text("not valid json {{{")
    with pytest.raises(SystemExit) as exc:
        load_index(str(f))
    assert exc.value.code == 1


def test_load_index_empty_list_exits_with_code_1(tmp_path):
    """Verifies that an empty list in the index file causes sys.exit(1)."""
    f = tmp_path / "index.json"
    f.write_text("[]")
    with pytest.raises(SystemExit) as exc:
        load_index(str(f))
    assert exc.value.code == 1


def test_load_index_malformed_entry_exits_with_code_1(tmp_path):
    """Verifies that a malformed entry (missing required field) causes sys.exit(1)."""
    data = [{"id": "x", "embedding": [0.1, 0.2]}]
    f = tmp_path / "index.json"
    f.write_text(json.dumps(data))
    with pytest.raises(SystemExit) as exc:
        load_index(str(f))
    assert exc.value.code == 1


def test_load_index_single_entry_returns_list_of_one(tmp_path):
    """Verifies that a single-entry index is returned as a one-element list."""
    data = [{"id": "only", "text": "sole entry", "embedding": [1.0]}]
    f = tmp_path / "index.json"
    f.write_text(json.dumps(data))
    entries = load_index(str(f))
    assert len(entries) == 1
    assert entries[0].id == "only"
