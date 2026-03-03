import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send multiple prompts to Claude concurrently")
    parser.add_argument("prompts", nargs="*", help="One or more prompts to send")
    parser.add_argument("--file", help="Plain-text file with one prompt per line (takes precedence)")
    return parser.parse_args()


def load_prompts(args: argparse.Namespace) -> list:
    if args.file:
        lines = Path(args.file).read_text(encoding="utf-8").splitlines()
        return [line.strip() for line in lines if line.strip()]
    return list(args.prompts)