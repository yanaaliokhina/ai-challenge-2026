# Day 6 – Token Counter Utility

## Goal

Build a command-line token counter utility that estimates token usage for text inputs before sending them to an LLM API. This teaches how tokenization works, why it matters for cost and context window management, and how to reason about token budgets.

---

## What We Should Build

A CLI utility that accepts text (from an argument, a file, or stdin) and reports:
- Token count for the input text
- The model's context window limit
- Percentage of the context window consumed
- Whether the input fits within the model's context window

The utility must support multiple models with different context window sizes.

---

## Functional Requirements

### 1. Token Counting

- Count tokens for a given input text using the `tiktoken` library
- Support at least the following models:
  - `gpt-4o` — 128,000 token context window
  - `gpt-4` — 8,192 token context window
  - `gpt-3.5-turbo` — 16,385 token context window
  - `claude-3-haiku` — 200,000 token context window (approximate, use `cl100k_base` encoding)
  - `claude-3-5-sonnet` — 200,000 token context window (approximate, use `cl100k_base` encoding)
- Default model: `gpt-4o`

### 2. Input Sources

The utility must accept text from exactly one of:
- `--text` argument: inline text string passed on the command line
- `--file` argument: path to a `.txt` or `.md` file to read and count tokens for
- `stdin`: if neither `--text` nor `--file` is provided, read from stdin

### 3. Output Format

The output must include:
- Input source (argument, file, or stdin)
- Model name used for counting
- Token count
- Context window size for the selected model
- Percentage of the context window used (rounded to 2 decimal places)
- A clear status line: `FITS` if token count is within the context window, `EXCEEDS` if it does not

### 4. Multi-text Batch Mode

- Add a `--batch` flag that accepts a `.txt` file where each line is a separate text entry
- For each line, output the token count and fit status
- At the end of batch mode, output a summary: total lines, total tokens, min/max/average tokens per line

### 5. Model Selection

- Accept a `--model` argument to select the model
- If an unsupported model is passed, print a clear error listing supported models and exit with code 1

### 6. Verbose Mode

- Add a `--verbose` flag
- In verbose mode, additionally output:
  - The list of individual tokens (decoded as strings) for the given text
  - Remaining token budget (context window minus token count)

### 7. Error Handling

- If `--file` is provided but the file does not exist, print a clear error and exit with code 1
- If `--batch` file is empty, print a warning and exit with code 0
- If both `--text` and `--file` are provided, print an error and exit with code 1

---

## Python Topics Covered

- Utility functions and module design
- File I/O (`open`, reading `.txt` and `.md` files)
- Type hints and typed return values
- `argparse` for CLI argument parsing
- `stdin` reading via `sys.stdin`
- Error handling with descriptive exit codes
- f-strings and formatted output

---

## AI Topics Covered

- Tokenization: what tokens are and why they differ from words
- The `tiktoken` library and its encoding schemes (`cl100k_base`, `o200k_base`)
- Model context window limits and their practical implications
- Token budgets: planning input + output to fit within a context window
- Why token count matters for cost and latency estimation

---

## Acceptance Criteria

- [ ] Counting tokens from `--text`, `--file`, and stdin all produce correct results
- [ ] Output always includes: model name, token count, context window, percentage used, and FITS/EXCEEDS status
- [ ] `--model` selects the correct tokenizer and context window
- [ ] Unsupported model name triggers a clean error with supported model list
- [ ] `--batch` mode processes each line and outputs a summary
- [ ] `--verbose` mode outputs individual token strings and remaining budget
- [ ] Providing both `--text` and `--file` triggers an error
- [ ] Missing file path triggers an error with exit code 1
- [ ] All logic is covered by pytest unit tests
