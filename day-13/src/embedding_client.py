import os
import httpx
from constants import OPENAI_API_URL, DEFAULT_EMBEDDING_MODEL


class EmbeddingClient:
    def __init__(self):
        self._api_key = os.environ["OPENAI_API_KEY"]

    def embed(self, text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "input": text,
        }
        response = httpx.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
