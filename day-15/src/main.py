from cli_parser import CLIParser
from llm_client import LLMClient
from agent import run_agent

if __name__ == "__main__":
    args = CLIParser().parse_args()
    client = LLMClient()
    run_agent(task=args.task, max_iterations=args.max_iterations, client=client, model=args.model)
