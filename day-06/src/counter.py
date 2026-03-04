import tiktoken
from constants import SUPPORTED_MODELS


def get_encoding(model: str) -> tiktoken.Encoding:
    encoding_name = SUPPORTED_MODELS[model]["encoding"]
    return tiktoken.get_encoding(encoding_name)


def count_tokens(text: str, model: str) -> int:
    enc = get_encoding(model)
    return len(enc.encode(text))


def get_token_strings(text: str, model: str) -> list[str]:
    enc = get_encoding(model)
    token_ids = enc.encode(text)
    return [enc.decode([tid]) for tid in token_ids]
