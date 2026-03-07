import os
import httpx
from constants import OPENAI_EMBEDDING_URL, EMBEDDING_MODEL


class EmbeddingClient:
    def __init__(self) -> None:
        self._api_key = os.environ["OPENAI_API_KEY"]

    def embed(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": EMBEDDING_MODEL,
            "input": texts,
        }
        response = httpx.post(OPENAI_EMBEDDING_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()["data"]
        data.sort(key=lambda item: item["index"])
        return [item["embedding"] for item in data]
