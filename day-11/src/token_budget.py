import sys


def estimate_tokens(text: str) -> int:
    word_count = len(text.split())
    return int(word_count / 0.75)


def apply_budget(text: str, max_tokens: int) -> tuple[str, bool]:
    estimated = estimate_tokens(text)
    if estimated <= max_tokens:
        return text, False

    print(
        f"Warning: document exceeds token budget (estimated {estimated} tokens > max {max_tokens}). Truncating.",
        file=sys.stderr,
    )
    target_words = int(max_tokens * 0.75)
    truncated = " ".join(text.split()[:target_words])
    return truncated, True
