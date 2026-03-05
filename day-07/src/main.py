"""Entry point for day-07 project — prompt experiment script."""

import json

from cli_parser import CLIParser
from llm_client import LLMClient
from prompt_loader import load_prompts


def run() -> None:
    args = CLIParser().parse_args()
    prompts = load_prompts(args.prompts_file)
    client = LLMClient(model=args.model)

    results = []
    for entry in prompts:
        result: dict = {
            "id": entry["id"],
            "label": entry.get("label"),
            "prompt": entry["prompt"],
            "response": None,
            "latency_ms": 0.0,
            "error": None,
        }
        try:
            response_text, latency_ms = client.ask(entry["prompt"])
            result["response"] = response_text
            result["latency_ms"] = latency_ms
        except Exception as e:
            result["error"] = str(e)

        results.append(result)

    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    successes = [r for r in results if r["error"] is None]
    failures = [r for r in results if r["error"] is not None]
    avg_latency = (
        sum(r["latency_ms"] for r in successes) / len(successes) if successes else 0.0
    )

    print(f"Total prompts attempted: {len(results)}")
    print(f"Successful responses:    {len(successes)}")
    print(f"Failures:                {len(failures)}")
    print(f"Average latency (ms):    {avg_latency:.1f}")


if __name__ == "__main__":
    run()
