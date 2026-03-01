import argparse

from constants import TASK_MAP

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract structured outputs from an LLM.")
    parser.add_argument(
        "--task",
        required=True,
        choices=list(TASK_MAP.keys()),
        help="Analysis task to run",
    )
    parser.add_argument("--input", required=True, help="Text to analyse")
    
    return parser.parse_args()