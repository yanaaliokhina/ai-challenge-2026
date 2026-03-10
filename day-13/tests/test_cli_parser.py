"""Tests for cli_parser module."""

import pytest
from src.cli_parser import CLIParser
from src.constants import DEFAULT_EMBEDDING_MODEL, DEFAULT_TOP_N


def test_cli_parser_default_top_n(monkeypatch):
    """Verifies that --top defaults to DEFAULT_TOP_N when not provided."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", "idx.json", "--query", "hello"])
    args = CLIParser().parse_args()
    assert args.top == DEFAULT_TOP_N


def test_cli_parser_default_model(monkeypatch):
    """Verifies that --model defaults to DEFAULT_EMBEDDING_MODEL when not provided."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", "idx.json", "--query", "hello"])
    args = CLIParser().parse_args()
    assert args.model == DEFAULT_EMBEDDING_MODEL


def test_cli_parser_custom_top(monkeypatch):
    """Verifies that a custom --top value is parsed correctly."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", "idx.json", "--query", "hello", "--top", "5"])
    args = CLIParser().parse_args()
    assert args.top == 5


def test_cli_parser_custom_model(monkeypatch):
    """Verifies that a custom --model value is parsed correctly."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", "idx.json", "--query", "hello", "--model", "text-embedding-3-large"])
    args = CLIParser().parse_args()
    assert args.model == "text-embedding-3-large"


def test_cli_parser_missing_index_exits(monkeypatch):
    """Verifies that omitting --index causes argparse to exit."""
    monkeypatch.setattr("sys.argv", ["main.py", "--query", "hello"])
    with pytest.raises(SystemExit):
        CLIParser().parse_args()


def test_cli_parser_missing_query_exits(monkeypatch):
    """Verifies that omitting --query causes argparse to exit."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", "idx.json"])
    with pytest.raises(SystemExit):
        CLIParser().parse_args()


def test_cli_parser_index_and_query_are_set(monkeypatch):
    """Verifies that --index and --query values are captured correctly."""
    monkeypatch.setattr("sys.argv", ["main.py", "--index", "my_index.json", "--query", "test query"])
    args = CLIParser().parse_args()
    assert args.index == "my_index.json"
    assert args.query == "test query"
