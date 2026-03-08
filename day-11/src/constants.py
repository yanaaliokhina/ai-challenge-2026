ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
DEFAULT_MAX_DOC_TOKENS = 3000

PROMPT_TEMPLATE = (
    "You are a helpful assistant. Answer the user's question using ONLY the information "
    "provided in the document below. Do not use any external knowledge.\n\n"
    "Document:\n{document}\n\n"
    "Question: {query}\n\n"
    "Answer:"
)
