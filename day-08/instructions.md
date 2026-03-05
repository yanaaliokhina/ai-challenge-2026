# Day 8 – Generate Text Embeddings

## Goal

Build a command-line tool that generates vector embeddings for text inputs using the Claude (or compatible) embeddings API, and prints or saves the resulting vectors in a structured format.

## What We Should Build

A Python CLI script that accepts one or more text strings, sends them to an embeddings API, and returns the resulting embedding vectors. The tool must handle single and batch inputs, display basic metadata (model used, vector dimensions, input count), and optionally persist the results to a JSON file.

## Functional Requirements

### 1. Input Handling

- Accept a single text string via a CLI flag (`--text`)
- Accept a file of newline-separated texts via a CLI flag (`--file`)
- Exactly one of `--text` or `--file` must be provided; raise a clear error otherwise

### 2. Embedding Generation

- Send the input text(s) to an embeddings API using `httpx` (sync)
- Support a configurable model name via a `--model` flag with a sensible default
- Each text must produce exactly one embedding vector (list of floats)
- The implementation must use typed functions with explicit return types

### 3. Output

- Print a summary to stdout:
  - Number of inputs processed
  - Model used
  - Embedding dimension (length of each vector)
- Print the first 5 values of each embedding vector (truncated preview)
- Optionally save full results to a JSON file via `--output` flag
  - JSON structure: list of objects, each containing `text`, `model`, and `embedding` fields

### 4. Error Handling

- Raise a descriptive error if the API key is missing or the API call fails
- Raise a descriptive error if the input file does not exist or is empty
- All errors must surface a human-readable message (no raw tracebacks)

### 5. Configuration

- API key loaded from the `ANTHROPIC_API_KEY` environment variable (or the relevant provider's key)
- Model name and API endpoint stored as constants, not hardcoded inline

## Python Topics Covered

- Typed functions with return type annotations
- Dataclasses or Pydantic models for structured results
- `argparse` for CLI argument parsing
- `httpx` for synchronous HTTP requests
- JSON serialization with `json` module
- File I/O for reading input files and writing output

## AI Topics Covered

- Embedding API usage
- What embeddings are and what they represent
- Batch vs. single embedding requests
- Understanding embedding dimensions

## Acceptance Criteria

- `python src/main.py --text "Hello world"` prints a summary with dimension and truncated vector preview
- `python src/main.py --file inputs.txt` processes all lines in the file and prints a summary per input
- `python src/main.py --text "Hello" --output out.json` saves full embeddings to `out.json`
- Running without `--text` or `--file` prints a clear usage error
- All public functions have type annotations
- Tests cover: single text embedding, batch from file, missing API key error, output file structure
