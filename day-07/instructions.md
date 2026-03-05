# Day 7 – Prompt Experiment Script

## Goal

Build a CLI tool that loads multiple prompt variations from a file, sends each to an LLM, and saves the results to a structured output file for comparison.

## What We Should Build

A script that reads a set of prompt variations from a JSONL or JSON file, executes each against an LLM API, collects the responses, and writes a structured results file. The tool enables systematic comparison of prompt variations to understand how phrasing affects LLM output.

## Functional Requirements

### Input

1. Accept a `--prompts-file` argument pointing to a JSON or JSONL file.
2. Each entry in the file must include at minimum:
   - `id` — a unique string identifier for the prompt variation
   - `prompt` — the prompt text to send to the LLM
3. Optionally, each entry may include:
   - `label` — a human-readable description of what the variation tests
4. Accept a `--output-file` argument specifying where to write results (default: `results.json`).
5. Accept a `--model` argument to select the LLM model (default to a constant defined in `constants.py`).

### Processing

6. Load and parse all prompt variations from the input file.
7. Send each prompt to the LLM in sequence (not concurrently).
8. For each prompt, capture:
   - The original prompt text
   - The LLM response text
   - Response latency in milliseconds (wall-clock time of the API call)
9. Handle API errors gracefully: if a single prompt fails, record the error and continue with the remaining prompts.

### Output

10. Write all results to the specified output file as a JSON array.
11. Each result entry must include:
    - `id`
    - `label` (if present in input, otherwise omit or set to `null`)
    - `prompt`
    - `response` (string, or `null` on error)
    - `latency_ms` (integer or float)
    - `error` (string if an error occurred, otherwise `null`)
12. Print a summary to stdout after all prompts are processed:
    - Total prompts attempted
    - Number of successful responses
    - Number of failures
    - Average latency in milliseconds (for successful responses only)

### File I/O

13. Support both `.json` (array of objects) and `.jsonl` (one JSON object per line) input formats, detected automatically by file extension.
14. If the input file does not exist or cannot be parsed, exit with a clear error message and a non-zero exit code.
15. If the output file already exists, overwrite it without prompting.

## Python Topics Covered

- File I/O: reading and parsing JSON and JSONL formats
- `argparse` for CLI argument handling
- Error handling with try/except for both file and API errors
- Basic timing using `time` module
- Writing structured data to JSON output files
- Control flow: processing a list sequentially with per-item error handling

## AI Topics Covered

- Prompt variation and experimentation
- Observing how different prompt phrasings affect LLM responses
- Latency measurement per LLM call
- Systematic prompt comparison as a foundation for evaluation

## Acceptance Criteria

- [ ] Script reads a valid prompts file and sends each prompt to the LLM.
- [ ] Results file is written with all required fields per entry.
- [ ] Latency is measured and recorded for each call.
- [ ] If one prompt fails, the script continues processing remaining prompts.
- [ ] Summary is printed to stdout on completion.
- [ ] Both `.json` and `.jsonl` input formats are supported.
- [ ] Invalid or missing input file exits with a non-zero code and a clear error message.
- [ ] Tests cover: loading prompts, writing results, latency recording, and error handling for a failed API call.
