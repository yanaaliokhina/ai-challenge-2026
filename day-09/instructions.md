# Day 9 – Cosine Similarity Search

## Goal

Build a CLI tool that compares a query text against a set of candidate texts using cosine similarity on their embeddings, and ranks the candidates from most to least similar.

## What We Should Build

A Python CLI script that accepts a query string and a list of candidate texts (via file or inline flags), generates embeddings for all of them using the Voyage AI embeddings API, computes cosine similarity between the query and each candidate, and prints a ranked results table.

## Functional Requirements

### 1. Input Handling

- Accept a query string via `--query`
- Accept candidate texts from a newline-separated file via `--file`
- Both `--query` and `--file` are required; raise a clear error if either is missing
- Raise a descriptive error if the file does not exist or contains fewer than 2 lines

### 2. Embedding Generation

- Generate embeddings for the query and all candidates using the Voyage AI embeddings API via `httpx` (sync)
- Use a configurable model via `--model` flag with a sensible default
- All API communication must use `httpx` (sync) with explicit error handling

### 3. Cosine Similarity Computation

- Implement cosine similarity using `numpy` only (no external similarity libraries)
- Compute similarity between the query embedding and each candidate embedding
- Return a float in the range [-1.0, 1.0] for each pair

### 4. Output

- Print a ranked table to stdout with columns: `Rank`, `Score`, `Text`
- Rank 1 = highest similarity
- Scores rounded to 4 decimal places
- Text truncated to 80 characters in the display if longer

### 5. Error Handling

- Raise a descriptive error if `VOYAGE_API_KEY` is missing
- Raise a descriptive error if the API call fails (non-2xx response)
- Raise a descriptive error if any embedding vector is empty or malformed

### 6. Configuration

- API key loaded from `VOYAGE_API_KEY` environment variable
- Default model name and API endpoint stored as constants, not hardcoded inline

## Python Topics Covered

- `numpy` for vector math (dot product, norm, cosine similarity)
- Typed functions with explicit return type annotations
- Dataclasses or Pydantic models for structured results
- `argparse` for CLI argument parsing
- `httpx` for synchronous HTTP requests

## AI Topics Covered

- Cosine similarity as a measure of semantic closeness
- How embedding vectors encode meaning
- Ranking results by similarity score
- Query-vs-document comparison pattern (foundation of retrieval)

## Acceptance Criteria

- `python src/main.py --query "What is a neural network?" --file candidates.txt` prints a ranked table
- Results are ordered from highest to lowest cosine similarity score
- Scores are floats rounded to 4 decimal places
- Running without `--query` or `--file` prints a clear usage error
- All public functions have type annotations
- Tests cover: similarity computation correctness, ranking order, missing API key error, malformed input file
