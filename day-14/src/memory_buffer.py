from typing import Optional


class MemoryBuffer:
    """Maintains a rolling list of conversation messages with a configurable turn limit."""

    def __init__(self, max_turns: int, system_prompt: Optional[str] = None) -> None:
        self._max_turns = max_turns
        self._system_prompt = system_prompt
        self._messages: list[dict[str, str]] = []

    def append(self, role: str, content: str) -> None:
        """Append a message and trim the buffer to the turn limit."""
        self._messages.append({"role": role, "content": content})
        self._trim()

    def _trim(self) -> None:
        """Drop the oldest user+assistant pair when complete pairs exceed the turn limit."""
        while len(self._messages) // 2 > self._max_turns:
            self._messages.pop(0)
            self._messages.pop(0)

    def clear(self) -> None:
        """Reset the conversation buffer."""
        self._messages = []

    def get_messages(self) -> list[dict[str, str]]:
        """Return a copy of the current message buffer."""
        return list(self._messages)

    @property
    def system_prompt(self) -> Optional[str]:
        """Return the system prompt if set."""
        return self._system_prompt
