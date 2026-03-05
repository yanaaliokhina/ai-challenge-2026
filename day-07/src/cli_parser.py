import argparse
from constants import DEFAULT_MODEL, DEFAULT_OUTPUT_FILE


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Prompt experiment CLI — send multiple prompt variations to an LLM and compare results"
        )
        parser.add_argument(
            "--prompts-file",
            required=True,
            help="Path to JSON or JSONL file with prompt variations",
        )
        parser.add_argument(
            "--output-file",
            default=DEFAULT_OUTPUT_FILE,
            help=f"Path to write results JSON (default: {DEFAULT_OUTPUT_FILE})",
        )
        parser.add_argument(
            "--model",
            default=DEFAULT_MODEL,
            help=f"Model name (default: {DEFAULT_MODEL})",
        )
        return parser.parse_args()
