import argparse

from constants import DEFAULT_MODEL

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank candidate texts by cosine similarity to a query using Voyage AI embeddings"
    )
    parser.add_argument("--query", required=True, help="Query text to compare against candidates")
    parser.add_argument("--file", required=True, help="Path to newline-separated candidate texts file")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Voyage AI embedding model (default: {DEFAULT_MODEL})",
    )
    return parser.parse_args()