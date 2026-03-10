import json
import sys
from pathlib import Path
from pydantic import BaseModel, ValidationError


class IndexEntry(BaseModel):
    id: str
    text: str
    embedding: list[float]


def load_index(path: str) -> list[IndexEntry]:
    file_path = Path(path)
    if not file_path.exists():
        print(f"Error: Index file not found: {path}")
        sys.exit(1)
    try:
        with open(file_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in index file: {e}")
        sys.exit(1)
    if not isinstance(data, list) or len(data) == 0:
        print("Error: Index file must contain a non-empty list of entries")
        sys.exit(1)
    try:
        entries = [IndexEntry(**item) for item in data]
    except (ValidationError, TypeError) as e:
        print(f"Error: Malformed index entry: {e}")
        sys.exit(1)
    return entries
