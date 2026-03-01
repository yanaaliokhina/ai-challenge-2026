from typing import Literal

from pydantic import BaseModel, Field


class SentimentResult(BaseModel):
    """Structured result for sentiment analysis."""

    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)


class KeyFacts(BaseModel):
    """Structured result for key fact extraction."""

    facts: list[str] = Field(min_length=1)
    source_topic: str = Field(min_length=1)
