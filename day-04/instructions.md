# Day 4 – Async LLM Calls

## Goal

Build an async Python script that sends multiple prompts to the Claude API concurrently using `asyncio` and `httpx`, and demonstrates the performance advantage of parallel execution over sequential calls.

---

## What We Should Build

A command-line script that:
- Accepts a list of prompts (via CLI arguments or an input file)
- Dispatches all prompts to the Claude API **concurrently** using `asyncio.gather`
- Collects responses while preserving the original prompt order
- Measures and reports total wall-clock time for the concurrent run
- Handles per-prompt errors gracefully so one failure does not abort the others

---

## Functional Requirements

### 1. Input

- Accept multiple prompts as positional CLI arguments.
- Alternatively, accept a `--file` flag pointing to a plain-text file where each line is one prompt.
- If both are provided, the file takes precedence.
- Reject empty input with a clear error message.

### 2. Async Execution

- Use `asyncio` as the concurrency primitive.
- Use `httpx.AsyncClient` for all HTTP communication with the Claude API.
- Dispatch all prompts simultaneously with `asyncio.gather`.
- Each prompt must be wrapped in its own `async` function.

### 3. Result Collection

- Collect one result per prompt.
- Results must be returned in the **same order** as the input prompts, regardless of which API call finishes first.
- Each result must include:
  - The original prompt (truncated to 60 characters for display)
  - The model's response text
  - Whether the call succeeded or failed

### 4. Error Handling

- If a single prompt call raises an exception (network error, API error, timeout), capture the error message and mark that result as failed.
- Do not cancel or raise from the other concurrent calls.
- Use `return_exceptions=True` in `asyncio.gather` or equivalent per-task error isolation.

### 5. Timing

- Measure total wall-clock time from the moment all tasks are dispatched to the moment all results are collected.
- Print the elapsed time at the end of the output.

### 6. Output Format

Print results to stdout in a human-readable format, one block per prompt:

```
[1] Prompt: <truncated prompt>
    Status: OK | ERROR
    Response: <response text or error message>

...

Total time: X.XXs
```

### 7. Configuration

- Read the Claude API key from the `ANTHROPIC_API_KEY` environment variable.
- Use a configurable model name (default: `claude-haiku-4-5-20251001`).
- Use a configurable `max_tokens` (default: `256`).
- These may be constants at the top of the file or in a dedicated constants module.

---

## Python Topics Covered

- `async def` / `await`
- `asyncio.run`
- `asyncio.gather` with `return_exceptions=True`
- `httpx.AsyncClient` and async context managers
- `time.perf_counter` for wall-clock measurement
- `argparse` for CLI input

---

## AI Topics Covered

- Parallel prompt execution against an LLM API
- Understanding concurrency benefits for LLM workloads
- Per-request error isolation in AI pipelines
- Relationship between concurrency and API rate limits

---

## Acceptance Criteria

- [ ] Script runs from CLI and accepts multiple prompts
- [ ] All prompts are dispatched concurrently (not sequentially)
- [ ] Results are printed in input order
- [ ] A failed prompt prints an error message without crashing the script
- [ ] Total elapsed time is printed
- [ ] The `ANTHROPIC_API_KEY` environment variable is required and checked at startup
- [ ] Tests verify concurrent dispatch, result ordering, and error isolation
- [ ] All tests pass with `pytest tests/ -v`
