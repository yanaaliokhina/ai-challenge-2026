"""Entry point for day-11 project."""

from cli_parser import CLIParser
from llm_client import LLMClient
from parser import parse_file
from prompt import build_prompt
from token_budget import apply_budget, estimate_tokens

if __name__ == "__main__":
    args = CLIParser().parse_args()

    document = parse_file(args.file)
    estimated = estimate_tokens(document)
    document, truncated = apply_budget(document, args.max_tokens)

    if args.verbose:
        print(f"Estimated tokens: {estimated}")
        print(f"Truncated: {'yes' if truncated else 'no'}")
        print()

    prompt = build_prompt(document, args.query)
    client = LLMClient()
    answer = client.ask(prompt)
    print(answer)
