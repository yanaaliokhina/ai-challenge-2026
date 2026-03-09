# Day 12 – Usage Examples

## How to Run

### Index a text file
```bash
python src/main.py --file data/sample.txt
```

### Index a file and specify a custom index path
```bash
python src/main.py --file data/sample.txt --index my_index.json
```

### Query the index
```bash
python src/main.py --query "What is retrieval-augmented generation?"
```

### Query with custom top-N results
```bash
python src/main.py --query "How do embeddings work?" --top-n 5
```

### Index and query in one command
```bash
python src/main.py --file data/sample.txt --query "What is the main topic?" --top-n 3
```

### Re-run indexing on the same file (deduplication check)
```bash
python src/main.py --file data/sample.txt
# Expected: no new chunks added, index size unchanged
```

### Example output (query mode)
```
Top 3 results:
[1] Score: 0.9312 | "Embeddings represent text as dense vectors in high-dimensional space..."
[2] Score: 0.8874 | "Retrieval-Augmented Generation combines a retrieval step with generation..."
[3] Score: 0.8541 | "Cosine similarity measures the angle between two vectors..."
```

## How to Run Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run a specific test file
```bash
pytest tests/test_index.py -v
```

### Run only deduplication tests
```bash
pytest tests/test_index.py -v -k "dedup"
```

### Run only query/similarity tests
```bash
pytest tests/test_index.py -v -k "query or similarity"
```

### Run tests without making real API calls (using mocked embeddings)
```bash
pytest tests/ -v -k "not integration"
```
