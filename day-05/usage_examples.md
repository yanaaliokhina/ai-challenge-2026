# Day 5 – Usage Examples

## How to Run

### Single-shot mode

Send a single prompt and print the response:

```bash
python src/main.py --prompt "What is the capital of France?"
```

Expected output (example):
```
The capital of France is Paris.
```

---

### Single-shot with a system prompt

```bash
python src/main.py --prompt "Introduce yourself" --system "You are a friendly pirate assistant"
```

Expected output (example):
```
Ahoy! I be yer friendly pirate assistant, ready to sail the seas of knowledge with ye!
```

---

### Single-shot with verbose output

```bash
python src/main.py --prompt "Hello" --verbose
```

Expected stderr output (before the response):
```
[verbose] Model: claude-haiku-4-5-20251001
[verbose] System: (none)
[verbose] Prompt: Hello
```

Expected stdout output:
```
Hello! How can I assist you today?
```

---

### Single-shot with a custom model

```bash
python src/main.py --prompt "Tell me a joke" --model claude-haiku-4-5-20251001
```

---

### Interactive mode

Launch a REPL session:

```bash
python src/main.py --interactive
```

Example session:
```
You: What is Python?
Assistant: Python is a high-level, interpreted programming language known for its clear syntax...

You: Tell me one fun fact about it
Assistant: A fun fact about Python: it was named after Monty Python's Flying Circus, not the snake!

You: exit
```

---

### Interactive mode with a system prompt

```bash
python src/main.py --interactive --system "You are a Socratic tutor. Answer every question with a question."
```

---

### Mutually exclusive flag error

```bash
python src/main.py --prompt "Hello" --interactive
```

Expected output:
```
error: argument --interactive/-i: not allowed with argument --prompt
```
Exits with a non-zero exit code.

---

### Missing mode error

```bash
python src/main.py --verbose
```

Expected output:
```
error: one of the arguments --prompt --interactive/-i is required
```
Exits with a non-zero exit code.

---

## How to Run Tests

Run all tests for Day 5:

```bash
pytest tests/ -v
```

Run only the LLM client tests:

```bash
pytest tests/test_llm_client.py -v
```

Run only the CLI parser tests:

```bash
pytest tests/test_cli_parser.py -v
```

Run only the orchestration (main) tests:

```bash
pytest tests/test_main.py -v
```

Run tests with stdout captured (useful for inspecting printed output):

```bash
pytest tests/ -v -s
```

> Tests use `unittest.mock` to patch `httpx` calls and `monkeypatch` to simulate stdin — no real API calls or user input required.
