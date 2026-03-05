import argparse
from constants import DEFAULT_MODEL


class CLIParser:
    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Generate text embeddings via Voyage AI")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--text", help="Single text string to embed")
        group.add_argument("--file", help="Path to file with newline-separated texts")
        parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Embedding model (default: {DEFAULT_MODEL})")
        parser.add_argument("--output", help="Path to save full results as JSON")
        return parser.parse_args()
