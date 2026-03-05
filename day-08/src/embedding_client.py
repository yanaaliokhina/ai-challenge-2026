import os
from dataclasses import dataclass

import httpx

from constants import VOYAGE_API_URL


@dataclass
class EmbeddingResult:
    """Holds a single text and its embedding vector."""

    text: str
    model: str
    embedding: list[float]


class EmbeddingClient:
    def __init__(self) -> None:
        api_key = os.environ.get("VOYAGE_API_KEY")
        if not api_key:
            raise EnvironmentError("VOYAGE_API_KEY environment variable is not set")
        self._api_key = api_key

    def embed(self, texts: list[str], model: str) -> list[EmbeddingResult]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "content-type": "application/json",
        }
        payload = {
            "model": model,
            "input": texts,
        }
        response = httpx.post(VOYAGE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        results: list[EmbeddingResult] = []
        for item in data["data"]:
            results.append(
                EmbeddingResult(
                    text=texts[item["index"]],
                    model=model,
                    embedding=item["embedding"],
                )
            )
        return results
