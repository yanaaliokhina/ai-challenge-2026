# Day 12 – Embedding Index Storage

## Goal

Build a persistent embedding index that stores text chunks alongside their vector embeddings in a local JSON file, and supports loading, querying, and updating that index across multiple runs.

## What We Should Build

A CLI tool that:
1. Accepts a text file as input and splits it into chunks
2. Generates embeddings for each chunk via the LLM API
3. Saves the chunks and their embeddings to a local JSON index file
4. On subsequent runs, loads the existing index instead of re-embedding already-indexed content
5. Accepts a query string, embeds it, and returns the top-N most similar chunks from the stored index

## Functional Requirements

### 1. Text Chunking
- Accept a plain text file path via CLI argument
- Split the text into chunks of a configurable size (default: 300 characters)
- Overlap between chunks is optional but not required

### 2. Embedding Generation
- Generate a vector embedding for each chunk using the embeddings API
- Each chunk must be stored together with its embedding as a single index entry

### 3. JSON Index Storage
- Persist the index to a local JSON file (default path: `index.json` inside the day folder)
- The index format must include, for each entry:
  - `id`: a unique integer or UUID
  - `text`: the original chunk text
  - `embedding`: the embedding vector as a list of floats
- If the index file already exists, load it and skip re-embedding chunks that are already stored (identified by matching text content)

### 4. Query Mode
- Accept a query string via CLI argument
- Embed the query using the same embeddings API
- Compute cosine similarity between the query embedding and every stored chunk embedding
- Return the top-N results (default: 3) with their similarity scores and chunk text

### 5. CLI Interface
- `--file`: path to a text file to index
- `--query`: a query string to search the index
- `--top-n`: number of top results to return (default: 3)
- `--index`: path to the JSON index file (default: `index.json`)
- The tool must support running `--file` and `--query` independently or together in one command

### 6. Deduplication
- Before embedding a chunk, check if the same text already exists in the loaded index
- If it does, skip the API call and reuse the stored embedding

## Python Topics Covered

- JSON file I/O (read, write, append)
- argparse for multi-flag CLI
- List and dict manipulation
- Cosine similarity via manual computation or numpy
- UUID or integer ID generation

## AI Topics Covered

- Embeddings API usage
- Vector persistence across sessions
- Similarity search over a stored index
- Incremental indexing (skip already-embedded content)

## Acceptance Criteria

- Running `--file` on a text file produces a populated `index.json`
- Running `--file` again on the same file does not re-embed already-indexed chunks (no duplicate entries)
- Running `--query` returns the top-N most similar chunks with their similarity scores
- Running with both `--file` and `--query` indexes first, then queries
- The index file is valid JSON and can be inspected manually
- All logic is covered by at least one test per feature (indexing, deduplication, querying)
