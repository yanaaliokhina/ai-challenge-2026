# Day 11 – Local Document Q&A

## Goal

Build a CLI tool that reads a local document from disk, parses and cleans its content, and answers a user question by injecting the full document as context into an LLM prompt — without any embedding or retrieval step.

## What We Should Build

A CLI script that:
1. Accepts a local `.txt` or `.md` file as input
2. Parses and cleans the file content based on its format
3. Estimates the token count of the document content
4. Warns the user if the document exceeds a configurable token budget
5. Injects the full document content into a prompt template
6. Sends the prompt to an LLM API and prints the answer

## Functional Requirements

### 1. File Parsing

- Accept `.txt` and `.md` files via the `--file` argument
- For `.txt` files: read the raw content as-is
- For `.md` files: strip Markdown formatting (headers `#`, bold `**`, italic `*`, inline code `` ` ``, links `[text](url)`) and return plain text
- Reject unsupported file extensions with a clear error message
- Handle UTF-8 encoding; raise a clear error on encoding failures

### 2. Content Preprocessing

- Strip leading and trailing whitespace from the full document
- Collapse sequences of more than two consecutive blank lines into a single blank line
- Preserve paragraph structure (single blank lines between sections)

### 3. Token Budget Check

- Estimate the token count of the cleaned document using a simple word-based approximation: `tokens ≈ words / 0.75`
- Accept a `--max-tokens` CLI argument (default: 3000)
- If the estimated token count exceeds `--max-tokens`, print a warning to stderr and truncate the document to fit within the budget before injecting it into the prompt
- Do not raise an exception on truncation — warn and continue

### 4. Context Injection

- Construct a prompt with the following structure:
  - A system-level instruction telling the LLM to answer using only the provided document
  - The cleaned document content as context
  - The user's question
- The prompt template must be defined as a module-level constant string with named placeholders

### 5. CLI Interface

- Required arguments:
  - `--file`: path to the input document
  - `--query`: the question to answer
- Optional arguments:
  - `--max-tokens`: maximum token budget for the document content (default: 3000)
  - `--verbose`: if set, print the estimated token count and whether truncation occurred before printing the answer

### 6. Output

- Print the LLM's answer to stdout
- In verbose mode, print before the answer:
  - Estimated token count of the document
  - Whether the document was truncated (`truncated: yes/no`)

## Python Topics Covered

- File I/O and UTF-8 encoding handling
- `pathlib.Path` for file extension detection
- Regular expressions for Markdown stripping
- String manipulation and whitespace normalization
- `argparse` for CLI design

## AI Topics Covered

- Direct context injection into prompts
- Token budget estimation and truncation
- Prompt template design for document Q&A
- Grounding LLM answers in a provided document

## Acceptance Criteria

- Given a `.txt` or `.md` file and a query, the script returns an answer grounded in the document content
- Markdown stripping removes formatting characters without removing meaningful words or sentences
- Token estimation triggers a warning and truncation when the document exceeds `--max-tokens`
- Unsupported file types produce a clear error message and exit with a non-zero code
- Tests verify Markdown stripping, whitespace normalization, token estimation, and truncation logic independently of the live API
