"""Tests for CLI parsing, prompt loading, error isolation, ordering, and output format."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import src.main as main_module
from src.client import PromptResult
from src.main import print_results, run, run_prompt
from src.cli_parser import load_prompts

class _Args:
    def __init__(self, prompts=None, file=None):
        self.prompts = prompts or []
        self.file = file


def test_load_prompts_from_positional_args():
    """Verifies prompts are loaded from positional CLI arguments when no file is given."""
    assert load_prompts(_Args(prompts=["hello", "world"])) == ["hello", "world"]


def test_load_prompts_from_file(tmp_path):
    """Verifies prompts are loaded line-by-line from a plain-text file."""
    f = tmp_path / "prompts.txt"
    f.write_text("first prompt\nsecond prompt\n")
    assert load_prompts(_Args(file=str(f))) == ["first prompt", "second prompt"]


def test_load_prompts_file_takes_precedence_over_args(tmp_path):
    """Verifies --file takes precedence over positional arguments."""
    f = tmp_path / "p.txt"
    f.write_text("from file\n")
    assert load_prompts(_Args(prompts=["from args"], file=str(f))) == ["from file"]


def test_load_prompts_file_skips_blank_lines(tmp_path):
    """Verifies blank and whitespace-only lines in --file are ignored."""
    f = tmp_path / "p.txt"
    f.write_text("first\n\n   \nsecond\n")
    assert load_prompts(_Args(file=str(f))) == ["first", "second"]


def test_load_prompts_returns_empty_list_when_no_input():
    """Verifies load_prompts returns an empty list when no prompts and no file are given."""
    assert load_prompts(_Args()) == []


def test_run_prompt_success():
    """Verifies run_prompt returns PromptResult with success=True on a successful ask."""
    async def inner():
        mock_client = MagicMock()
        mock_client.ask = AsyncMock(return_value="Good answer")
        result = await run_prompt(mock_client, "My question")
        assert result.success is True
        assert result.response == "Good answer"
        assert result.prompt == "My question"

    asyncio.run(inner())


def test_run_prompt_error_isolation():
    """Verifies run_prompt catches exceptions and returns PromptResult with success=False."""
    async def inner():
        mock_client = MagicMock()
        mock_client.ask = AsyncMock(side_effect=RuntimeError("network failure"))
        result = await run_prompt(mock_client, "bad prompt")
        assert result.success is False
        assert "network failure" in result.response

    asyncio.run(inner())


def test_run_preserves_prompt_order():
    """Verifies results from run() are in the same order as input prompts."""
    responses = {"p1": "r1", "p2": "r2", "p3": "r3"}

    async def fake_ask(prompt):
        return responses[prompt]

    mock_client = MagicMock()
    mock_client.ask = fake_ask

    async def inner():
        with patch("src.main.AsyncLLMClient", return_value=mock_client):
            results, _ = await run(["p1", "p2", "p3"], "key")
        assert [r.prompt for r in results] == ["p1", "p2", "p3"]
        assert [r.response for r in results] == ["r1", "r2", "r3"]

    asyncio.run(inner())


def test_run_isolates_one_failed_prompt():
    """Verifies run() marks a failed prompt ERROR without cancelling other tasks."""
    async def fake_ask(prompt):
        if prompt == "bad":
            raise ValueError("boom")
        return f"ok:{prompt}"

    mock_client = MagicMock()
    mock_client.ask = fake_ask

    async def inner():
        with patch("src.main.AsyncLLMClient", return_value=mock_client):
            results, _ = await run(["good", "bad", "also good"], "key")
        assert results[0].success is True
        assert results[1].success is False
        assert "boom" in results[1].response
        assert results[2].success is True

    asyncio.run(inner())


def test_print_results_format(capsys):
    """Verifies print_results outputs index, status, response, and total time correctly."""
    results = [
        PromptResult(prompt="Short prompt", response="Answer", success=True),
        PromptResult(prompt="Another one", response="Failed msg", success=False),
    ]
    print_results(results, 1.23)
    out = capsys.readouterr().out
    assert "[1] Prompt: Short prompt" in out
    assert "    Status: OK" in out
    assert "    Response: Answer" in out
    assert "[2] Prompt: Another one" in out
    assert "    Status: ERROR" in out
    assert "Total time: 1.23s" in out


def test_print_results_truncates_prompt_to_60_chars(capsys):
    """Verifies print_results truncates prompts longer than 60 characters."""
    long_prompt = "A" * 80
    print_results([PromptResult(prompt=long_prompt, response="ok", success=True)], 0.5)
    out = capsys.readouterr().out
    assert "A" * 60 in out
    assert "A" * 61 not in out


def test_main_exits_on_empty_prompts(capsys):
    """Verifies main() exits with code 1 and prints an error when no prompts are given."""
    with patch("sys.argv", ["main.py"]):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "key"}):
            with pytest.raises(SystemExit) as exc:
                asyncio.run(main_module.main())
            assert exc.value.code == 1
    assert "no prompts" in capsys.readouterr().err


def test_main_exits_when_api_key_missing(monkeypatch, capsys):
    """Verifies main() exits with code 1 when ANTHROPIC_API_KEY is not set."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with patch("sys.argv", ["main.py", "hello"]):
        with pytest.raises(SystemExit) as exc:
            asyncio.run(main_module.main())
        assert exc.value.code == 1
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err
