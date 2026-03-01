# Day 3 – Structured Outputs with Pydantic

## Goal

Build a module that sends a prompt to an LLM and reliably parses its response into a
validated Pydantic model, raising clear errors when the output is malformed or fails
schema validation.

---

## What We Should Build

A Python module that wraps an LLM API call, instructs the model to reply in JSON, and
deserialises the raw string response into a typed Pydantic model. When the LLM returns
invalid JSON or a JSON object that does not match the expected schema, the module must
raise a descriptive error rather than silently returning bad data.

A CLI entry point allows sending a structured-output request from the command line and
printing the validated result as formatted JSON.

---

## Functional Requirements

### 1. Pydantic response models

Define at least two Pydantic models that represent structured LLM responses:

- `SentimentResult` — contains:
  - `sentiment`: a `Literal["positive", "negative", "neutral"]` field
  - `confidence`: a `float` between 0.0 and 1.0 (inclusive), validated with a Pydantic
    field constraint
  - `reasoning`: a non-empty `str`

- `KeyFacts` — contains:
  - `facts`: a non-empty `list[str]` (at least one item)
  - `source_topic`: a non-empty `str`

### 2. `StructuredLLMClient` class

- Accepts an `httpx.AsyncClient` and a model name string on initialisation
- Exposes an async method `.ask(prompt: str, response_model: type[T]) -> T` where `T`
  is a Pydantic `BaseModel` subclass
- The method must:
  - Build a system message instructing the LLM to respond only with valid JSON matching
    the model's schema
  - Call the LLM API (Anthropic messages endpoint) with the prompt
  - Extract the text content from the response
  - Parse the text as JSON
  - Validate the parsed dict against `response_model` using Pydantic
  - Return the validated model instance
- Raises `JSONDecodeError` (from `json` stdlib) when the response is not valid JSON
- Raises `pydantic.ValidationError` when the JSON does not match the schema

### 3. Schema injection

- `StructuredLLMClient.ask()` must automatically include the JSON schema of the
  `response_model` in the system prompt so the LLM knows the exact shape to produce
- Use `response_model.model_json_schema()` to obtain the schema

### 4. CLI entry point (`src/main.py`)

- Accepts `--task` (one of: `sentiment`, `facts`) and `--input` (the text to analyse)
  as required CLI arguments
- Routes to the appropriate Pydantic model based on `--task`
- Calls `StructuredLLMClient.ask()` and prints the validated result as indented JSON to
  stdout
- Prints a clear error message and exits with code 1 on `JSONDecodeError` or
  `ValidationError`

### 5. Type safety

- All public methods and functions must have full type annotations
- Use `TypeVar` to type the generic `response_model` parameter of `.ask()`
- Use Pydantic `Field` for model constraints (confidence bounds, non-empty lists/strings)

---

## Python Topics Covered

- Pydantic models and field validation
- Generic functions with `TypeVar`
- `json` module: parsing and error handling
- `asyncio` for async HTTP calls
- `httpx.AsyncClient`
- `argparse` for CLI argument handling
- Type annotations with `Literal`, `TypeVar`, `type[T]`

---

## AI Topics Covered

- Structured outputs from LLMs
- JSON output validation
- Schema injection into system prompts
- Prompt engineering for reliable JSON responses
- Handling malformed LLM responses gracefully

---

## Acceptance Criteria

- `SentimentResult` and `KeyFacts` models validate correct inputs and reject invalid ones
- `StructuredLLMClient.ask()` correctly parses a valid JSON LLM response into the
  target model
- `JSONDecodeError` is raised when the LLM response is not valid JSON
- `pydantic.ValidationError` is raised when the JSON does not match the schema
- The schema of the target model is included in the system prompt sent to the LLM
- CLI routes `--task sentiment` and `--task facts` to the correct models
- CLI prints validated output as indented JSON on success
- CLI exits with code 1 and prints an error on parse or validation failure
- All public APIs are fully type-annotated
- Tests cover: valid parse, invalid JSON, schema mismatch, model field validation,
  CLI routing
