import sys

from cli_parser import parse_args

from constants import MAX_TEXT_DISPLAY_LENGTH
from embedding_client import EmbeddingClient
from similarity import rank_candidates
from candidates_loader import load_candidates

def print_results(results: list) -> None:
    header = f"{'Rank':<6} {'Score':<8} {'Text'}"
    print(header)
    print("-" * (6 + 8 + MAX_TEXT_DISPLAY_LENGTH + 2))
    for r in results:
        truncated = r.text[:MAX_TEXT_DISPLAY_LENGTH] if len(r.text) > MAX_TEXT_DISPLAY_LENGTH else r.text
        print(f"{r.rank:<6} {r.score:<8.4f} {truncated}")


def main() -> None:
    args = parse_args()

    try:
        candidates = load_candidates(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        client = EmbeddingClient()
    except EnvironmentError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    all_texts = [args.query] + candidates
    try:
        embeddings = client.embed(all_texts, model=args.model)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    query_embedding = embeddings[0]
    candidates_map = dict(zip(candidates, embeddings[1:]))

    results = rank_candidates(query_embedding, candidates_map)
    print_results(results)


if __name__ == "__main__":
    main()
