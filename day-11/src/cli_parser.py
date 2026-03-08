"""CLI argument parser for day-11 project."""

import argparse

from constants import DEFAULT_MAX_DOC_TOKENS, DEFAULT_MODEL


class CLIParser:
    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Local Document Q&A CLI")
        parser.add_argument("--file", required=True, help="Path to the input document (.txt or .md)")
        parser.add_argument("--query", required=True, help="Question to answer about the document")
        parser.add_argument(
            "--max-tokens",
            type=int,
            default=DEFAULT_MAX_DOC_TOKENS,
            help=f"Maximum token budget for document content (default: {DEFAULT_MAX_DOC_TOKENS})",
        )
        parser.add_argument("--verbose", action="store_true", help="Print token count and truncation status")
        return parser.parse_args()
