# Day 2 – Prompt Template Engine

## Goal

Build a reusable prompt template engine that renders structured prompts from named
placeholders, validates required variables, and supports multiple template formats.

---

## What We Should Build

A Python module that defines a `PromptTemplate` class. The class accepts a template
string with named placeholders and renders a final prompt string by substituting
provided variables. It must validate that all required placeholders are supplied
before rendering, and raise a descriptive error when any are missing.

A CLI entry point allows rendering a named template from the command line by passing
variable values as arguments.

---

## Functional Requirements

### 1. PromptTemplate class

- Accepts a template string on initialisation (e.g. `"Translate {text} into {language}."`)
- Parses the template to extract all placeholder names automatically
- Exposes a `.render(**kwargs)` method that substitutes placeholders and returns the
  final string
- Raises a `MissingVariableError` (custom exception) listing every missing placeholder
  when `.render()` is called without all required variables
- Raises a `ValueError` when extra (unused) variables are passed — no silent ignoring

### 2. TemplateLibrary class

- Stores named templates in memory (dict-backed)
- `.register(name: str, template: PromptTemplate)` — adds a template
- `.get(name: str) -> PromptTemplate` — retrieves a template by name; raises
  `KeyError` if not found
- `.list_templates() -> list[str]` — returns sorted list of registered template names

### 3. Predefined templates

Register at least three ready-to-use templates in a `templates.py` module:

- `"translate"` — translates `{text}` into `{language}`
- `"summarise"` — summarises `{text}` in `{num_sentences}` sentences
- `"qa"` — answers `{question}` given `{context}`

### 4. CLI entry point (`src/main.py`)

- Accepts `--template` (name of a registered template) and `--var KEY=VALUE` pairs
  (repeatable flag) as CLI arguments
- Renders the selected template with the supplied variables and prints the result to
  stdout
- Prints a clear error message and exits with code 1 on validation failure

### 5. Type safety

- All public methods and functions must have full type annotations
- Use `dataclasses` or plain classes with `__slots__` where appropriate

---

## Python Topics Covered

- Class design and encapsulation
- Custom exceptions
- String parsing (`str.format_map`, `string.Formatter`)
- `argparse` for CLI argument handling
- Type annotations
- `dataclasses`
- Unit testing with `pytest`

---

## AI Topics Covered

- Prompt engineering basics
- Placeholder-based prompt templating
- Reusable prompt libraries
- Variable injection into prompts

---

## Acceptance Criteria

- `PromptTemplate.render()` correctly substitutes all placeholders
- `MissingVariableError` is raised with a message listing missing variable names when
  any placeholder is not supplied
- `ValueError` is raised when unknown extra variables are passed
- `TemplateLibrary` can register, retrieve, and list templates
- All three predefined templates are registered and renderable
- CLI renders a template from the command line and prints the result
- CLI exits with code 1 and prints an error on missing variables
- All public APIs are fully type-annotated
- Tests cover: successful render, missing variable error, extra variable error,
  library registration and retrieval
