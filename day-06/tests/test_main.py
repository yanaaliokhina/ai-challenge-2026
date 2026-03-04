"""Tests for main.py orchestration logic."""

import sys
import pytest
from unittest.mock import patch, mock_open, MagicMock
from main import main, print_single_result, run_batch_mode


def _set_argv(args: list[str]):
    """Set sys.argv for a test."""
    sys.argv = ["main.py"] + args


# --- print_single_result ---

def test_print_single_result_fits_status(capsys):
    """FITS is shown when token count is within the context window."""
    print_single_result("argument", "gpt-4o", 100, False, [])
    out = capsys.readouterr().out
    assert "FITS" in out
    assert "gpt-4o" in out
    assert "100" in out


def test_print_single_result_exceeds_status(capsys):
    """EXCEEDS is shown when token count surpasses the context window."""
    print_single_result("file", "gpt-4", 9000, False, [])
    out = capsys.readouterr().out
    assert "EXCEEDS" in out


def test_print_single_result_verbose_shows_tokens_and_budget(capsys):
    """Verbose mode prints token strings and remaining budget."""
    print_single_result("argument", "gpt-4o", 5, True, ["Hello", " world"])
    out = capsys.readouterr().out
    assert "Tokens (decoded)" in out
    assert "Remaining budget" in out
    assert "Hello" in out


def test_print_single_result_usage_percentage_is_rounded(capsys):
    """Usage percentage is rounded to 2 decimal places."""
    print_single_result("argument", "gpt-4o", 1, False, [])
    out = capsys.readouterr().out
    assert "0.0%" in out or "0.00%" in out


# --- main: model validation ---

@patch("main.count_tokens", return_value=5)
@patch("main.get_token_strings", return_value=[])
def test_main_unsupported_model_exits_with_code_1(mock_gts, mock_ct, capsys):
    """Unsupported model causes exit with code 1 and prints error."""
    _set_argv(["--text", "hi", "--model", "gpt-99"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "Unsupported model" in err
    assert "gpt-99" in err


# --- main: text + file conflict ---

@patch("main.count_tokens", return_value=5)
@patch("main.get_token_strings", return_value=[])
def test_main_text_and_file_conflict_exits_with_code_1(mock_gts, mock_ct, capsys):
    """Providing both --text and --file causes exit with code 1."""
    _set_argv(["--text", "hello", "--file", "some.txt"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "either --text or --file" in err


# --- main: --text input ---

@patch("main.count_tokens", return_value=3)
@patch("main.get_token_strings", return_value=[])
def test_main_text_argument_prints_result(mock_gts, mock_ct, capsys):
    """--text input runs single mode and prints Source as 'argument'."""
    _set_argv(["--text", "Hello world"])
    main()
    out = capsys.readouterr().out
    assert "argument" in out
    assert "gpt-4o" in out


# --- main: --file missing ---

def test_main_missing_file_exits_with_code_1(capsys):
    """A missing --file path causes exit with code 1 and prints error."""
    _set_argv(["--file", "/nonexistent/path/file.txt"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "File not found" in err


# --- main: --file valid ---

@patch("main.count_tokens", return_value=10)
@patch("main.get_token_strings", return_value=[])
@patch("builtins.open", mock_open(read_data="Some file content here."))
def test_main_file_argument_prints_file_source(mock_gts, mock_ct, capsys):
    """--file input runs single mode and prints Source as 'file'."""
    _set_argv(["--file", "sample.txt"])
    main()
    out = capsys.readouterr().out
    assert "file" in out


# --- main: stdin ---

@patch("main.count_tokens", return_value=7)
@patch("main.get_token_strings", return_value=[])
@patch("sys.stdin")
def test_main_stdin_prints_stdin_source(mock_stdin, mock_gts, mock_ct, capsys):
    """stdin input runs single mode and prints Source as 'stdin'."""
    mock_stdin.read.return_value = "stdin text"
    _set_argv([])
    main()
    out = capsys.readouterr().out
    assert "stdin" in out


# --- run_batch_mode ---

@patch("main.count_tokens", side_effect=[4, 12, 7])
@patch("builtins.open", mock_open(read_data="First line\nSecond line here\nThird\n"))
def test_run_batch_mode_prints_summary(mock_ct, capsys):
    """Batch mode prints per-line results and a correct summary."""
    run_batch_mode("prompts.txt", "gpt-4o")
    out = capsys.readouterr().out
    assert "Line 1" in out
    assert "Line 2" in out
    assert "Line 3" in out
    assert "Summary" in out
    assert "Total lines:   3" in out
    assert "Total tokens:  23" in out
    assert "Min tokens:    4" in out
    assert "Max tokens:    12" in out


def test_run_batch_mode_missing_file_exits_with_code_1(capsys):
    """Batch mode with missing file exits with code 1 and prints error."""
    with pytest.raises(SystemExit) as exc:
        run_batch_mode("/nonexistent/prompts.txt", "gpt-4o")
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "File not found" in err


@patch("builtins.open", mock_open(read_data=""))
def test_run_batch_mode_empty_file_exits_with_code_0(capsys):
    """Batch mode with empty file prints warning and exits with code 0."""
    with pytest.raises(SystemExit) as exc:
        run_batch_mode("empty.txt", "gpt-4o")
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "Warning" in out
