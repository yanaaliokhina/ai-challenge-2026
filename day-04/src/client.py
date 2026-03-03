"""Async LLM client for the Anthropic Messages API."""

import httpx
from dataclasses import dataclass

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_TOKENS = 256


@dataclass
class PromptResult:
    prompt: str
    response: str
    success: bool


class AsyncLLMClient:

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS):
        self._api_key = api_key
        self._model = model
        self._max_tokens = max_tokens

    async def ask(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            headers = {
                "x-api-key": self._api_key,
                "anthropic-version": API_VERSION,
                "content-type": "application/json",
            }
            payload = {
                "model": self._model,
                "max_tokens": self._max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            response = await client.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["content"][0]["text"]