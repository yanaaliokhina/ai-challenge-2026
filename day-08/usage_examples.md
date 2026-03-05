# Day 8 – Usage Examples

## How to Run

### Embed a single text string

```bash
python src/main.py --text "The quick brown fox jumps over the lazy dog"
```

Expected output:
```
Inputs processed : 1
Model            : voyage-3-lite
Embedding dim    : 512
[0] preview      : [0.0123, -0.0456, 0.0789, -0.0321, 0.0654, ...]
```

### Embed multiple texts from a file

```bash
python src/main.py --file inputs.txt
```

Where `inputs.txt` contains one text per line:
```
The sky is blue.
Cats are independent animals.
Python is a great programming language.
```

Expected output:
```
Inputs processed : 3
Model            : voyage-3-lite
Embedding dim    : 512
[0] preview      : [0.0123, -0.0456, ...]
[1] preview      : [-0.0234, 0.0567, ...]
[2] preview      : [0.0345, -0.0678, ...]
```

### Save full embeddings to a JSON file

```bash
python src/main.py --text "Hello world" --output embeddings.json
```

Resulting `embeddings.json` structure:
```json
[
  {
    "text": "Hello world",
    "model": "voyage-3-lite",
    "embedding": [0.0123, -0.0456, 0.0789, ...]
  }
]
```

### Use a different model

```bash
python src/main.py --text "Sample text" --model voyage-3
```

### Error cases

Missing input flag:
```bash
python src/main.py
# Error: provide exactly one of --text or --file
```

Non-existent file:
```bash
python src/main.py --file missing.txt
# Error: file 'missing.txt' not found
```

## How to Run Tests

```bash
pytest tests/ -v
```

Run only the embedding client tests:
```bash
pytest tests/test_embedding_client.py -v
```

Run only the main helper function tests:
```bash
pytest tests/test_main.py -v
```

Test the output file structure specifically:
```bash
pytest tests/test_main.py::test_save_results_json_structure -v
```

All tests use mocks — no live API call is required.
