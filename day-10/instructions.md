# Day 10 – Mini RAG Script

## Goal

Build a minimal Retrieval-Augmented Generation (RAG) pipeline that chunks a text document, embeds the chunks, retrieves the most relevant chunk for a user query, and uses it as context for an LLM-generated answer.

## What We Should Build

A CLI script that:
1. Reads a plain text document from disk
2. Splits it into overlapping chunks
3. Embeds each chunk using an embedding API
4. Embeds a user query
5. Retrieves the top-K most similar chunks using cosine similarity
6. Injects the retrieved chunks into a prompt and calls the LLM for a final answer
7. Prints the answer to stdout

## Functional Requirements

### 1. Text Chunking

- Accept a plain `.txt` file as input
- Split the document into fixed-size chunks by word count (e.g. 100 words per chunk)
- Support a configurable overlap between consecutive chunks (e.g. 20 words)
- Each chunk must retain its original position index

### 2. Embedding

- Embed all chunks using an embedding API (e.g. `text-embedding-3-small` via OpenAI or equivalent)
- Embed the user query using the same model
- Store chunk text and its embedding vector together in memory (no external DB required)

### 3. Retrieval

- Compute cosine similarity between the query embedding and all chunk embeddings
- Return the top-K most relevant chunks (default K=3)
- K must be configurable via CLI argument

### 4. Answer Generation

- Construct a prompt that includes:
  - The retrieved chunks as context
  - The user query
  - An instruction for the LLM to answer using only the provided context
- Call the LLM API and return the response text

### 5. CLI Interface

- Required arguments:
  - `--file`: path to the input `.txt` document
  - `--query`: the question to answer
- Optional arguments:
  - `--top-k`: number of chunks to retrieve (default: 3)
  - `--chunk-size`: words per chunk (default: 100)
  - `--overlap`: overlapping words between chunks (default: 20)

### 6. Output

- Print the final LLM answer to stdout
- Optionally print retrieved chunk indices and similarity scores when `--verbose` flag is set

## Python Topics Covered

- File I/O and text processing
- List slicing for chunking with overlap
- numpy for cosine similarity
- argparse for CLI design
- Modular function design

## AI Topics Covered

- Text chunking strategies
- Embedding-based retrieval
- Context injection into prompts
- Retrieval-Augmented Generation (RAG) pattern
- Similarity search without a vector database

## Acceptance Criteria

- Given a `.txt` file and a query, the script returns a relevant answer grounded in the document
- Chunking produces non-empty, overlapping chunks that together cover the full document
- Retrieval selects chunks with highest cosine similarity to the query
- The LLM prompt includes the retrieved chunks as context
- All CLI arguments are validated; missing required args produce a clear error
- Tests verify chunking logic, cosine similarity ranking, and prompt construction independently of the live API
