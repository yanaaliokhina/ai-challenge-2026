import os
from typing import Optional
import httpx
from constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION, DEFAULT_MODEL, MAX_TOKENS


class LLMClient:
    def __init__(self) -> None:
        self._api_key = os.environ["ANTHROPIC_API_KEY"]

    def chat(self, messages: list[dict[str, str]], system: Optional[str] = None) -> str:
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": ANTHROPIC_API_VERSION,
            "content-type": "application/json",
        }
        payload: dict[str, object] = {
            "model": DEFAULT_MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": messages,
        }
        if system:
            payload["system"] = system
        response = httpx.post(ANTHROPIC_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
