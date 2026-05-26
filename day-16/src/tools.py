"""Built-in demo tools for day-16 project."""

from datetime import datetime
from tool_registry import tool


@tool(
    description="Returns the current date and time.",
    parameters=[],
)
def get_current_datetime() -> str:
    """Return the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool(
    description="Counts the number of words in a given text.",
    parameters=[
        {"name": "text", "type": "string", "description": "The text to count words in."},
    ],
)
def word_count(text: str) -> int:
    """Return the number of words in the provided text."""
    return len(text.split())


@tool(
    description="Converts a temperature from Celsius to Fahrenheit.",
    parameters=[
        {"name": "celsius", "type": "number", "description": "Temperature in Celsius."},
    ],
)
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius value to Fahrenheit."""
    return celsius * 9 / 5 + 32
