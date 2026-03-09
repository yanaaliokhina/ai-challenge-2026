import argparse
from constants import DEFAULT_CHUNK_SIZE, DEFAULT_TOP_N, DEFAULT_INDEX_PATH


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Embedding Index Storage CLI")
        parser.add_argument("--file", help="Path to a text file to index")
        parser.add_argument("--query", help="Query string to search the index")
        parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N, help=f"Number of top results (default: {DEFAULT_TOP_N})")
        parser.add_argument("--index", default=DEFAULT_INDEX_PATH, help=f"Path to the JSON index file (default: {DEFAULT_INDEX_PATH})")
        parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help=f"Chunk size in characters (default: {DEFAULT_CHUNK_SIZE})")
        return parser.parse_args()
