# Day 6 – Usage Examples

## How to Run

### Count tokens for inline text (default model: gpt-4o)
```bash
python src/main.py --text "Hello, world! This is a token counter test."
```

Expected output:
```
Source:         argument
Model:          gpt-4o
Tokens:         11
Context window: 128000
Usage:          0.01%
Status:         FITS
```

### Count tokens for a file
```bash
python src/main.py --file data/sample.txt
```

### Count tokens using a specific model
```bash
python src/main.py --text "Summarize this article for me." --model gpt-4
```

### Count tokens from stdin
```bash
echo "What is the capital of France?" | python src/main.py
```

```bash
cat data/long_document.txt | python src/main.py --model claude-3-5-sonnet
```

### Verbose mode — show individual tokens and remaining budget
```bash
python src/main.py --text "Hello world" --verbose
```

Expected output (in addition to standard output):
```
Tokens (decoded): ['Hello', ' world']
Remaining budget: 127998 tokens
```

### Batch mode — count tokens per line from a file
```bash
python src/main.py --batch data/prompts.txt --model gpt-4o
```

Expected output format:
```
Line 1:  8 tokens  [FITS]
Line 2:  23 tokens [FITS]
Line 3:  312 tokens [FITS]
---
Summary:
  Total lines:   3
  Total tokens:  343
  Min tokens:    8
  Max tokens:    312
  Avg tokens:    114.33
```

### Unsupported model — triggers a clean error
```bash
python src/main.py --text "Hello" --model gpt-5-ultra
```

Expected output:
```
Error: Unsupported model 'gpt-5-ultra'.
Supported models: gpt-4o, gpt-4, gpt-3.5-turbo, claude-3-haiku, claude-3-5-sonnet
```
Exit code: 1

### Conflicting input flags — triggers an error
```bash
python src/main.py --text "Hello" --file data/sample.txt
```

Expected output:
```
Error: Provide either --text or --file, not both.
```
Exit code: 1

---

## How to Run Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run only token counting logic tests
```bash
pytest tests/test_counter.py -v
```

### Run only CLI argument parsing tests
```bash
pytest tests/test_cli.py -v
```

### Run batch mode tests
```bash
pytest tests/ -v -k "batch"
```

### Run with printed output for debugging
```bash
pytest tests/ -s
```
