ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024

SUPPORTED_MODELS = {
    "gpt-4o": {"encoding": "o200k_base", "context_window": 128000},
    "gpt-4": {"encoding": "cl100k_base", "context_window": 8192},
    "gpt-3.5-turbo": {"encoding": "cl100k_base", "context_window": 16385},
    "claude-3-haiku": {"encoding": "cl100k_base", "context_window": 200000},
    "claude-3-5-sonnet": {"encoding": "cl100k_base", "context_window": 200000},
}

DEFAULT_COUNTER_MODEL = "gpt-4o"
