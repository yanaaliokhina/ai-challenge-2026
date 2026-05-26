"""CLI argument parser for day-16 project."""

import argparse
from constants import DEFAULT_MODEL


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Day-16 Tool Registry CLI")
        parser.add_argument("--prompt", required=True, help="Prompt to send to the LLM")
        parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
        parser.add_argument("--verbose", action="store_true", help="Print debug info")
        return parser.parse_args()
