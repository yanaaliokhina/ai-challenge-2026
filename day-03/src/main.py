import asyncio
import json
import sys
from typing import Union

import httpx
import pydantic

from client import StructuredLLMClient
from cli_parser import parse_args
from constants import MODEL, TASK_MAP

async def run(task: str, input_text: str) -> None:
    response_model = TASK_MAP[task]
    
    async with httpx.AsyncClient() as http_client:
        client = StructuredLLMClient(http_client=http_client, model=MODEL)
        result = await client.ask(prompt=input_text, response_model=response_model)
        print(json.dumps(result.model_dump(), indent=2))


def main() -> None:
    args = parse_args()
    
    try:
        asyncio.run(run(args.task, args.input))
    except (json.JSONDecodeError, pydantic.ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
