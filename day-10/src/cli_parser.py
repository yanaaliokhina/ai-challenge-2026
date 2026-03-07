import argparse
from constants import DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP, DEFAULT_TOP_K


class CLIParser:

    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Mini RAG Script — answer questions from a text document")
        parser.add_argument("--file", required=True, help="Path to the input .txt document")
        parser.add_argument("--query", required=True, help="Question to answer from the document")
        parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help=f"Number of chunks to retrieve (default: {DEFAULT_TOP_K})")
        parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help=f"Words per chunk (default: {DEFAULT_CHUNK_SIZE})")
        parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP, help=f"Overlapping words between chunks (default: {DEFAULT_OVERLAP})")
        parser.add_argument("--verbose", action="store_true", help="Print retrieved chunks and similarity scores")
        return parser.parse_args()
