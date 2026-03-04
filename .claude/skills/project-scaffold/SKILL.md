---
name: project-scaffold
description: "ALWAYS use this skill when implementing any new day challenge — no exceptions. Triggers on: user asks to scaffold a day project, create a day-N folder, or /implement-challenge is invoked for any challenge."
---

# Python Project Scaffold

Generates a four-file structured Python project inside `day-{N}/src/` for this ai-challenge-2026 repo.

## When This Skill Applies

Use this skill for **every new challenge implementation** — no exceptions:
- `/implement-challenge` is invoked (any challenge, any day)
- User asks to scaffold or create a `day-{N}/` project
- A new `day-{N}/src/` directory needs to be created

## Steps

1. Identify the day number N. If not provided, ask for it.
2. Create `day-{N}/src/` if it does not exist.
3. Review instructions for the implemented challenge and write the files below if they are needed.

---

## Files to Generate

### `day-{N}/src/constants.py`

```python
"""Constants for day-{N} project."""

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
```

### `day-{N}/src/cli_parser.py`

```python
"""CLI argument parser for day-{N} project."""

import argparse
from constants import DEFAULT_MODEL


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(description="day-{N} LLM CLI")
        parser.add_argument("--prompt", required=True, help="Prompt to send to the LLM")
        parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
        parser.add_argument("--verbose", action="store_true", help="Print debug info")
        return parser.parse_args()
```

### `day-{N}/src/llm_client.py`

```python
"""LLM client for Anthropic API — day-{N} project."""

import os
import httpx
from constants import ANTHROPIC_API_URL, ANTHROPIC_API_VERSION, DEFAULT_MODEL, MAX_TOKENS


class LLMClient:
    def __init__(self):
        self._api_key = os.environ["ANTHROPIC_API_KEY"]

    def ask(self, prompt: str) -> str:
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": ANTHROPIC_API_VERSION,
            "content-type": "application/json",
        }
        payload = {
            "model": DEFAULT_MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = httpx.post(ANTHROPIC_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
```

### `day-{N}/src/main.py`

```python
"""Entry point for day-{N} project."""

from cli_parser import CLIParser
from llm_client import LLMClient

if __name__ == "__main__":
    args = CLIParser().parse_args()

    if args.verbose:
        print(f"[verbose] prompt: {args.prompt}")

    client = LLMClient()
    response = client.ask(args.prompt)

    if args.verbose:
        print("[verbose] response received")

    print(response)
```

---

## Rules

### Constants ownership (CRITICAL)
- `constants.py` is the ONLY file allowed to define module-level static values
- `llm_client.py` MUST NOT define any module-level constants — not `DEFAULT_MODEL`, not `_API_URL`, not `MAX_TOKENS`, nothing
- `cli_parser.py` MUST import `DEFAULT_MODEL` from `constants`, NEVER from `llm_client`
- Any new static value added during challenge extension (e.g. a temperature, a timeout) goes into `constants.py` first

### Forbidden anti-patterns
```python
# WRONG — constant defined in llm_client.py
DEFAULT_MODEL = "claude-haiku-4-5-20251001"  # belongs in constants.py

# WRONG — cli_parser importing from llm_client
from llm_client import DEFAULT_MODEL  # must import from constants instead

# WRONG — hardcoded literal in llm_client.py body
"max_tokens": 1024          # use MAX_TOKENS from constants
"anthropic-version": "2023-06-01"  # use ANTHROPIC_API_VERSION from constants
```

### Other rules
- Use `httpx` (not `requests`) — mandated by project tech stack
- API key via `os.environ["ANTHROPIC_API_KEY"]` only — never in source
- Every file must have a module-level docstring
- Do not add extra files, dependencies, or comments beyond docstrings

## After Writing Files

Print this usage example (with actual N substituted):

```
ANTHROPIC_API_KEY=sk-... python day-{N}/src/main.py --prompt "Hello, Claude!" --verbose
```
