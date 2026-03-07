from pathlib import Path

def load_candidates(file_path: str) -> list[str]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Candidates file not found: {file_path}")

    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError(f"Candidates file must contain at least 2 non-empty lines, got {len(lines)}")

    return lines