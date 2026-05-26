"""Entry point for day-16 Tool Registry project."""

import json
import logging

import tools  # noqa: F401 — registers all demo tools as a side effect
from cli_parser import CLIParser
from constants import TOOL_SELECTION_PROMPT
from llm_client import LLMClient
from tool_registry import call_tool, list_tools

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def select_and_run_tool(prompt: str, client: LLMClient) -> tuple[str, dict, str]:
    """Ask the LLM to pick a tool, dispatch it, and return (tool_name, args, result)."""
    available = list_tools()
    tools_json = json.dumps(available, indent=2)
    llm_prompt = TOOL_SELECTION_PROMPT.format(tools_json=tools_json, user_prompt=prompt)

    raw_response = client.ask(llm_prompt)

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned non-JSON response: {raw_response!r}") from exc

    tool_name = parsed.get("tool_name")
    arguments = parsed.get("arguments", {})

    if not tool_name:
        raise ValueError("LLM response missing 'tool_name' field.")

    result = call_tool(tool_name, arguments)
    return tool_name, arguments, result


if __name__ == "__main__":
    args = CLIParser().parse_args()

    if args.verbose:
        logger.info("Prompt: %s", args.prompt)

    client = LLMClient()
    tool_name, arguments, result = select_and_run_tool(args.prompt, client)

    print(f"Tool:      {tool_name}")
    print(f"Arguments: {json.dumps(arguments)}")
    print(f"Result:    {result}")
