import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import pydantic
import pytest

from src.client import StructuredLLMClient
from src.models import KeyFacts, SentimentResult


def make_mock_http_client(response_text: str) -> AsyncMock:
    """Return a mock httpx.AsyncClient whose post() returns response_text as LLM content."""
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {"content": [{"type": "text", "text": response_text}]}

    mock_client = AsyncMock()
    mock_client.post.return_value = response
    return mock_client


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    """Inject a dummy API key so tests do not require a real environment variable."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")


def test_ask_returns_valid_sentiment_result():
    """Verifies that ask() parses a valid JSON LLM response into a SentimentResult."""
    json_text = '{"sentiment": "positive", "confidence": 0.9, "reasoning": "Good vibes."}'
    mock_client = make_mock_http_client(json_text)

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        return await client.ask(prompt="How do you feel?", response_model=SentimentResult)

    result = asyncio.run(_run())
    assert isinstance(result, SentimentResult)
    assert result.sentiment == "positive"
    assert result.confidence == 0.9


def test_ask_returns_valid_key_facts():
    """Verifies that ask() parses a valid JSON LLM response into a KeyFacts instance."""
    json_text = '{"facts": ["Fact A.", "Fact B."], "source_topic": "Testing"}'
    mock_client = make_mock_http_client(json_text)

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        return await client.ask(prompt="Extract facts.", response_model=KeyFacts)

    result = asyncio.run(_run())
    assert isinstance(result, KeyFacts)
    assert result.source_topic == "Testing"
    assert len(result.facts) == 2


def test_ask_raises_json_decode_error_for_invalid_json():
    """Verifies that ask() raises json.JSONDecodeError when the LLM response is not valid JSON."""
    mock_client = make_mock_http_client("not valid json")

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        return await client.ask(prompt="test", response_model=SentimentResult)

    with pytest.raises(json.JSONDecodeError):
        asyncio.run(_run())


def test_ask_raises_validation_error_for_schema_mismatch():
    """Verifies that ask() raises pydantic.ValidationError when JSON does not match the model schema."""
    mock_client = make_mock_http_client('{"wrong_field": "bad_value"}')

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        return await client.ask(prompt="test", response_model=SentimentResult)

    with pytest.raises(pydantic.ValidationError):
        asyncio.run(_run())


def test_ask_includes_model_schema_in_system_prompt():
    """Verifies that ask() includes the response_model's JSON schema in the system prompt."""
    json_text = '{"sentiment": "neutral", "confidence": 0.5, "reasoning": "Flat."}'
    mock_client = make_mock_http_client(json_text)

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        await client.ask(prompt="test", response_model=SentimentResult)

    asyncio.run(_run())

    call_kwargs = mock_client.post.call_args
    system_prompt = call_kwargs.kwargs["json"]["system"]
    schema = SentimentResult.model_json_schema()
    assert json.dumps(schema, indent=2) in system_prompt


def test_ask_sends_correct_model_name():
    """Verifies that ask() sends the model name supplied at construction in the API request."""
    json_text = '{"sentiment": "neutral", "confidence": 0.5, "reasoning": "OK."}'
    mock_client = make_mock_http_client(json_text)

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="my-special-model")
        await client.ask(prompt="test", response_model=SentimentResult)

    asyncio.run(_run())

    call_kwargs = mock_client.post.call_args
    assert call_kwargs.kwargs["json"]["model"] == "my-special-model"


def test_ask_sends_prompt_as_user_message_content():
    """Verifies that ask() sends the prompt string as the content of the user message."""
    json_text = '{"sentiment": "positive", "confidence": 0.8, "reasoning": "Happy."}'
    mock_client = make_mock_http_client(json_text)

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        await client.ask(prompt="my specific prompt text", response_model=SentimentResult)

    asyncio.run(_run())

    call_kwargs = mock_client.post.call_args
    messages = call_kwargs.kwargs["json"]["messages"]
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "my specific prompt text"


def test_ask_uses_api_key_from_environment():
    """Verifies that ask() uses the ANTHROPIC_API_KEY environment variable as the x-api-key header."""
    json_text = '{"sentiment": "positive", "confidence": 0.8, "reasoning": "Fine."}'
    mock_client = make_mock_http_client(json_text)

    async def _run():
        client = StructuredLLMClient(http_client=mock_client, model="test-model")
        await client.ask(prompt="test", response_model=SentimentResult)

    asyncio.run(_run())

    call_kwargs = mock_client.post.call_args
    headers = call_kwargs.kwargs["headers"]
    assert headers["x-api-key"] == "test-key"
