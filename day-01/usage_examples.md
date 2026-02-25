# Day 1 – Usage Examples

## How to Run

Send a prompt to the Claude API and print the response:

```bash
python src/main.py "What is a large language model?"
# Output:
# A large language model (LLM) is a type of AI...
# Input tokens: 12 | Output tokens: 87
```

Try different prompts:

```bash
python src/main.py "Explain recursion in one sentence."

python src/main.py "What is the difference between a list and a tuple in Python?"
```

Missing API key — exits with a clear error before any network call:

```bash
# With ANTHROPIC_API_KEY unset:
python src/main.py "Hello"
# Error: ANTHROPIC_API_KEY is not set.
```

---

## How to Run Tests

```bash
pytest tests/ -v
```

Run only error-handling tests:

```bash
pytest tests/ -v -k "error or missing"
```
