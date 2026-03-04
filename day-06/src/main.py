import sys
from cli_parser import CLIParser
from constants import SUPPORTED_MODELS
from counter import count_tokens, get_token_strings


def print_single_result(
    source: str,
    model: str,
    token_count: int,
    verbose: bool,
    token_strings: list[str],
) -> None:
    context_window = SUPPORTED_MODELS[model]["context_window"]
    usage_pct = round(token_count / context_window * 100, 2)
    status = "FITS" if token_count <= context_window else "EXCEEDS"

    print(f"Source:         {source}")
    print(f"Model:          {model}")
    print(f"Tokens:         {token_count}")
    print(f"Context window: {context_window}")
    print(f"Usage:          {usage_pct}%")
    print(f"Status:         {status}")

    if verbose:
        remaining = context_window - token_count
        print(f"Tokens (decoded): {token_strings}")
        print(f"Remaining budget: {remaining} tokens")


def run_batch_mode(batch_file: str, model: str) -> None:
    try:
        with open(batch_file, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: File not found: {batch_file}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print("Warning: batch file is empty.")
        sys.exit(0)

    context_window = SUPPORTED_MODELS[model]["context_window"]
    counts: list[int] = []

    for i, line in enumerate(lines, 1):
        token_count = count_tokens(line, model)
        counts.append(token_count)
        status = "FITS" if token_count <= context_window else "EXCEEDS"
        print(f"Line {i}: {token_count} tokens [{status}]")

    total = sum(counts)
    min_c = min(counts)
    max_c = max(counts)
    avg_c = round(total / len(counts), 2)

    print("---")
    print("Summary:")
    print(f"  Total lines:   {len(counts)}")
    print(f"  Total tokens:  {total}")
    print(f"  Min tokens:    {min_c}")
    print(f"  Max tokens:    {max_c}")
    print(f"  Avg tokens:    {avg_c}")


def main() -> None:
    args = CLIParser().parse_args()

    if args.model not in SUPPORTED_MODELS:
        supported = ", ".join(SUPPORTED_MODELS.keys())
        print(f"Error: Unsupported model '{args.model}'.\nSupported models: {supported}", file=sys.stderr)
        sys.exit(1)

    if args.batch:
        run_batch_mode(args.batch, args.model)
        return

    if args.text is not None and args.file is not None:
        print("Error: Provide either --text or --file, not both.", file=sys.stderr)
        sys.exit(1)

    if args.text is not None:
        text = args.text
        source = "argument"
    elif args.file is not None:
        try:
            with open(args.file, "r") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        source = "file"
    else:
        text = sys.stdin.read()
        source = "stdin"

    token_count = count_tokens(text, args.model)
    token_strings = get_token_strings(text, args.model) if args.verbose else []
    print_single_result(source, args.model, token_count, args.verbose, token_strings)


if __name__ == "__main__":
    main()
