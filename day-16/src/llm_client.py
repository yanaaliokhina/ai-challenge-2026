"""LLM client for Anthropic API — day-16 project."""

import os
import httpx
from constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION, DEFAULT_MODEL, MAX_TOKENS


class LLMClient:
    def __init__(self):
        self._api_key = os.environ["ANTHROPIC_API_KEY"]

    def ask(self, prompt: str) -> str:
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": ANTHROPIC_API_VERSION,
            "content-type": "application/json",
        }
        payload = {
            "model": DEFAULT_MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = httpx.post(ANTHROPIC_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
