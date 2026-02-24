# Coding Challenges: Day 01 – Day 05

# Day 01 – First LLM Call & Project Setup

## Goal

Set up a minimal, clean Python project and make your first real call to the Anthropic API.
No frameworks, no abstractions — just a well-structured script that loads config, calls the LLM,
and handles errors properly. By the end, you have a working, testable foundation.

---

## What to Build

1. A `pyproject.toml` (or `requirements.txt`) for the day's dependencies
2. A `config.py` — typed settings loaded from `.env` using `pydantic-settings`
3. A `client.py` — a thin wrapper around the Anthropic SDK
4. A `main.py` — entry point that calls the LLM with a question and prints the answer
5. A `tests/test_client.py` — tests with mocked API calls

---

## Python Skill Focus

- **Python packaging**: `pyproject.toml`, editable installs, virtual environments
- **Environment management**: loading secrets from `.env` with `pydantic-settings`
- **Type hints**: full annotations on every function (`-> str`, `-> None`, etc.)
- **Module structure**: `__init__.py`, clean imports
- **Error handling**: catching specific exceptions, not bare `except:`

---

## AI Concept Focus

- **Calling an LLM API**: understanding the request structure (messages, roles, max_tokens)
- **Message roles**: `user`, `assistant`, `system` — what each means
- **API response structure**: how to extract the text from an Anthropic response
- **Model selection**: understanding model tiers (Haiku = fast/cheap, Sonnet = balanced)

---

## Day 02 – Prompt Template Engine

### Goal
Build a reusable prompt template system that supports named variable substitution and stores
templates in a registry. No LLM call today — focus on clean Python data modeling.

### What to Build
- A `PromptTemplate` class that holds a template string with `{variable}` placeholders
- A `render(**kwargs)` method that substitutes variables and raises a clear error on missing/extra ones
- A `TemplateRegistry` class that stores templates by name and allows retrieval and rendering
- A `main.py` demonstrating creating, registering, and rendering real AI prompts (QA, summarize, translate)
- Tests covering: successful render, missing variable error, extra variable error, partial render, registry lookup

### Python Skill Focus
- **Dataclasses** with `__post_init__` for derived state (extracting variable names via `re.findall`)
- **Pydantic v2** — optionally model templates with `BaseModel` and `Field` validators
- **Custom exceptions** — `TemplateError` with informative messages
- **Type hints** — `dict[str, str]`, `list[str]`, `Optional`
- **String formatting** — `str.format(**kwargs)` vs `str.format_map()`

### AI Concept Focus
- **Prompt templates** — how production AI systems avoid hardcoding prompts as inline strings
- **Variable substitution** — `{user_input}`, `{context}`, `{language}` as reusable prompt slots
- **System vs user prompts** — structuring prompts with separate sections
- **Template reuse** — why naming and versioning prompts matters for debugging and A/B testing

---

## Day 03 – Structured Output Parser

### Goal
Build a parser that extracts JSON from raw LLM responses and validates it against
a Pydantic schema. LLMs don't always output clean JSON — your parser must handle
code fences, inline JSON, and embedded JSON in prose.

### What to Build
- A `StructuredOutputParser[T]` generic class that accepts a Pydantic model as its schema
- An `_extract_json()` method with 3 strategies: code fence (` ```json ``` `), raw `{...}`, embedded in text
- A `parse(raw: str) -> T` method that extracts then validates
- A `get_schema_json()` method that returns the JSON schema string (to inject into prompts)
- Example schemas: `SentimentResult`, `ExtractedEntities`, `SummaryResult`
- Tests covering: each extraction strategy, no JSON found, invalid JSON, schema mismatch

### Python Skill Focus
- **Pydantic v2** — `BaseModel`, `model_validate`, `ValidationError`, `model_json_schema()`
- **Generics** — `TypeVar`, `Generic[T]`, `Type[T]` to make the parser work with any schema
- **Regex** — `re.search` with code fence and brace patterns
- **Error handling** — wrapping `json.JSONDecodeError` and `ValidationError` into `ParseError`
- **Type hints** — precise return types on a generic class

### AI Concept Focus
- **Structured outputs** — prompting LLMs to return machine-readable JSON
- **JSON schema** — how including a schema in the prompt constrains LLM output format
- **Output validation** — why you can't trust raw LLM strings as structured data
- **Extraction strategies** — LLMs wrap JSON in fences, prose, or output it raw — handle all three

---

## Day 04 – Token Counter & Cost Estimator

### Goal
Build a utility that counts tokens in text and calculates estimated API cost for
a given model and usage. Understand how input and output tokens are priced differently.

### What to Build
- A `Model` enum with values for Haiku, Sonnet, and Opus
- `ModelPricing` and `TokenUsage` as frozen dataclasses (immutable value objects)
- A `CostEstimate` dataclass with `total_cost_usd` property and a readable `__str__`
- A `PRICING` registry dict mapping each `Model` to its `ModelPricing`
- A `count_tokens(text: str) -> int` function using `tiktoken` with word-count fallback
- An `estimate(usage, model) -> CostEstimate` function and a convenience `estimate_from_text()`
- Tests covering: zero cost, 1M token cost, total = input + output, token counting

### Python Skill Focus
- **`@dataclass(frozen=True)`** — immutable value objects for money/measurement types
- **Enums** — `Model(str, Enum)` for type-safe model names
- **Type hints** — `dict[Model, ModelPricing]`, `Literal`, precise numeric types
- **`__str__`** override for readable output formatting
- **Optional dependency** — `try: import tiktoken / except ImportError: fallback`

### AI Concept Focus
- **Token counting** — why tokens ≠ words and how BPE tokenizers work
- **Cost estimation** — input tokens and output tokens have different per-token prices
- **Model pricing tiers** — Haiku (cheap/fast) vs Sonnet vs Opus cost differences
- **Budget management** — why tracking token usage matters in production AI systems

---

## Day 05 – Retry & Fallback LLM Client

### Goal
Build a resilient LLM client that retries on transient failures using exponential backoff
with jitter, and falls back to an alternative model when the primary model fails.

### What to Build
- An exception hierarchy: `LLMError` → `RateLimitError`, `AuthenticationError`, `ModelUnavailableError`, `MaxRetriesExceededError`
- A `RetryConfig` frozen dataclass with: `max_attempts`, `base_delay`, `max_delay`, `jitter`, `retryable_exceptions`
- A `@with_retry(config)` decorator that retries the wrapped function on retryable exceptions
- A `ResilientLLMClient` with a `primary_model` and `fallback_model` — falls back when primary fails
- Tests covering: succeeds on first try, retries N times, raises after max attempts, fallback triggered

### Python Skill Focus
- **Decorators** — `functools.wraps`, parameterized decorator factory `with_retry(config)(func)`
- **`ParamSpec` + `TypeVar`** — correct typing for decorators that preserve argument signatures
- **Custom exception hierarchy** — specific types for retryable vs permanent failures
- **`time.sleep` + jitter** — `random.random()` to prevent synchronized retries (thundering herd)
- **`@dataclass(frozen=True)`** — `RetryConfig` as an immutable config object

### AI Concept Focus
- **Retry strategies** — when to retry (rate limits, timeouts) vs when not to (auth errors)
- **Exponential backoff** — delay grows as `base * 2^attempt` to reduce pressure on the API
- **Jitter** — adding randomness prevents multiple clients from retrying simultaneously
- **Fallback models** — routing to cheaper/faster model when primary is unavailable
- **Transient vs permanent failures** — HTTP 429 is retryable; HTTP 401 is not
