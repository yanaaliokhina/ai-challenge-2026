# Day 13 – Simple Vector Search CLI

## Goal

Build a command-line tool that loads a persisted embedding index from disk, converts a user query into a vector using an embedding API, and retrieves the most semantically similar entries from the index.

## What We Should Build

A CLI application that:
- Loads a stored embedding index (JSON format, as produced in Day 12)
- Accepts a natural language query from the user
- Embeds the query using the same embedding model used to build the index
- Computes cosine similarity between the query vector and all stored vectors
- Returns the top-N most similar results with their scores

## Functional Requirements

### 1. Index Loading
- Read an embedding index from a local JSON file
- The index file contains a list of entries, each with:
  - `id`: unique identifier (string)
  - `text`: original text content (string)
  - `embedding`: list of floats (vector)
- Validate that the file exists and contains at least one entry
- Raise a clear error if the file is missing or malformed

### 2. Query Embedding
- Accept a query string as a CLI argument
- Send the query to the embedding API (same model as stored index)
- Return the query as a float vector

### 3. Similarity Search
- Compute cosine similarity between the query vector and each stored vector
- Rank all entries by descending similarity score
- Return the top-N results (default: 3, configurable via CLI flag)

### 4. Output
- Print each result to stdout in a readable format
- Each result must include:
  - Rank (1, 2, 3, ...)
  - Entry `id`
  - Similarity score (rounded to 4 decimal places)
  - Original `text` (truncated to 200 characters if longer)
- If no results are found, print a clear message

### 5. CLI Interface
- `--index` (required): path to the JSON index file
- `--query` (required): natural language search query
- `--top` (optional): number of top results to return (default: 3)
- `--model` (optional): embedding model name (default: matches index default)

### 6. Error Handling
- Missing index file: print error and exit with code 1
- Empty query string: print error and exit with code 1
- API failure: print error and exit with code 1
- Invalid JSON in index file: print error and exit with code 1

## Python Topics Covered

- argparse for CLI argument parsing
- JSON file loading and validation
- numpy for cosine similarity computation
- Type hints and dataclasses or Pydantic models
- Error handling with sys.exit

## AI Topics Covered

- Embedding API usage (query-time)
- Cosine similarity for semantic retrieval
- Query-to-vector search pattern
- Vector index as a retrieval backend

## Acceptance Criteria

- [ ] CLI accepts `--index`, `--query`, `--top`, and `--model` arguments
- [ ] Loads and validates the JSON index file
- [ ] Embeds the query using the embedding API
- [ ] Computes cosine similarity for all entries
- [ ] Returns the correct top-N results sorted by score descending
- [ ] Prints rank, id, score, and text for each result
- [ ] Handles missing file, empty query, and API errors gracefully
- [ ] All acceptance criteria covered by pytest tests
