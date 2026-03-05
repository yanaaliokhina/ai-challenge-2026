import os
import time

import httpx

from constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION, MAX_TOKENS


class LLMClient:
    def __init__(self, model: str):
        self._api_key = os.environ["ANTHROPIC_API_KEY"]
        self._model = model

    def ask(self, prompt: str) -> tuple[str, float]:
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": ANTHROPIC_API_VERSION,
            "content-type": "application/json",
        }
        payload = {
            "model": self._model,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
        start = time.time()
        response = httpx.post(ANTHROPIC_API_URL, headers=headers, json=payload)
        latency_ms = (time.time() - start) * 1000
        response.raise_for_status()
        return response.json()["content"][0]["text"], latency_ms
