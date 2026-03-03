"""CLI argument parser for day-05 project."""

import argparse
from typing import List, Optional

from constants import DEFAULT_MODEL


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="CLI AI Assistant powered by Claude",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--prompt",
        type=str,
        metavar="TEXT",
        help="Single prompt to send to the LLM (single-shot mode)",
    )
    mode_group.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Launch an interactive REPL session",
    )
    parser.add_argument(
        "--system",
        type=str,
        default=None,
        metavar="TEXT",
        help="System prompt applied to every LLM call",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        metavar="MODEL",
        help=f"Model name to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print request metadata to stderr before each response",
    )
    return parser


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse and return CLI arguments."""
    return build_parser().parse_args(args)
