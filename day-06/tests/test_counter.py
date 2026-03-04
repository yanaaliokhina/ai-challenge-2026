"""Tests for counter.py token counting logic."""

from unittest.mock import MagicMock, patch
import pytest
from counter import count_tokens, get_token_strings, get_encoding


def _make_mock_enc(token_ids: list[int], decoded_map: dict[int, str]) -> MagicMock:
    """Build a reusable mock tiktoken encoding."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = token_ids
    mock_enc.decode.side_effect = lambda ids: decoded_map[ids[0]]
    return mock_enc


@patch("counter.tiktoken.get_encoding")
def test_count_tokens_simple_text_returns_correct_count(mock_get_encoding):
    """count_tokens returns the number of token IDs returned by the encoder."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = [15496, 995]
    mock_get_encoding.return_value = mock_enc

    result = count_tokens("Hello world", "gpt-4o")

    assert result == 2


@patch("counter.tiktoken.get_encoding")
def test_count_tokens_empty_string_returns_zero(mock_get_encoding):
    """count_tokens returns 0 for an empty string."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = []
    mock_get_encoding.return_value = mock_enc

    result = count_tokens("", "gpt-4o")

    assert result == 0


@patch("counter.tiktoken.get_encoding")
def test_count_tokens_uses_correct_encoding_for_gpt4o(mock_get_encoding):
    """count_tokens requests o200k_base encoding for gpt-4o."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = [1]
    mock_get_encoding.return_value = mock_enc

    count_tokens("test", "gpt-4o")

    mock_get_encoding.assert_called_once_with("o200k_base")


@patch("counter.tiktoken.get_encoding")
def test_count_tokens_uses_correct_encoding_for_gpt4(mock_get_encoding):
    """count_tokens requests cl100k_base encoding for gpt-4."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = [1]
    mock_get_encoding.return_value = mock_enc

    count_tokens("test", "gpt-4")

    mock_get_encoding.assert_called_once_with("cl100k_base")


@patch("counter.tiktoken.get_encoding")
def test_count_tokens_uses_correct_encoding_for_claude(mock_get_encoding):
    """count_tokens requests cl100k_base encoding for claude-3-5-sonnet."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = [1]
    mock_get_encoding.return_value = mock_enc

    count_tokens("test", "claude-3-5-sonnet")

    mock_get_encoding.assert_called_once_with("cl100k_base")


@patch("counter.tiktoken.get_encoding")
def test_get_token_strings_returns_decoded_list(mock_get_encoding):
    """get_token_strings returns a list of decoded token strings."""
    mock_enc = _make_mock_enc([15496, 995], {15496: "Hello", 995: " world"})
    mock_get_encoding.return_value = mock_enc

    result = get_token_strings("Hello world", "gpt-4o")

    assert result == ["Hello", " world"]


@patch("counter.tiktoken.get_encoding")
def test_get_token_strings_empty_text_returns_empty_list(mock_get_encoding):
    """get_token_strings returns an empty list for empty input text."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = []
    mock_get_encoding.return_value = mock_enc

    result = get_token_strings("", "gpt-4o")

    assert result == []


@patch("counter.tiktoken.get_encoding")
def test_get_token_strings_length_matches_count_tokens(mock_get_encoding):
    """get_token_strings length equals count_tokens for the same text."""
    mock_enc = MagicMock()
    mock_enc.encode.return_value = [1, 2, 3, 4]
    mock_enc.decode.side_effect = lambda ids: str(ids[0])
    mock_get_encoding.return_value = mock_enc

    token_strings = get_token_strings("some text here", "gpt-4")
    token_count = count_tokens("some text here", "gpt-4")

    assert len(token_strings) == token_count


@patch("counter.tiktoken.get_encoding")
def test_count_tokens_long_text_returns_large_count(mock_get_encoding):
    """count_tokens handles a large number of tokens correctly."""
    large_token_list = list(range(5000))
    mock_enc = MagicMock()
    mock_enc.encode.return_value = large_token_list
    mock_get_encoding.return_value = mock_enc

    result = count_tokens("x " * 5000, "gpt-4o")

    assert result == 5000
