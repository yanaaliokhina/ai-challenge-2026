import os
import httpx
from constants import VOYAGE_API_URL, VOYAGE_EMBEDDING_MODEL


class EmbeddingClient:
    def __init__(self):
        self._api_key = os.environ["VOYAGE_API_KEY"]

    def embed(self, text: str) -> list[float]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "content-type": "application/json",
        }
        payload = {
            "model": VOYAGE_EMBEDDING_MODEL,
            "input": [text],
        }
        response = httpx.post(VOYAGE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
