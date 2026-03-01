from template import PromptTemplate


class TemplateLibrary:
    def __init__(self) -> None:
        self._templates: dict[str, PromptTemplate] = {}

    def register(self, name: str, template: PromptTemplate) -> None:
        self._templates[name] = template

    def get(self, name: str) -> PromptTemplate:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found")
        return self._templates[name]

    def list_templates(self) -> list[str]:
        return sorted(self._templates.keys())
