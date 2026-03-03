"""Entry point for day-05 CLI AI Assistant."""

import sys
from typing import Optional

from cli_parser import parse_args
from llm_client import LLMClient


def _print_verbose(model: str, system: Optional[str], prompt: str) -> None:
    """Write request metadata to stderr."""
    print(f"[verbose] Model: {model}", file=sys.stderr)
    print(f"[verbose] System: {system or '(none)'}", file=sys.stderr)
    print(f"[verbose] Prompt: {prompt}", file=sys.stderr)


def run_single_shot(args, client: LLMClient) -> None:
    """Send a single prompt and print the response."""
    if args.verbose:
        _print_verbose(args.model, args.system, args.prompt)
    response = client.ask(args.prompt, system=args.system, model=args.model)
    print(response)


def run_interactive(args, client: LLMClient) -> None:
    """Run a REPL loop until the user exits."""
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.strip().lower() in ("exit", "quit"):
            break
        if not user_input.strip():
            continue
        if args.verbose:
            _print_verbose(args.model, args.system, user_input)
        try:
            response = client.ask(user_input, system=args.system, model=args.model)
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            continue
        print(f"Assistant: {response}")


def main() -> None:
    """Parse args, wire components, and dispatch to the correct mode."""
    args = parse_args()
    client = LLMClient()
    if args.interactive:
        run_interactive(args, client)
    else:
        run_single_shot(args, client)


if __name__ == "__main__":
    main()
