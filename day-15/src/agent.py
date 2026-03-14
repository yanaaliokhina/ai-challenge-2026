"""Agent loop with structured LLM response parsing for day-15 project."""

import json
from typing import Optional
from pydantic import BaseModel, model_validator
from llm_client import LLMClient
from tools import TOOL_REGISTRY
from constants import AGENT_SYSTEM_PROMPT

class ToolCall(BaseModel):
    name: str
    argument: str


class AgentResponse(BaseModel):
    tool_call: Optional[ToolCall] = None
    final_answer: Optional[str] = None

    @model_validator(mode="after")
    def exactly_one_field(self) -> "AgentResponse":
        if self.tool_call is None and self.final_answer is None:
            raise ValueError("Response must have either tool_call or final_answer")
        if self.tool_call is not None and self.final_answer is not None:
            raise ValueError("Response must have either tool_call or final_answer, not both")
        return self

def build_prompt(task: str, history: list[str]) -> str:
    """Builds the full prompt for the current agent iteration."""
    parts = [AGENT_SYSTEM_PROMPT, f"\nTask: {task}"]
    if history:
        parts.append("\nHistory:")
        parts.extend(history)
    parts.append("\nNext step:")
    return "\n".join(parts)


def parse_response(raw: str) -> AgentResponse:
    """Parses raw LLM text into an AgentResponse Pydantic model."""
    raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON found in response: {raw!r}")
    return AgentResponse.model_validate(json.loads(raw[start:end]))


def run_agent(task: str, max_iterations: int, client: LLMClient, model: str) -> None:
    """Runs the agent reasoning loop for the given task."""
    history: list[str] = []

    for i in range(1, max_iterations + 1):
        prompt = build_prompt(task, history)
        raw = client.ask(prompt, model=model)

        try:
            response = parse_response(raw)
            print  (f"[Step {i}] Parsed response: {response} {history}")
        except Exception as e:
            print(f"[Step {i}] Parse error: {e}")
            history.append(f"Step {i} — Parse error: {e}")
            continue

        if response.final_answer is not None:
            print(f"[Step {i}] Final answer: {response.final_answer}")
            return

        tool_call = response.tool_call
        print(f"[Step {i}] Tool call: {tool_call.name}({tool_call.argument!r})")

        if tool_call.name not in TOOL_REGISTRY:
            observation = f"Error: unknown tool '{tool_call.name}'"
        else:
            try:
                observation = TOOL_REGISTRY[tool_call.name](tool_call.argument)
            except Exception as e:
                observation = f"Error: {e}"

        print(f"[Step {i}] Observation: {observation}")
        history.append(f"Step {i} — Called {tool_call.name}({tool_call.argument!r}) → {observation}")

    print("Max iterations reached. No final answer produced.")
