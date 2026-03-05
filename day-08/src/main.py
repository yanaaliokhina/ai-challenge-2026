import json
import sys
from pathlib import Path

from cli_parser import CLIParser
from constants import EMBEDDING_PREVIEW_COUNT
from embedding_client import EmbeddingClient, EmbeddingResult


def load_texts_from_file(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"file '{path}' not found")
    lines = [line.strip() for line in p.read_text().splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"file '{path}' is empty")
    return lines


def print_summary(results: list[EmbeddingResult]) -> None:
    if not results:
        return
    dim = len(results[0].embedding)
    print(f"Inputs processed : {len(results)}")
    print(f"Model            : {results[0].model}")
    print(f"Embedding dim    : {dim}")
    for i, result in enumerate(results):
        preview = result.embedding[:EMBEDDING_PREVIEW_COUNT]
        formatted = ", ".join(f"{v:.4f}" for v in preview)
        print(f"[{i}] preview      : [{formatted}, ...]")


def save_results(results: list[EmbeddingResult], path: str) -> None:
    data = [{"text": r.text, "model": r.model, "embedding": r.embedding} for r in results]
    Path(path).write_text(json.dumps(data, indent=2))
    print(f"Results saved to {path}")


if __name__ == "__main__":
    try:
        args = CLIParser().parse_args()

        if args.file:
            texts = load_texts_from_file(args.file)
        else:
            texts = [args.text]

        client = EmbeddingClient()
        results = client.embed(texts, args.model)

        print_summary(results)

        if args.output:
            save_results(results, args.output)

    except (FileNotFoundError, ValueError, EnvironmentError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
