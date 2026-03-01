import string
from dataclasses import dataclass


class MissingVariableError(Exception):
    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(f"Missing variables: {', '.join(missing)}")


@dataclass
class PromptTemplate:
    template: str

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset(self._placeholders)
    
    def __post_init__(self) -> None:
        formatter = string.Formatter()
        self._placeholders: set[str] = {
            fname
            for _, fname, _, _ in formatter.parse(self.template)
            if fname is not None
        }

    def render(self, **kwargs: str) -> str:
        missing = sorted(self._placeholders - set(kwargs.keys()))
        if missing:
            raise MissingVariableError(missing)

        extra = sorted(set(kwargs.keys()) - self._placeholders)
        if extra:
            raise ValueError(f"Unknown variables: {', '.join(extra)}")

        return self.template.format_map(kwargs)

    
