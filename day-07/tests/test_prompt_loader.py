"""Tests for the prompt_loader module."""

import json
import pytest

from src.prompt_loader import load_prompts


def test_load_prompts_json_returns_all_entries(tmp_path):
    """Verifies that a valid .json file with multiple entries is loaded correctly."""
    data = [
        {"id": "v1", "prompt": "Hello"},
        {"id": "v2", "prompt": "Hi", "label": "casual"},
    ]
    f = tmp_path / "prompts.json"
    f.write_text(json.dumps(data))
    result = load_prompts(str(f))
    assert len(result) == 2
    assert result[0]["id"] == "v1"
    assert result[1]["label"] == "casual"


def test_load_prompts_jsonl_returns_all_entries(tmp_path):
    """Verifies that a valid .jsonl file with multiple lines is loaded correctly."""
    lines = [
        json.dumps({"id": "a", "prompt": "Prompt A"}),
        json.dumps({"id": "b", "prompt": "Prompt B", "label": "formal"}),
    ]
    f = tmp_path / "prompts.jsonl"
    f.write_text("\n".join(lines) + "\n")
    result = load_prompts(str(f))
    assert len(result) == 2
    assert result[1]["id"] == "b"


def test_load_prompts_jsonl_skips_blank_lines(tmp_path):
    """Verifies that blank lines in a .jsonl file are ignored."""
    lines = [
        json.dumps({"id": "x", "prompt": "X"}),
        "",
        json.dumps({"id": "y", "prompt": "Y"}),
    ]
    f = tmp_path / "prompts.jsonl"
    f.write_text("\n".join(lines))
    result = load_prompts(str(f))
    assert len(result) == 2


def test_load_prompts_missing_file_exits(tmp_path):
    """Verifies that a missing input file causes a SystemExit with non-zero code."""
    with pytest.raises(SystemExit) as exc_info:
        load_prompts(str(tmp_path / "nonexistent.json"))
    assert exc_info.value.code != 0


def test_load_prompts_invalid_json_exits(tmp_path):
    """Verifies that a malformed JSON file causes a SystemExit with non-zero code."""
    f = tmp_path / "bad.json"
    f.write_text("not valid json {{{")
    with pytest.raises(SystemExit) as exc_info:
        load_prompts(str(f))
    assert exc_info.value.code != 0


def test_load_prompts_invalid_jsonl_exits(tmp_path):
    """Verifies that a malformed JSONL file causes a SystemExit with non-zero code."""
    f = tmp_path / "bad.jsonl"
    f.write_text('{"id": "ok"}\nnot json\n')
    with pytest.raises(SystemExit) as exc_info:
        load_prompts(str(f))
    assert exc_info.value.code != 0


def test_load_prompts_json_single_entry(tmp_path):
    """Verifies that a JSON file with a single entry is loaded as a list of one."""
    data = [{"id": "solo", "prompt": "Just one"}]
    f = tmp_path / "single.json"
    f.write_text(json.dumps(data))
    result = load_prompts(str(f))
    assert len(result) == 1
    assert result[0]["id"] == "solo"


def test_load_prompts_entry_without_label(tmp_path):
    """Verifies that entries without a label field are loaded without error."""
    data = [{"id": "nolabel", "prompt": "No label here"}]
    f = tmp_path / "nolabel.json"
    f.write_text(json.dumps(data))
    result = load_prompts(str(f))
    assert "label" not in result[0]
