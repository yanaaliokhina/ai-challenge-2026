# Day 10 – Usage Examples

## Sample Input File

`data/sample.txt` is a short article about Retrieval-Augmented Generation (RAG). It covers:

- What RAG is and how it works
- Key contributors and the original paper (Lewis et al., 2020)
- Retrieval methods (DPR, FAISS, cosine similarity)
- Chunking strategies and evaluation metrics
- Practical embedding APIs and future research directions

Use it to test all example commands below.

## How to Run

### Basic usage

```bash
python src/main.py --file data/sample.txt --query "What is the main topic of this document?"
```

### Custom chunk size and overlap

```bash
python src/main.py --file data/sample.txt --query "Who are the key contributors?" --chunk-size 80 --overlap 15
```

### Change number of retrieved chunks

```bash
python src/main.py --file data/sample.txt --query "Summarize the conclusions." --top-k 5
```

### Verbose mode (shows retrieved chunks and similarity scores)

```bash
python src/main.py --file data/sample.txt --query "What methods were used?" --verbose
```

### Expected output (non-verbose)

```
Based on the provided context, the main topic of the document is...
```

### Expected output (verbose)

```
Retrieved chunks:
  [chunk 2] similarity=0.874 — "...text of the chunk..."
  [chunk 5] similarity=0.821 — "...text of the chunk..."
  [chunk 1] similarity=0.799 — "...text of the chunk..."

Answer:
Based on the provided context, the main topic of the document is...
```

## How to Run Tests

### Run all tests

```bash
pytest tests/ -v
```

### Run only chunking tests

```bash
pytest tests/test_chunker.py -v
```

### Run only retrieval tests

```bash
pytest tests/test_retriever.py -v
```

### Run only embedder tests

```bash
pytest tests/test_embedder.py -v
```

### Run only prompt construction tests

```bash
pytest tests/test_prompt.py -v
```
