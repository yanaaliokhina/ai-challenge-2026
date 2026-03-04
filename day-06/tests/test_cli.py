"""Tests for cli_parser.py argument parsing."""

import sys
import pytest
from cli_parser import CLIParser


def _parse(args: list[str]):
    """Helper: set sys.argv and parse args."""
    sys.argv = ["main.py"] + args
    return CLIParser().parse_args()


def test_parse_args_text_argument_sets_text():
    """--text argument is correctly parsed into args.text."""
    args = _parse(["--text", "Hello world"])
    assert args.text == "Hello world"


def test_parse_args_file_argument_sets_file():
    """--file argument is correctly parsed into args.file."""
    args = _parse(["--file", "data/sample.txt"])
    assert args.file == "data/sample.txt"


def test_parse_args_batch_argument_sets_batch():
    """--batch argument is correctly parsed into args.batch."""
    args = _parse(["--batch", "data/prompts.txt"])
    assert args.batch == "data/prompts.txt"


def test_parse_args_default_model_is_gpt4o():
    """Default model is gpt-4o when --model is not specified."""
    args = _parse(["--text", "hi"])
    assert args.model == "gpt-4o"


def test_parse_args_model_argument_overrides_default():
    """--model argument overrides the default model."""
    args = _parse(["--text", "hi", "--model", "gpt-4"])
    assert args.model == "gpt-4"


def test_parse_args_verbose_defaults_to_false():
    """--verbose flag defaults to False when not provided."""
    args = _parse(["--text", "hi"])
    assert args.verbose is False


def test_parse_args_verbose_flag_sets_true():
    """--verbose flag is True when provided."""
    args = _parse(["--text", "hi", "--verbose"])
    assert args.verbose is True


def test_parse_args_no_text_no_file_sets_both_to_none():
    """args.text and args.file are None when neither flag is provided."""
    args = _parse([])
    assert args.text is None
    assert args.file is None


def test_parse_args_batch_with_model():
    """--batch and --model can be combined."""
    args = _parse(["--batch", "data/prompts.txt", "--model", "claude-3-haiku"])
    assert args.batch == "data/prompts.txt"
    assert args.model == "claude-3-haiku"
