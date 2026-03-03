# Day 5 – CLI AI Assistant

## Goal

Build a fully functional command-line AI assistant that accepts user input through CLI flags and interactive mode, sends prompts to an LLM, and prints structured responses. The focus is on clean CLI design with `argparse` and practical prompt interaction patterns.

---

## What We Should Build

A CLI tool (`main.py`) that can:

1. Accept a prompt directly as a CLI argument (single-shot mode)
2. Launch an interactive REPL session where the user types prompts and receives responses one at a time (interactive mode)
3. Support optional flags to control behaviour: model selection, system prompt, and output verbosity

---

## Functional Requirements

### 1. Single-Shot Mode

- The user passes a prompt via `--prompt` flag
- The tool sends the prompt to the LLM and prints the response to stdout
- The program exits after printing the response

### 2. Interactive Mode

- Launched with `--interactive` flag (or `-i`)
- The tool enters a REPL loop:
  - Displays a prompt prefix (e.g. `You: `)
  - Reads input from stdin
  - Sends input to the LLM
  - Prints the LLM response prefixed with `Assistant: `
  - Loops until the user types `exit` or `quit` or sends EOF (Ctrl+D)
- Each turn in the loop is a fresh, independent call (no conversation memory required)

### 3. System Prompt Support

- Optional `--system` flag accepts a string used as the system prompt for every call
- If not provided, the LLM uses its default behaviour (no system message sent)

### 4. Model Selection

- Optional `--model` flag to specify the model name
- Must have a sensible default (e.g. `claude-haiku-4-5-20251001`)

### 5. Verbose Mode

- Optional `--verbose` flag (or `-v`)
- When enabled, prints additional metadata to stderr before the response:
  - Model used
  - System prompt (if any)
  - Input prompt

### 6. LLM Client

- Implement a simple synchronous `LLMClient` class in `src/llm_client.py`
- The client exposes a single `ask(prompt, system=None, model=None)` method
- API key is read from the `ANTHROPIC_API_KEY` environment variable
- HTTP calls are made using `httpx` (synchronous)
- Raise a clear `RuntimeError` with a descriptive message on API errors (non-2xx responses)

### 7. Argument Parsing

- All CLI arguments are handled in `src/cli_parser.py` using `argparse`
- `--prompt` and `--interactive` are mutually exclusive; exactly one must be provided
- Validation errors print a usage message and exit with a non-zero code

### 8. Entry Point

- `src/main.py` imports from `cli_parser` and `llm_client` and orchestrates the flow
- No business logic lives in `main.py` — it only wires components together

---

## Python Topics Covered

- `argparse`: mutually exclusive groups, default values, short flags
- Modular project structure: separating CLI parsing, LLM client, and entry point
- Synchronous HTTP with `httpx`
- Environment variable access with `os.environ`
- stdin reading and REPL loop patterns
- Error handling and clean exit codes

---

## AI Topics Covered

- Single-turn LLM prompt interaction
- System prompt usage
- Model selection via API
- CLI-driven prompt engineering workflow

---

## Acceptance Criteria

- `python src/main.py --prompt "What is 2+2?"` prints a response and exits
- `python src/main.py --interactive` starts a REPL that responds to each input and exits cleanly on `exit`/`quit`/EOF
- `--prompt` and `--interactive` cannot be used together; the program exits with an error if both are provided
- `--system "You are a pirate"` changes LLM behaviour visibly in the response
- `--verbose` prints model, system prompt, and input to stderr before the response
- `--model` overrides the default model
- All tests in `tests/` pass with `pytest`
- No implementation logic in `main.py` beyond wiring
