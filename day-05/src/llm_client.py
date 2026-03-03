"""LLM client for Anthropic API — day-05 project."""

import os
from typing import Optional

import httpx

from constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION, DEFAULT_MODEL, MAX_TOKENS


class LLMClient:
    """Synchronous client for the Anthropic messages API."""

    def __init__(self) -> None:
        """Read API key from environment; raise RuntimeError if absent."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
        self._api_key = api_key

    def ask(self, prompt: str, system: Optional[str] = None, model: Optional[str] = None) -> str:
        """Send a single prompt and return the assistant's text response."""
        resolved_model = model or DEFAULT_MODEL
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": ANTHROPIC_API_VERSION,
            "content-type": "application/json",
        }
        body: dict = {
            "model": resolved_model,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system

        response = httpx.post(ANTHROPIC_API_URL, headers=headers, json=body)
        if response.status_code != 200:
            raise RuntimeError(f"API error {response.status_code}: {response.text}")

        data = response.json()
        return data["content"][0]["text"]
