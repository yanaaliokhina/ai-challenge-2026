# Day 4 – Usage Examples

## How to Run

### Send multiple prompts as CLI arguments

```bash
python src/main.py "What is the capital of France?" "Name three planets." "What is 2 + 2?"
```

Expected output:
```
[1] Prompt: What is the capital of France?
    Status: OK
    Response: The capital of France is Paris.

[2] Prompt: Name three planets.
    Status: OK
    Response: Mercury, Venus, Earth.

[3] Prompt: What is 2 + 2?
    Status: OK
    Response: 2 + 2 equals 4.

Total time: 1.42s
```

---

### Send prompts from a file

Create a file `prompts.txt`:
```
What is the capital of Japan?
Explain gravity in one sentence.
What color is the sky?
```

Run:
```bash
python src/main.py --file prompts.txt
```

---

### Single prompt (edge case)

```bash
python src/main.py "Summarize the water cycle in one sentence."
```

---

### Empty input (error case)

```bash
python src/main.py
```

Expected output (stderr):
```
Error: no prompts provided.
```

---

## How to Run Tests

```bash
pytest tests/ -v
```

### Run only concurrency tests

```bash
pytest tests/test_main.py -v -k "concurrent"
```

### Run only error handling tests

```bash
pytest tests/test_main.py -v -k "error"
```

### Run with printed output (useful for debugging async behavior)

```bash
pytest tests/ -s
```
