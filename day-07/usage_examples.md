# Day 7 – Usage Examples

## How to Run

Run the experiment script with a prompts file:

```bash
python src/main.py --prompts-file data/prompts.json
```

Specify a custom output file:

```bash
python src/main.py --prompts-file data/prompts.json --output-file data/results.json
```

Use a JSONL input file:

```bash
python src/main.py --prompts-file data/prompts.jsonl --output-file data/results.json
```

Override the model:

```bash
python src/main.py --prompts-file data/prompts.json --model gpt-4o-mini
```

### Example Input File (`data/prompts.json`)

```json
[
  {
    "id": "v1",
    "label": "Direct question",
    "prompt": "What is the capital of France?"
  },
  {
    "id": "v2",
    "label": "Polite phrasing",
    "prompt": "Could you please tell me the capital of France?"
  },
  {
    "id": "v3",
    "label": "Chain-of-thought nudge",
    "prompt": "Think step by step: what is the capital of France?"
  }
]
```

### Example Input File (`data/prompts.jsonl`)

```
{"id": "v1", "label": "Direct question", "prompt": "What is the capital of France?"}
{"id": "v2", "label": "Polite phrasing", "prompt": "Could you please tell me the capital of France?"}
```

### Example Output File (`results.json`)

```json
[
  {
    "id": "v1",
    "label": "Direct question",
    "prompt": "What is the capital of France?",
    "response": "The capital of France is Paris.",
    "latency_ms": 312,
    "error": null
  },
  {
    "id": "v2",
    "label": "Polite phrasing",
    "prompt": "Could you please tell me the capital of France?",
    "response": "Of course! The capital of France is Paris.",
    "latency_ms": 289,
    "error": null
  }
]
```

### Example stdout Summary

```
Total prompts attempted: 3
Successful responses:    3
Failures:                0
Average latency (ms):    301.0
```

### Error Case – Missing Input File

```bash
python src/main.py --prompts-file data/nonexistent.json
# Error: Input file not found: data/nonexistent.json
# exits with code 1
```

---

## How to Run Tests

Run all tests:

```bash
pytest tests/ -v
```

Run a specific test file:

```bash
pytest tests/test_main.py -v
pytest tests/test_prompt_loader.py -v
pytest tests/test_llm_client.py -v
```

Run only the error-handling tests:

```bash
pytest tests/ -v -k "error or fail"
```

Run tests with printed output (useful for inspecting summaries):

```bash
pytest tests/ -s
```
