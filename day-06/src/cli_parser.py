import argparse
from constants import DEFAULT_COUNTER_MODEL


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Token Counter Utility")
        parser.add_argument("--text", help="Inline text to count tokens for")
        parser.add_argument("--file", help="Path to a .txt or .md file to count tokens for")
        parser.add_argument("--batch", help="Path to a .txt file with one text per line (batch mode)")
        parser.add_argument(
            "--model",
            default=DEFAULT_COUNTER_MODEL,
            help=f"Model to use for tokenization (default: {DEFAULT_COUNTER_MODEL})",
        )
        parser.add_argument("--verbose", action="store_true", help="Show individual tokens and remaining budget")
        return parser.parse_args()
