import argparse
from constants import DEFAULT_MAX_TURNS, DEFAULT_MODEL


class CLIParser:

    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Multi-turn chat with memory buffer")
        parser.add_argument("--system", default=None, help="System prompt to set assistant persona")
        parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS, help=f"Max conversation turns to keep in memory (default: {DEFAULT_MAX_TURNS})")
        parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
        return parser.parse_args()
