# Python AI 30-Day Challenge

A 30-day challenge to strengthen advanced Python skills and learn practical AI engineering —
one independent mini-project per day.

---

## What This Is

Each day is a **standalone project**. There is no evolving system, no shared codebase, no
dependencies between days. Every challenge can be picked up, understood, and run in isolation.

Each day focuses on:
- One clear **Python engineering concept**
- One clear **AI/LLM concept**
- A working, tested implementation

---

## Why This Structure

Building one cohesive system across 30 days is good for product work.
This challenge is for **learning** — so each day you context-switch into a fresh problem,
practice a specific skill deliberately, and finish with something that runs and is tested.

---

## Weekly Themes

| Week | Theme | Days |
|------|-------|------|
| Week 1 | LLM API & Prompt Foundations | 1–7 |
| Week 2 | Embeddings & RAG Basics | 8–14 |
| Week 3 | Agents & Tool Usage | 15–21 |
| Week 4 | Evaluation, Guardrails & Practical AI Engineering | 22–30 |

---

## Repository Structure

```
/python-ai-30-day-challenge
  README.md
  .env.example
  /day-01
      instructions.md   ← what to build and how
      notes.md          ← your learnings (fill in after)
      src/              ← implementation goes here
  /day-02
      ...
  /utils                ← optional shared helpers (e.g. .env loader)
  /docs                 ← architecture notes, references
```

Each day folder is self-contained. There is no project-wide `pyproject.toml` — each day
manages its own dependencies as needed.

---

## Daily Challenge Index

| Day | Title | Python Focus | AI Focus |
|-----|-------|-------------|----------|
| 01 | First LLM Call & Project Setup | packaging, env management | calling Anthropic API |
| 02 | Prompt Template Engine | Pydantic, dataclasses | prompt templates |
| 03 | Structured Output Parser | Pydantic validators, error handling | JSON schema outputs |
| 04 | Token Counter & Cost Estimator | type hints, dataclasses | token counting |
| 05 | Retry & Fallback LLM Client | decorators, custom exceptions | retry/fallback strategies |
| 06 | Async Batch LLM Caller | asyncio, semaphores | concurrent LLM calls |
| 07 | Prompt Version Manager CLI | Typer CLI, file I/O | prompt versioning |
| 08 | Embedding Generator + Similarity Search | numpy, type hints | embeddings, cosine similarity |
| 09 | Text Chunker with Strategies | dataclasses, strategy pattern | text chunking |
| 10 | In-Memory Vector Store | custom data structures, generics | vector search |
| 11 | Simple RAG Pipeline | composing components, pathlib | end-to-end RAG |
| 12 | File Document Indexer | file I/O, JSON persistence | document indexing |
| 13 | Conversation Memory Manager | dataclasses, collections | context window management |
| 14 | ChromaDB Mini-Indexer | third-party integration | persistent vector store |
| 15 | Tool Registry Pattern | decorators, function metadata | tool registration |
| 16 | ReAct Agent Loop | state machine, parsing | ReAct reasoning loop |
| 17 | Multi-Tool Agent | JSON schemas, dispatch | tool calling pattern |
| 18 | Sub-Agent Delegator | delegation pattern | sub-agent orchestration |
| 19 | Async Agent Task Queue | asyncio.Queue, workers | async agent execution |
| 20 | Agent Session Logger | context managers | agent observability |
| 21 | CLI Chatbot with Tools | REPL pattern, integration | chatbot with tool use |
| 22 | Output Guardrails Validator | validation patterns, regex | output guardrails |
| 23 | Prompt A/B Comparison | experiment design | prompt experiments |
| 24 | LLM Evaluation Harness | file loading, reporting | evaluation patterns |
| 25 | Prompt Response Cache | caching patterns, hashing | prompt caching |
| 26 | Latency Measurement Decorator | decorators, statistics | LLM latency profiling |
| 27 | Structured JSON Logger | logging handlers, formatters | LLM call logging |
| 28 | LLM Test Suite with Mocks | pytest, unittest.mock | mocking LLM APIs |
| 29 | AI Observability Reporter | dataclasses, aggregation | session metrics |
| 30 | Mini Standalone RAG Chatbot | integration, clean code | RAG + chat demo |

---

## How to Run Any Day

Each day is independent. General pattern:

```bash
# Navigate to the day
cd day-01/src

# Create a virtual environment (recommended per day, or use one shared venv)
python -m venv .venv
source .venv/bin/activate

# Install that day's dependencies
pip install -r requirements.txt   # if present
# or manually: pip install anthropic pydantic python-dotenv

# Copy env template
cp ../../.env.example .env
# Edit .env with your API keys

# Run
python main.py

# Run tests
pytest tests/ -v
```

---

## Environment Setup

Copy `.env.example` to `.env` in whichever day you're working on:

```dotenv
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here       # optional, for days that use OpenAI
```

The `.env.example` at the root can be copied into any day's `src/` folder.

---

## Suggested Git Workflow

One branch per day, merged to main when done:

```bash
git checkout -b day-01
# implement, test
git add day-01/
git commit -m "day-01: first LLM call and project setup"
git push origin day-01
# open PR → merge to main
git checkout main && git pull
git checkout -b day-02
```

Tag completed weeks:
```bash
git tag -a week-1 -m "Week 1 complete: LLM API + Prompt Foundations"
```

---

## Testing Approach

Each day should include at least a basic test:

| Tool | Use |
|------|-----|
| `pytest` | test runner |
| `unittest.mock` / `pytest-mock` | mock LLM API calls (never hit real API in tests) |
| `pytest-asyncio` | async test support (Week 3 onward) |

Rule: **all LLM API calls are mocked in tests**. Never spend tokens on tests.

```bash
# Run tests for a day
pytest day-05/src/tests/ -v

# Run with coverage
pytest day-05/src/tests/ --cov=day-05/src -v
```

---

## AI Learning Strategy

- **Week 1**: Get comfortable calling LLM APIs, parsing outputs, handling errors
- **Week 2**: Understand embeddings from scratch — write your own similarity search before using a library
- **Week 3**: Build agents bottom-up — understand the loop before using a framework
- **Week 4**: Treat AI outputs as untrusted data — validate, evaluate, measure everything

Each day builds *understanding*, not just working code. The goal is to be able to explain
every line of what you wrote.

---

## Python Skills Strengthened

By the end of Day 30, you will have practiced:

- Type hints, `TypeVar`, `Protocol`, `Annotated`
- Pydantic v2: models, validators, serialization
- Dataclasses for lightweight containers
- `asyncio`: `async/await`, `gather`, `Queue`, semaphores
- Context managers: `__enter__/__exit__`, `contextlib`
- Decorators: retry, timing, caching, registration
- Error handling: custom exceptions, `try/except/finally`
- pytest: fixtures, parametrize, mocking, async tests
- Typer: CLI building, commands, arguments, options
- Logging: structured logs, JSON formatters, handlers
- File I/O: `pathlib`, JSON, YAML
- Environment management: `pydantic-settings`, `python-dotenv`

---

## Notes on Scope

- Each challenge targets **≤ 3 hours** of focused work
- If a day runs long, ship what works — perfect is the enemy of done
- `notes.md` is for real reflections: what took longer, what you'd redo, what clicked
- There are no bonus points for over-engineering
