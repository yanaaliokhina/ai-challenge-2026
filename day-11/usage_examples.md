# Day 11 – Usage Examples

## Sample Input File

`data/sample.txt` is a plain-text summary of the "Attention Is All You Need" paper (Vaswani et al., 2017). It covers:

- The paper's main contribution: the transformer architecture
- Key contributors and their affiliations
- Methods: scaled dot-product attention, multi-head attention, positional encoding
- Evaluation results on WMT 2014 translation benchmarks
- Conclusions about attention-only models vs. recurrent and convolutional approaches

Use it to test all example commands below.

## How to Run

### Basic usage with a plain text file

```bash
python src/main.py --file data/sample.txt --query "What is the main topic of this document?"
```

### Query a Markdown file

```bash
python src/main.py --file data/notes.md --query "What conclusions are described in this document?"
```

### Set a custom token budget

```bash
python src/main.py --file data/sample.txt --query "Who are the key contributors?" --max-tokens 1500
```

### Verbose mode (shows token count and truncation status)

```bash
python src/main.py --file data/sample.txt --query "Summarize the methods described." --verbose
```

### Expected output (non-verbose)

```
Based on the document, the main topic is...
```

### Expected output (verbose)

```
Estimated tokens: 412
Truncated: no

Based on the document, the main topic is...
```

### Expected output when document exceeds token budget

```
Warning: document exceeds token budget (estimated 4100 tokens > max 3000). Truncating.
Estimated tokens: 4100
Truncated: yes

Based on the provided context...
```

### Unsupported file type error

```bash
python src/main.py --file data/report.pdf --query "What is this about?"
```

```
Error: unsupported file type '.pdf'. Only .txt and .md are supported.
```

## How to Run Tests

### Run all tests

```bash
pytest tests/ -v
```

### Run only Markdown stripping tests

```bash
pytest tests/test_parser.py -v
```

### Run only token estimation and truncation tests

```bash
pytest tests/test_token_budget.py -v
```

### Run only prompt construction tests

```bash
pytest tests/test_prompt.py -v
```
