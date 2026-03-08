"""Tests for document parser — strip_markdown, preprocess, and parse_file."""

import pytest
from unittest.mock import mock_open, patch, MagicMock
from pathlib import Path

from src.parser import strip_markdown, preprocess, parse_file


class TestStripMarkdown:
    def test_strip_markdown_removes_h1_header(self):
        """Verifies that a level-1 header marker is removed."""
        assert strip_markdown("# Title\n") == "Title\n"

    def test_strip_markdown_removes_h3_header(self):
        """Verifies that a level-3 header marker is removed."""
        assert strip_markdown("### Section\n") == "Section\n"

    def test_strip_markdown_removes_bold(self):
        """Verifies that bold markers are removed and inner text is preserved."""
        assert strip_markdown("This is **bold** text.") == "This is bold text."

    def test_strip_markdown_removes_italic(self):
        """Verifies that italic markers are removed and inner text is preserved."""
        assert strip_markdown("This is *italic* text.") == "This is italic text."

    def test_strip_markdown_removes_inline_code(self):
        """Verifies that backtick inline code markers are removed."""
        assert strip_markdown("Use `print()` here.") == "Use print() here."

    def test_strip_markdown_removes_link_keeps_text(self):
        """Verifies that Markdown links are replaced by their display text."""
        assert strip_markdown("[OpenAI](https://openai.com)") == "OpenAI"

    def test_strip_markdown_preserves_plain_text(self):
        """Verifies that plain text without Markdown is returned unchanged."""
        text = "Hello world. No formatting here."
        assert strip_markdown(text) == text

    def test_strip_markdown_handles_multiple_headers(self):
        """Verifies that multiple headers on separate lines are all stripped."""
        text = "# One\n## Two\n### Three\n"
        result = strip_markdown(text)
        assert "#" not in result
        assert "One" in result and "Two" in result and "Three" in result


class TestPreprocess:
    def test_preprocess_strips_leading_whitespace(self):
        """Verifies that leading whitespace is removed."""
        assert preprocess("   hello") == "hello"

    def test_preprocess_strips_trailing_whitespace(self):
        """Verifies that trailing whitespace is removed."""
        assert preprocess("hello   ") == "hello"

    def test_preprocess_collapses_three_blank_lines_to_one(self):
        """Verifies that three consecutive blank lines are collapsed to one."""
        result = preprocess("a\n\n\nb")
        assert result == "a\n\nb"

    def test_preprocess_collapses_many_blank_lines_to_one(self):
        """Verifies that many consecutive blank lines are collapsed to one."""
        result = preprocess("a\n\n\n\n\nb")
        assert result == "a\n\nb"

    def test_preprocess_preserves_single_blank_line(self):
        """Verifies that a single blank line between paragraphs is preserved."""
        result = preprocess("para one\n\npara two")
        assert result == "para one\n\npara two"

    def test_preprocess_empty_string(self):
        """Verifies that an empty string is returned as-is."""
        assert preprocess("") == ""


class TestParseFile:
    def test_parse_file_unsupported_extension_exits(self, tmp_path):
        """Verifies that an unsupported file extension causes a SystemExit with code 1."""
        pdf_file = tmp_path / "report.pdf"
        pdf_file.write_text("content")
        with pytest.raises(SystemExit) as exc_info:
            parse_file(str(pdf_file))
        assert exc_info.value.code == 1

    def test_parse_file_txt_returns_raw_content(self, tmp_path):
        """Verifies that a .txt file is read and preprocessed without markdown stripping."""
        txt_file = tmp_path / "doc.txt"
        txt_file.write_text("Hello world.\n\n\nNew paragraph.")
        result = parse_file(str(txt_file))
        assert result == "Hello world.\n\nNew paragraph."

    def test_parse_file_md_strips_markdown(self, tmp_path):
        """Verifies that a .md file has Markdown formatting stripped."""
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Title\n\nSome **bold** text.")
        result = parse_file(str(md_file))
        assert "#" not in result
        assert "**" not in result
        assert "Title" in result
        assert "bold" in result

    def test_parse_file_encoding_error_exits(self, tmp_path):
        """Verifies that a non-UTF-8 file causes a SystemExit with code 1."""
        bad_file = tmp_path / "bad.txt"
        bad_file.write_bytes(b"\xff\xfe invalid utf-8 \x80\x81")
        with pytest.raises(SystemExit) as exc_info:
            parse_file(str(bad_file))
        assert exc_info.value.code == 1
