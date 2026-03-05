# 🤖 Python AI 30-Day Challenge

A 30-day challenge to strengthen advanced Python skills and learn practical AI engineering —
one independent mini-project per day.

## 🎯 Purpose of This Challenge

Each day is a **standalone project**. There is no evolving system, no shared codebase, no
dependencies between days. Every challenge can be picked up, understood, and run in isolation. This 30-day challenge is designed to:

- Learn the fundamentals of AI through hands-on practice
- Strengthen advanced Python fundamentals
- Apply medium-level AI concepts in practical implementations
- Complete 30 completely independent mini-projects

IMPORTANT:
- Each day is standalone and unrelated to others
- Each task requires up to 3 hours of focused coding
- Python only 
- No enterprise-scale architecture
- Practical learning over theory


# 🗂 Repository Structure

```
/ai-challenge-2026
  README.md
  .env.example
  /day-01
      instructions.md      ← what to build and how
      usage_examples.md    ← day-specific run and test examples
      src/                 ← implementation goes here
      tests/               ← pytest tests
  /day-02
      ...
```

Each day:
- Is fully independent
- Contains implementation steps
- Includes reflection notes

Each day folder is self-contained. There is no project-wide `pyproject.toml` — each day manages its own dependencies as needed.


# ▶️ How to Run Any Challenge

Each day is fully self-contained. To run a challenge:

**1. Copy and export environment variables**
```bash
cp .env.example .env
# Fill in your API keys in .env

# Export variables so they are available in your shell session:
export $(grep -v '^#' .env | xargs)

# Or, to reuse the same .env across multiple days, export from the root:
set -a && source .env && set +a
```

**2. Navigate to the day folder**
```bash
cd day-01
```

**3. Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Run the challenge**
```bash
python src/main.py
```

> Each day includes a `usage_examples.md` with day-specific run commands, flags, and test instructions.


# 🧪 How to Run Tests

Each day that includes tests uses `pytest`. From inside the day folder (with the venv active):

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run a specific test file
pytest tests/test_main.py

# Run with output printed (useful for debugging)
pytest tests/ -s
```

> See each day's `usage_examples.md` for day-specific test commands and notes.


# 🤖 Claude Integration

This project includes Claude commands that automate the challenge workflow.

## Slash Commands

| Command | Description |
|---|---|
| `/generate-next-challenge` | Reads README.md, detects the next incomplete day, and generates `instructions.md` + `usage_examples.md` |
| `/implement-challenge` | Implements the latest generated challenge, runs tests, and marks it as ✅ DONE in README.md if they pass |

## Skills

Skills are reusable building blocks that Claude invokes automatically during every challenge implementation.

| Skill | Trigger | Description |
|---|---|---|
| `project-scaffold` | Every `/implement-challenge` invocation — no exceptions | Generates `constants.py`, `cli_parser.py`, `llm_client.py`, and `main.py` base structure with an `LLMClient.ask()` backed by `httpx` (sync). All static values live in `constants.py` only. |

## Workflow

```
/generate-next-challenge
       ↓
/implement-challenge
  (auto-invokes skills when applicable)
```

Each command is context-aware: it reads README.md to detect which day to act on and enforces the project's tech stack and scope rules automatically.


# 📅 The 30 Independent Challenges

## Week 1 – LLM & Prompt Basics

### Day 1 – Build a Typed LLM API Client ✅ DONE
- Python Focus: Type hints, dataclasses, error handling
- AI Focus: Making LLM API calls
- Deliverable: CLI script that sends a prompt and prints a response

### Day 2 – Prompt Template Engine ✅ DONE
- Python Focus: Class design, validation
- AI Focus: Prompt engineering basics

### Day 3 – Structured Outputs with Pydantic ✅ DONE
- Python Focus: Pydantic models
- AI Focus: JSON output validation

### Day 4 – Async LLM Calls ✅ DONE
- Python Focus: asyncio, concurrency
- AI Focus: Parallel prompt execution

### Day 5 – CLI AI Assistant ✅ DONE
- Python Focus: argparse or typer
- AI Focus: Basic prompt interaction

### Day 6 – Token Counter Utility ✅ DONE
- Python Focus: Utility functions
- AI Focus: Token estimation

### Day 7 – Prompt Experiment Script ✅ DONE
- Python Focus: File I/O
- AI Focus: Compare prompt variations

## Week 2 – Embeddings & RAG Fundamentals

### Day 8 – Generate Text Embeddings ✅ DONE
- Python Focus: Typed functions
- AI Focus: Embedding API usage

### Day 9 – Cosine Similarity Search
- Python Focus: numpy basics
- AI Focus: Similarity comparison

### Day 10 – Mini RAG Script
- Python Focus: Text chunking
- AI Focus: Retrieval-Augmented Generation

### Day 11 – Local Document Q&A
- Python Focus: File parsing
- AI Focus: Context injection

### Day 12 – Embedding Index Storage
- Python Focus: JSON storage
- AI Focus: Vector persistence

### Day 13 – Simple Vector Search CLI
- Python Focus: CLI design
- AI Focus: Query-to-vector retrieval

### Day 14 – Memory Buffer for Chat
- Python Focus: State management
- AI Focus: Conversation memory basics

## Week 3 – Agents & Tool Usage Basics

### Day 15 – Basic Agent Loop
- Python Focus: Clean control flow
- AI Focus: Reasoning loop

### Day 16 – Tool Registry Pattern
- Python Focus: Decorators
- AI Focus: Tool-calling mechanism

### Day 17 – Sub-Agent Delegation
- Python Focus: Modular design
- AI Focus: Delegation pattern

### Day 18 – Retry & Fallback Strategy
- Python Focus: Exception handling
- AI Focus: Robust AI calls

### Day 19 – Guardrail Validator
- Python Focus: Validation logic
- AI Focus: Output filtering

### Day 20 – Response Caching with Redis
- Python Focus: Redis basics
- AI Focus: Prompt-response caching

### Day 21 – Latency Measurement Tool
- Python Focus: Timing utilities
- AI Focus: Performance tracking

## Week 4 – Evaluation & Practical AI Engineering

### Day 22 – Prompt Evaluation Script
- Python Focus: Script structuring
- AI Focus: Output scoring

### Day 23 – Cost Estimation Utility
- Python Focus: Calculations
- AI Focus: Token-based cost estimation

### Day 24 – Structured Logging Setup
- Python Focus: Logging best practices
- AI Focus: AI request logging

### Day 25 – Async Batch Processing Script
- Python Focus: asyncio.gather
- AI Focus: Batch inference

### Day 26 – Simple Experiment Tracker
- Python Focus: JSON tracking
- AI Focus: Comparing outputs

### Day 27 – Context Manager for LLM Sessions
- Python Focus: Context managers
- AI Focus: Session lifecycle handling

### Day 28 – Output Sanitizer
- Python Focus: Regex and validation
- AI Focus: Safety filtering

### Day 29 – Mock LLM for Testing
- Python Focus: pytest + mocking
- AI Focus: Testing AI systems

### Day 30 – Mini AI Utility of Your Choice
- Python Focus: Clean design
- AI Focus: Any AI fundamental learned


# 🧠 Skills Strengthened

- Strong Python fundamentals
- Clean code organization
- Async programming
- API integrations
- AI fundamentals
- Prompt engineering
- RAG basics
- Agent basics
- Evaluation and experimentation