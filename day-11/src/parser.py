import re
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def parse_file(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        print(
            f"Error: unsupported file type '{ext}'. Only .txt and .md are supported.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        print(f"Error: failed to read '{file_path}' as UTF-8: {e}", file=sys.stderr)
        sys.exit(1)

    if ext == ".md":
        content = strip_markdown(content)

    return preprocess(content)


def strip_markdown(text: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def preprocess(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text
