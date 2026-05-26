"""Constants for day-16 project."""

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024

TOOL_SELECTION_PROMPT = """You are a tool-calling assistant. Given a user prompt and a list of available tools, respond with a JSON object selecting the best tool to use.

Available tools:
{tools_json}

User prompt: {user_prompt}

Respond ONLY with a JSON object in this exact format:
{{
  "tool_name": "<name of the tool to call>",
  "arguments": {{<argument key-value pairs>}}
}}

Select the most appropriate tool and provide all required arguments."""
