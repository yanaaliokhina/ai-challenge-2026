# Day 1 – Build a Typed LLM API Client

## Goal

Build a minimal, well-typed Python client for the Anthropic Claude API. Practice making real LLM API calls using proper Python type hints, dataclasses, and error handling — without relying on high-level SDK abstractions.

---

## What We Should Build

A CLI script that accepts a user prompt as input, sends it to the Claude API using `httpx`, and prints the model's response to the terminal. The client must be structured using typed dataclasses and handle common API errors gracefully.

---

## Functional Requirements

### 1. Request Dataclass
- Define a typed dataclass `LLMRequest` with fields:
  - `model` (str) — the model name to use
  - `prompt` (str) — the user message
  - `max_tokens` (int) — maximum tokens in the response
  - `temperature` (float) — sampling temperature

### 2. Response Dataclass
- Define a typed dataclass `LLMResponse` with fields:
  - `content` (str) — the text returned by the model
  - `model` (str) — the model that responded
  - `input_tokens` (int) — number of tokens in the input
  - `output_tokens` (int) — number of tokens in the output

### 3. API Client Function
- Write a function `send_request(request: LLMRequest) -> LLMResponse` that:
  - Reads the API key from the environment variable `ANTHROPIC_API_KEY`
  - Sends a POST request to the Anthropic Messages API using `httpx`
  - Parses the response JSON into an `LLMResponse` dataclass
  - Raises a descriptive `RuntimeError` on non-2xx responses

### 4. Error Handling
- Handle the following failure cases explicitly:
  - Missing or empty `ANTHROPIC_API_KEY`
  - HTTP error responses (4xx, 5xx) with status code and message
  - Network/connection errors

### 5. CLI Entry Point
- `src/main.py` must accept a prompt via a positional command-line argument
- Print the response content to stdout
- Print input/output token counts to stdout

---

## Python Topics Covered

- Type hints (`str`, `int`, `float`, `dataclass`)
- `dataclasses.dataclass`
- `os.environ` for environment variable access
- `httpx` for HTTP requests
- Exception handling with `try/except`
- `argparse` for CLI argument parsing

---

## AI Topics Covered

- Making a direct API call to a language model
- Understanding the Messages API request/response structure
- Model parameters: `model`, `max_tokens`, `temperature`
- Token usage awareness

---

## Acceptance Criteria

- [ ] `LLMRequest` and `LLMResponse` are implemented as typed dataclasses
- [ ] `send_request()` uses `httpx` (not the Anthropic SDK) to call the API
- [ ] Running `python src/main.py "Your prompt here"` returns a model response
- [ ] Token counts (input and output) are printed after the response
- [ ] Missing API key raises a clear error message before making any network call
- [ ] HTTP errors are caught and reported with status code and body

---

## How to Run

1. Copy the environment file and add your API key:
   ```
   cp .env.example .env
   # Edit .env and set ANTHROPIC_API_KEY=your_key_here
   ```

2. Navigate to the day folder:
   ```
   cd day-01
   ```

3. Create and activate a virtual environment:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the challenge:
   ```
   python src/main.py "What is a large language model?"
   ```
