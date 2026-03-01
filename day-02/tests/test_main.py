import pytest
from unittest.mock import patch
from src.main import main


def test_cli_renders_translate_template(capsys):
    """Verifies that the CLI renders the translate template with provided variables."""
    with patch("sys.argv", ["main", "--template", "translate", "--var", "text=Hello", "--var", "language=French"]):
        main()
    captured = capsys.readouterr()
    assert "Hello" in captured.out
    assert "French" in captured.out


def test_cli_renders_summarise_template(capsys):
    """Verifies that the CLI renders the summarise template with provided variables."""
    with patch("sys.argv", ["main", "--template", "summarise", "--var", "text=Long text.", "--var", "num_sentences=2"]):
        main()
    captured = capsys.readouterr()
    assert "Long text." in captured.out
    assert "2" in captured.out


def test_cli_renders_qa_template(capsys):
    """Verifies that the CLI renders the qa template with provided variables."""
    with patch("sys.argv", [
        "main", "--template", "qa",
        "--var", "question=What is AI?",
        "--var", "context=AI is artificial intelligence.",
    ]):
        main()
    captured = capsys.readouterr()
    assert "What is AI?" in captured.out
    assert "AI is artificial intelligence." in captured.out


def test_cli_exits_with_code_1_on_missing_variable(capsys):
    """Verifies that the CLI exits with code 1 when a required variable is missing."""
    with patch("sys.argv", ["main", "--template", "translate", "--var", "text=Hello"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "language" in captured.err


def test_cli_exits_with_code_1_on_unknown_template(capsys):
    """Verifies that the CLI exits with code 1 when an unknown template name is given."""
    with patch("sys.argv", ["main", "--template", "nonexistent"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1


def test_cli_exits_with_code_1_on_extra_variable(capsys):
    """Verifies that the CLI exits with code 1 when extra/unknown variables are passed."""
    with patch("sys.argv", [
        "main", "--template", "translate",
        "--var", "text=Hi",
        "--var", "language=French",
        "--var", "extra=oops",
    ]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "extra" in captured.err


def test_cli_prints_error_to_stderr_on_missing_variable(capsys):
    """Verifies that the CLI prints an error message to stderr when variables are missing."""
    with patch("sys.argv", ["main", "--template", "translate"]):
        with pytest.raises(SystemExit):
            main()
    captured = capsys.readouterr()
    assert len(captured.err) > 0


def test_cli_output_contains_rendered_result(capsys):
    """Verifies that the CLI prints the rendered result to stdout."""
    with patch("sys.argv", ["main", "--template", "qa", "--var", "question=Q?", "--var", "context=C."]):
        main()
    captured = capsys.readouterr()
    assert "Q?" in captured.out
    assert "C." in captured.out
