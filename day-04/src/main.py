import argparse
import asyncio
import os
import sys
import time

from cli_parser import parse_args, load_prompts
from client import AsyncLLMClient, PromptResult


async def run_prompt(client: AsyncLLMClient, prompt: str) -> PromptResult:
    try:
        text = await client.ask(prompt)
        return PromptResult(prompt=prompt, response=text, success=True)
    except Exception as exc:
        return PromptResult(prompt=prompt, response=str(exc), success=False)


def print_results(results: list, elapsed: float) -> None:
    for i, result in enumerate(results, 1):
        truncated = result.prompt[:60]
        status = "OK" if result.success else "ERROR"
        print(f"[{i}] Prompt: {truncated}")
        print(f"    Status: {status}")
        print(f"    Response: {result.response}")
        print()
    print(f"Total time: {elapsed:.2f}s")


async def run(prompts: list, api_key: str) -> tuple:
    client = AsyncLLMClient(api_key=api_key)
    start = time.perf_counter()
    results = await asyncio.gather(*[run_prompt(client, p) for p in prompts])
    elapsed = time.perf_counter() - start
    return list(results), elapsed


async def main() -> None:
    args = parse_args()
    prompts = load_prompts(args)

    if not prompts:
        print("Error: no prompts provided.", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    results, elapsed = await run(prompts, api_key)
    print_results(results, elapsed)


if __name__ == "__main__":
    asyncio.run(main())
