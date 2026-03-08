from constants import PROMPT_TEMPLATE


def build_prompt(document: str, query: str) -> str:
    return PROMPT_TEMPLATE.format(document=document, query=query)
