from typing import Union

from models import KeyFacts, SentimentResult

TASK_MAP: dict[str, type[Union[SentimentResult, KeyFacts]]] = {
    "sentiment": SentimentResult,
    "facts": KeyFacts,
}

MODEL = "claude-haiku-4-5-20251001"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION = "2023-06-01"
