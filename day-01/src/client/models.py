from dataclasses import dataclass

@dataclass
class LLMRequest:
    model: str
    prompt: str
    max_tokens: int
    temperature: float


@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int