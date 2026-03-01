# Day 2 – Usage Examples

## How to Run

Render the `translate` template:

```bash
python src/main.py --template translate --var text="Good morning" --var language="French"
# Output: Translate the following text into French:
#
# Good morning
```

Render the `summarise` template:

```bash
python src/main.py --template summarise --var text="Long article..." --var num_sentences="3"
# Output: Summarise the following text in 3 sentences:
#
# Long article...
```

Render the `qa` template:

```bash
python src/main.py --template qa --var question="What is RAG?" --var context="RAG stands for Retrieval-Augmented Generation."
# Output: Context:
# RAG stands for Retrieval-Augmented Generation.
#
# Question: What is RAG?
#
# Answer:
```

Missing variable — exits with code 1:

```bash
python src/main.py --template translate --var text="Hello"
# Error: Missing variables: language
```

Extra variable — exits with code 1:

```bash
python src/main.py --template translate --var text="Hello" --var language="French" --var extra="oops"
# Error: Unknown variables: extra
```

Unknown template — exits with code 1:

```bash
python src/main.py --template nonexistent
# Error: Template 'nonexistent' not found
```

---

## How to Run Tests

Run all tests:

```bash
pytest tests/ -v
```

Run a specific test file:

```bash
pytest tests/test_template.py -v
pytest tests/test_library.py -v
pytest tests/test_templates.py -v
pytest tests/test_main.py -v
```

Run only error-handling tests:

```bash
pytest tests/ -v -k "missing or extra or error"
```
