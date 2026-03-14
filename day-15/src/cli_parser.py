import argparse
from constants import DEFAULT_MODEL, DEFAULT_MAX_ITERATIONS


class CLIParser:
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Day-15 Basic Agent Loop")
        parser.add_argument("--task", required=True, help="Task for the agent to solve")
        parser.add_argument("--max-iterations", type=int, default=DEFAULT_MAX_ITERATIONS, help=f"Max loop iterations (default: {DEFAULT_MAX_ITERATIONS})")
        parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
        return parser.parse_args()
