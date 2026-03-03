"""Tests for main.py — verifies single-shot, interactive, and verbose behaviour."""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch, call

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import run_single_shot, run_interactive, _print_verbose


def _make_args(prompt=None, interactive=False, system=None, model="claude-haiku-4-5-20251001", verbose=False):
    """Build a mock argparse.Namespace."""
    args = MagicMock()
    args.prompt = prompt
    args.interactive = interactive
    args.system = system
    args.model = model
    args.verbose = verbose
    return args


def test_run_single_shot_prints_response(capsys):
    """run_single_shot prints the LLM response to stdout."""
    client = MagicMock()
    client.ask.return_value = "The answer is 4."
    args = _make_args(prompt="What is 2+2?")
    run_single_shot(args, client)
    captured = capsys.readouterr()
    assert "The answer is 4." in captured.out


def test_run_single_shot_passes_prompt_to_client():
    """run_single_shot calls client.ask with the correct prompt."""
    client = MagicMock()
    client.ask.return_value = "ok"
    args = _make_args(prompt="Hello")
    run_single_shot(args, client)
    client.ask.assert_called_once_with("Hello", system=None, model=args.model)


def test_run_single_shot_passes_system_to_client():
    """run_single_shot forwards the system prompt to client.ask."""
    client = MagicMock()
    client.ask.return_value = "ok"
    args = _make_args(prompt="Hello", system="You are a pirate")
    run_single_shot(args, client)
    client.ask.assert_called_once_with("Hello", system="You are a pirate", model=args.model)


def test_run_single_shot_verbose_writes_to_stderr(capsys):
    """run_single_shot with verbose writes metadata to stderr."""
    client = MagicMock()
    client.ask.return_value = "ok"
    args = _make_args(prompt="Hello", verbose=True, system="sys")
    run_single_shot(args, client)
    captured = capsys.readouterr()
    assert "[verbose]" in captured.err
    assert "Hello" in captured.err


def test_run_single_shot_no_verbose_no_stderr(capsys):
    """run_single_shot without verbose writes nothing to stderr."""
    client = MagicMock()
    client.ask.return_value = "ok"
    args = _make_args(prompt="Hello", verbose=False)
    run_single_shot(args, client)
    captured = capsys.readouterr()
    assert captured.err == ""


def test_run_interactive_exits_on_quit(monkeypatch, capsys):
    """run_interactive exits the loop when the user types 'quit'."""
    inputs = iter(["quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    client = MagicMock()
    args = _make_args(interactive=True)
    run_interactive(args, client)
    client.ask.assert_not_called()


def test_run_interactive_exits_on_exit(monkeypatch):
    """run_interactive exits the loop when the user types 'exit'."""
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    client = MagicMock()
    args = _make_args(interactive=True)
    run_interactive(args, client)
    client.ask.assert_not_called()


def test_run_interactive_exits_on_eof(monkeypatch):
    """run_interactive exits the loop cleanly on EOFError (Ctrl+D)."""
    monkeypatch.setattr("builtins.input", MagicMock(side_effect=EOFError))
    client = MagicMock()
    args = _make_args(interactive=True)
    run_interactive(args, client)
    client.ask.assert_not_called()


def test_run_interactive_sends_prompt_and_prints_response(monkeypatch, capsys):
    """run_interactive sends user input to client.ask and prints the response."""
    inputs = iter(["Hello", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    client = MagicMock()
    client.ask.return_value = "Hi there!"
    args = _make_args(interactive=True)
    run_interactive(args, client)
    client.ask.assert_called_once_with("Hello", system=None, model=args.model)
    captured = capsys.readouterr()
    assert "Assistant: Hi there!" in captured.out


def test_run_interactive_skips_empty_input(monkeypatch):
    """run_interactive skips blank lines without calling client.ask."""
    inputs = iter(["", "  ", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    client = MagicMock()
    args = _make_args(interactive=True)
    run_interactive(args, client)
    client.ask.assert_not_called()


def test_run_interactive_continues_on_runtime_error(monkeypatch, capsys):
    """run_interactive prints the error and continues the loop on RuntimeError."""
    inputs = iter(["bad", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    client = MagicMock()
    client.ask.side_effect = RuntimeError("API error 500: internal")
    args = _make_args(interactive=True)
    run_interactive(args, client)
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_print_verbose_outputs_model_system_prompt(capsys):
    """_print_verbose writes model, system, and prompt lines to stderr."""
    _print_verbose("claude-haiku-4-5-20251001", "Be helpful", "What is AI?")
    captured = capsys.readouterr()
    assert "claude-haiku-4-5-20251001" in captured.err
    assert "Be helpful" in captured.err
    assert "What is AI?" in captured.err


def test_print_verbose_shows_none_for_missing_system(capsys):
    """_print_verbose shows '(none)' when system is None."""
    _print_verbose("model", None, "prompt")
    captured = capsys.readouterr()
    assert "(none)" in captured.err
