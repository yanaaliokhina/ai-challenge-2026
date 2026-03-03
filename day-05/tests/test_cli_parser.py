"""Tests for cli_parser.py — verifies argument parsing behaviour."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cli_parser import parse_args
from constants import DEFAULT_MODEL


def test_prompt_mode_sets_prompt():
    """--prompt sets the prompt attribute and interactive is False."""
    args = parse_args(["--prompt", "hello"])
    assert args.prompt == "hello"
    assert not args.interactive


def test_interactive_mode_sets_flag():
    """--interactive sets the interactive flag and prompt is None."""
    args = parse_args(["--interactive"])
    assert args.interactive
    assert args.prompt is None


def test_short_interactive_flag():
    """-i is accepted as an alias for --interactive."""
    args = parse_args(["-i"])
    assert args.interactive


def test_prompt_and_interactive_are_mutually_exclusive():
    """--prompt and --interactive together raises SystemExit."""
    with pytest.raises(SystemExit):
        parse_args(["--prompt", "hi", "--interactive"])


def test_no_mode_flag_raises_system_exit():
    """Omitting both --prompt and --interactive raises SystemExit."""
    with pytest.raises(SystemExit):
        parse_args([])


def test_default_model_is_applied():
    """--model defaults to DEFAULT_MODEL when not provided."""
    args = parse_args(["--prompt", "hi"])
    assert args.model == DEFAULT_MODEL


def test_custom_model_is_applied():
    """--model overrides the default model value."""
    args = parse_args(["--prompt", "hi", "--model", "claude-opus-4-6"])
    assert args.model == "claude-opus-4-6"


def test_system_default_is_none():
    """--system defaults to None when not provided."""
    args = parse_args(["--prompt", "hi"])
    assert args.system is None


def test_system_flag_sets_value():
    """--system sets the system attribute."""
    args = parse_args(["--prompt", "hi", "--system", "You are a pirate"])
    assert args.system == "You are a pirate"


def test_verbose_default_is_false():
    """--verbose defaults to False when not provided."""
    args = parse_args(["--prompt", "hi"])
    assert not args.verbose


def test_verbose_flag_sets_true():
    """--verbose sets verbose to True."""
    args = parse_args(["--prompt", "hi", "--verbose"])
    assert args.verbose


def test_short_verbose_flag():
    """-v is accepted as an alias for --verbose."""
    args = parse_args(["--prompt", "hi", "-v"])
    assert args.verbose
