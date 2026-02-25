import os

import httpx

from .models import LLMRequest, LLMResponse
from .constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION

def send_request(request: LLMRequest) -> LLMResponse:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is missing or empty.")

    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_API_VERSION,
        "content-type": "application/json",
    }

    payload = {
        "model": request.model,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "messages": [{"role": "user", "content": request.prompt}],
    }

    try:
        response = httpx.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=60.0)
    except httpx.RequestError as exc:
        raise RuntimeError(f"Network error while calling Anthropic API: {exc}") from exc

    if response.status_code >= 400:
        raise RuntimeError(
            f"Anthropic API returned HTTP {response.status_code}: {response.text}"
        )

    data = response.json()
    content = data["content"][0]["text"]
    usage = data["usage"]

    return LLMResponse(
        content=content,
        model=data["model"],
        input_tokens=usage["input_tokens"],
        output_tokens=usage["output_tokens"],
    )
