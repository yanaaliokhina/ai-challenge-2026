import pytest
from pydantic import ValidationError

from src.models import KeyFacts, SentimentResult


def test_sentiment_result_valid_positive():
    """Verifies that SentimentResult accepts a valid positive sentiment input."""
    result = SentimentResult(sentiment="positive", confidence=0.9, reasoning="Strong positive tone.")
    assert result.sentiment == "positive"
    assert result.confidence == 0.9


def test_sentiment_result_valid_negative():
    """Verifies that SentimentResult accepts a valid negative sentiment input."""
    result = SentimentResult(sentiment="negative", confidence=0.7, reasoning="Negative language used.")
    assert result.sentiment == "negative"


def test_sentiment_result_valid_neutral():
    """Verifies that SentimentResult accepts a valid neutral sentiment input."""
    result = SentimentResult(sentiment="neutral", confidence=0.5, reasoning="No clear tone.")
    assert result.sentiment == "neutral"


def test_sentiment_result_invalid_sentiment_value():
    """Verifies that SentimentResult rejects a sentiment value outside the allowed Literal."""
    with pytest.raises(ValidationError):
        SentimentResult(sentiment="happy", confidence=0.8, reasoning="Not in Literal.")


def test_sentiment_result_confidence_below_zero():
    """Verifies that SentimentResult rejects a confidence value below 0.0."""
    with pytest.raises(ValidationError):
        SentimentResult(sentiment="positive", confidence=-0.1, reasoning="Below range.")


def test_sentiment_result_confidence_above_one():
    """Verifies that SentimentResult rejects a confidence value above 1.0."""
    with pytest.raises(ValidationError):
        SentimentResult(sentiment="positive", confidence=1.1, reasoning="Above range.")


def test_sentiment_result_confidence_at_boundary_zero():
    """Verifies that SentimentResult accepts confidence exactly at 0.0."""
    result = SentimentResult(sentiment="negative", confidence=0.0, reasoning="Boundary low.")
    assert result.confidence == 0.0


def test_sentiment_result_confidence_at_boundary_one():
    """Verifies that SentimentResult accepts confidence exactly at 1.0."""
    result = SentimentResult(sentiment="positive", confidence=1.0, reasoning="Boundary high.")
    assert result.confidence == 1.0


def test_sentiment_result_empty_reasoning_rejected():
    """Verifies that SentimentResult rejects an empty reasoning string."""
    with pytest.raises(ValidationError):
        SentimentResult(sentiment="positive", confidence=0.8, reasoning="")


def test_key_facts_valid():
    """Verifies that KeyFacts accepts a valid list of facts and a source_topic."""
    result = KeyFacts(facts=["Fact one.", "Fact two."], source_topic="Testing")
    assert len(result.facts) == 2
    assert result.source_topic == "Testing"


def test_key_facts_single_fact_accepted():
    """Verifies that KeyFacts accepts a list with exactly one fact."""
    result = KeyFacts(facts=["Only fact."], source_topic="Topic")
    assert result.facts == ["Only fact."]


def test_key_facts_empty_facts_list_rejected():
    """Verifies that KeyFacts rejects an empty facts list."""
    with pytest.raises(ValidationError):
        KeyFacts(facts=[], source_topic="Topic")


def test_key_facts_empty_source_topic_rejected():
    """Verifies that KeyFacts rejects an empty source_topic string."""
    with pytest.raises(ValidationError):
        KeyFacts(facts=["Some fact."], source_topic="")


def test_key_facts_missing_facts_field_rejected():
    """Verifies that KeyFacts raises ValidationError when facts field is absent."""
    with pytest.raises(ValidationError):
        KeyFacts(source_topic="Topic")


def test_sentiment_result_missing_required_field_rejected():
    """Verifies that SentimentResult raises ValidationError when a required field is absent."""
    with pytest.raises(ValidationError):
        SentimentResult(sentiment="positive", confidence=0.9)
