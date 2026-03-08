"""Tests for token budget estimation and truncation."""

from src.token_budget import estimate_tokens, apply_budget


class TestEstimateTokens:
    def test_estimate_tokens_basic(self):
        """Verifies that token count is estimated as word_count / 0.75."""
        text = " ".join(["word"] * 75)
        assert estimate_tokens(text) == 100

    def test_estimate_tokens_empty_string(self):
        """Verifies that an empty string returns zero tokens."""
        assert estimate_tokens("") == 0

    def test_estimate_tokens_single_word(self):
        """Verifies that a single word returns the expected token estimate."""
        assert estimate_tokens("hello") == 1

    def test_estimate_tokens_truncates_fractional(self):
        """Verifies that fractional token estimates are truncated to int."""
        text = " ".join(["word"] * 10)
        result = estimate_tokens(text)
        assert isinstance(result, int)
        assert result == int(10 / 0.75)


class TestApplyBudget:
    def test_apply_budget_within_limit_returns_unchanged(self):
        """Verifies that text within the token budget is returned unchanged."""
        text = " ".join(["word"] * 75)
        result, truncated = apply_budget(text, max_tokens=200)
        assert result == text
        assert truncated is False

    def test_apply_budget_exceeds_limit_truncates(self):
        """Verifies that text exceeding the budget is truncated."""
        text = " ".join(["word"] * 750)
        result, truncated = apply_budget(text, max_tokens=100)
        assert truncated is True
        assert estimate_tokens(result) <= 100

    def test_apply_budget_truncated_text_is_shorter(self):
        """Verifies that truncated text is shorter than the original."""
        text = " ".join(["word"] * 750)
        result, _ = apply_budget(text, max_tokens=100)
        assert len(result.split()) < len(text.split())

    def test_apply_budget_no_exception_on_truncation(self):
        """Verifies that truncation does not raise an exception."""
        text = " ".join(["word"] * 750)
        try:
            apply_budget(text, max_tokens=50)
        except Exception as e:
            assert False, f"apply_budget raised an exception: {e}"

    def test_apply_budget_exactly_at_limit(self):
        """Verifies that text exactly at the token limit is not truncated."""
        target_words = int(100 * 0.75)
        text = " ".join(["word"] * target_words)
        result, truncated = apply_budget(text, max_tokens=100)
        assert truncated is False
        assert result == text
