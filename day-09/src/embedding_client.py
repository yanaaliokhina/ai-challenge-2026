import os
import httpx
from constants import VOYAGE_API_URL


class EmbeddingClient:
    def __init__(self) -> None:
        api_key = os.environ.get("VOYAGE_API_KEY")
        if not api_key:
            raise EnvironmentError("VOYAGE_API_KEY environment variable is not set")
        self._api_key = api_key

    def embed(self, texts: list[str], model: str) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {"input": texts, "model": model}

        response = httpx.post(VOYAGE_API_URL, headers=headers, json=payload)

        if not response.is_success:
            raise RuntimeError(
                f"Voyage AI API error {response.status_code}: {response.text}"
            )

        data = response.json().get("data", [])
        if len(data) != len(texts):
            raise RuntimeError(
                f"Expected {len(texts)} embeddings, got {len(data)}"
            )

        embeddings: list[list[float]] = []
        for i, item in enumerate(data):
            vec = item.get("embedding")
            if not vec:
                raise RuntimeError(f"Embedding at index {i} is empty or malformed")
            embeddings.append(vec)

        return embeddings
