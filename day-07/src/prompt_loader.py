import json
import sys
from pathlib import Path
from typing import Any


def load_prompts(file_path: str) -> list[dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        if path.suffix == ".jsonl":
            entries = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    entries.append(json.loads(line))
            return entries
        else:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: failed to parse {file_path}: {e}", file=sys.stderr)
        sys.exit(1)
