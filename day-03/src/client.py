import json
import os
from typing import TypeVar

import httpx
from pydantic import BaseModel

from constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION

T = TypeVar("T", bound=BaseModel)

class StructuredLLMClient:
    def __init__(self, http_client: httpx.AsyncClient, model: str) -> None:
        self._http_client = http_client
        self._model = model

    async def ask(self, prompt: str, response_model: type[T]) -> T:
        schema = response_model.model_json_schema()
        response = await self._http_client.post(
            ANTHROPIC_API_URL,
            headers={
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": ANTHROPIC_API_VERSION,
                "content-type": "application/json",
            },
            json={
                "model": self._model,
                "max_tokens": 1024,
                "system": (
                    "You must respond with valid JSON only. "
                    "No explanations, no markdown, no code blocks. "
                    f"The JSON must exactly match this schema:\n{json.dumps(schema, indent=2)}"
                ),
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        response.raise_for_status()

        data = response.json()
        text = data["content"][0]["text"]

        parsed = json.loads(text)
        return response_model.model_validate(parsed)
