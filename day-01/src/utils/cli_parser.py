
import argparse
from utils.constants import DEFAULT_MAX_TOKENS, DEFAULT_MODEL, DEFAULT_TEMPERATURE

def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(description="Send a prompt to Claude and print the response.")
    
    parser.add_argument("prompt", type=str, help="The prompt to send to the model.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    
    return parser.parse_args()