"""Tests for the main orchestration logic — results writing, latency, error handling, and summary."""

import json
from unittest.mock import MagicMock, patch

import pytest

def _make_args(prompts_file: str, output_file: str, model: str = "claude-haiku-4-5-20251001"):
    args = MagicMock()
    args.prompts_file = prompts_file
    args.output_file = output_file
    args.model = model
    return args


def _mock_llm_client(responses: list):
    """Returns a mock LLMClient whose ask() returns (text, latency) from the given list in order."""
    client = MagicMock()
    client.ask.side_effect = responses
    return client


def test_run_writes_results_file_with_required_fields(tmp_path, monkeypatch):
    """Verifies that run() writes a JSON results file containing all required fields."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    prompts = [{"id": "v1", "prompt": "Hello", "label": "greeting"}]
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text(json.dumps(prompts))
    output_file = tmp_path / "results.json"

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([("Hi there", 123.4)])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    results = json.loads(output_file.read_text())
    assert len(results) == 1
    r = results[0]
    assert r["id"] == "v1"
    assert r["label"] == "greeting"
    assert r["prompt"] == "Hello"
    assert r["response"] == "Hi there"
    assert r["latency_ms"] == pytest.approx(123.4)
    assert r["error"] is None


def test_run_records_null_label_when_absent(tmp_path, monkeypatch):
    """Verifies that entries without a label field produce null in the results."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    prompts = [{"id": "v2", "prompt": "No label"}]
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text(json.dumps(prompts))
    output_file = tmp_path / "results.json"

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([("response", 50.0)])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    results = json.loads(output_file.read_text())
    assert results[0]["label"] is None


def test_run_continues_after_failed_prompt(tmp_path, monkeypatch, capsys):
    """Verifies that a failing API call records the error and processing continues."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    prompts = [
        {"id": "ok", "prompt": "Good prompt"},
        {"id": "bad", "prompt": "Bad prompt"},
        {"id": "ok2", "prompt": "Also good"},
    ]
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text(json.dumps(prompts))
    output_file = tmp_path / "results.json"

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([
        ("Success", 100.0),
        Exception("API error 500"),
        ("Also success", 80.0),
    ])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    results = json.loads(output_file.read_text())
    assert len(results) == 3
    assert results[0]["response"] == "Success"
    assert results[0]["error"] is None
    assert results[1]["response"] is None
    assert results[1]["error"] == "API error 500"
    assert results[2]["response"] == "Also success"


def test_run_prints_summary_to_stdout(tmp_path, monkeypatch, capsys):
    """Verifies that run() prints a summary with totals, successes, failures, and average latency."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    prompts = [
        {"id": "p1", "prompt": "Prompt 1"},
        {"id": "p2", "prompt": "Prompt 2"},
    ]
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text(json.dumps(prompts))
    output_file = tmp_path / "results.json"

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([("R1", 200.0), ("R2", 400.0)])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    captured = capsys.readouterr().out
    assert "Total prompts attempted: 2" in captured
    assert "Successful responses:    2" in captured
    assert "Failures:                0" in captured
    assert "300.0" in captured


def test_run_summary_with_all_failures(tmp_path, monkeypatch, capsys):
    """Verifies that average latency shows 0.0 when all prompts fail."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    prompts = [{"id": "f1", "prompt": "Will fail"}]
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text(json.dumps(prompts))
    output_file = tmp_path / "results.json"

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([Exception("timeout")])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    captured = capsys.readouterr().out
    assert "Failures:                1" in captured
    assert "0.0" in captured


def test_run_overwrites_existing_output_file(tmp_path, monkeypatch):
    """Verifies that an existing output file is overwritten without error."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    prompts = [{"id": "x", "prompt": "Overwrite test"}]
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text(json.dumps(prompts))
    output_file = tmp_path / "results.json"
    output_file.write_text("old content")

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([("New response", 10.0)])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    results = json.loads(output_file.read_text())
    assert results[0]["response"] == "New response"


def test_run_with_jsonl_input(tmp_path, monkeypatch):
    """Verifies that run() correctly processes a .jsonl input file."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    lines = [
        json.dumps({"id": "j1", "prompt": "JSONL prompt 1"}),
        json.dumps({"id": "j2", "prompt": "JSONL prompt 2", "label": "test"}),
    ]
    prompts_file = tmp_path / "prompts.jsonl"
    prompts_file.write_text("\n".join(lines))
    output_file = tmp_path / "out.json"

    args = _make_args(str(prompts_file), str(output_file))
    client = _mock_llm_client([("R1", 50.0), ("R2", 60.0)])

    with patch("main.CLIParser") as MockParser, patch("main.LLMClient", return_value=client):
        MockParser.return_value.parse_args.return_value = args
        from main import run
        run()

    results = json.loads(output_file.read_text())
    assert len(results) == 2
    assert results[1]["label"] == "test"
