"""Tests for constants.py — verifies all required constants are defined and non-empty."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import constants


def test_anthropic_api_url_is_defined():
    """ANTHROPIC_API_URL is a non-empty string pointing to the messages endpoint."""
    assert isinstance(constants.ANTHROPIC_API_URL, str)
    assert constants.ANTHROPIC_API_URL.startswith("https://")
    assert "messages" in constants.ANTHROPIC_API_URL


def test_anthropic_api_version_is_defined():
    """ANTHROPIC_API_VERSION is a non-empty string."""
    assert isinstance(constants.ANTHROPIC_API_VERSION, str)
    assert len(constants.ANTHROPIC_API_VERSION) > 0


def test_default_model_is_defined():
    """DEFAULT_MODEL is a non-empty string."""
    assert isinstance(constants.DEFAULT_MODEL, str)
    assert len(constants.DEFAULT_MODEL) > 0


def test_max_tokens_is_positive_int():
    """MAX_TOKENS is a positive integer."""
    assert isinstance(constants.MAX_TOKENS, int)
    assert constants.MAX_TOKENS > 0
