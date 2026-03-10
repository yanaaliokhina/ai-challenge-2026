"""Entry point for day-13 project."""

import sys
from cli_parser import CLIParser
from embedding_client import EmbeddingClient
from index_loader import load_index
from searcher import search


def run():
    args = CLIParser().parse_args()

    if not args.query.strip():
        print("Error: Query must not be empty")
        sys.exit(1)

    entries = load_index(args.index)

    try:
        client = EmbeddingClient()
        query_vector = client.embed(args.query, model=args.model)
    except Exception as e:
        print(f"Error: Embedding API failed: {e}")
        sys.exit(1)

    results = search(query_vector, entries, top_n=args.top)

    print(f'Query: "{args.query}"')
    print(f"Index: {args.index} ({len(entries)} entries)")
    print()

    if not results:
        print("No results found.")
        sys.exit(0)

    print("Results:")
    for result in results:
        print(f"{result.rank}. [score: {result.score}] id={result.id}")
        print(f"   {result.text}")
        print()


if __name__ == "__main__":
    run()
