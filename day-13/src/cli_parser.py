import argparse
from constants import DEFAULT_EMBEDDING_MODEL, DEFAULT_TOP_N


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Vector search CLI — query a stored embedding index")
        parser.add_argument("--index", required=True, help="Path to the JSON index file")
        parser.add_argument("--query", required=True, help="Natural language search query")
        parser.add_argument("--top", type=int, default=DEFAULT_TOP_N, help=f"Number of top results to return (default: {DEFAULT_TOP_N})")
        parser.add_argument("--model", default=DEFAULT_EMBEDDING_MODEL, help=f"Embedding model name (default: {DEFAULT_EMBEDDING_MODEL})")
        return parser.parse_args()
