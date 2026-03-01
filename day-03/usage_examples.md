# Day 3 – Usage Examples

## How to Run

Analyse sentiment of a text:

```bash
python src/main.py --task sentiment --input "I absolutely love this product!"
# Output (example):
# {
#   "sentiment": "positive",
#   "confidence": 0.97,
#   "reasoning": "The phrase 'absolutely love' is a strong positive expression."
# }
```

Extract key facts from a text:

```bash
python src/main.py --task facts --input "The Eiffel Tower is in Paris. It was built in 1889."
# Output (example):
# {
#   "facts": [
#     "The Eiffel Tower is located in Paris.",
#     "The Eiffel Tower was built in 1889."
#   ],
#   "source_topic": "Eiffel Tower"
# }
```

Invalid or malformed LLM response — exits with code 1:

```bash
# If the LLM returns non-JSON or a schema-mismatched response, the CLI prints:
# Error: <description of JSONDecodeError or ValidationError>
```

---

## How to Run Tests

Run all tests:

```bash
pytest tests/ -v
```

Run only model validation tests:

```bash
pytest tests/test_models.py -v
```

Run only client parsing tests:

```bash
pytest tests/test_client.py -v
```

Run only CLI routing tests:

```bash
pytest tests/test_main.py -v
```

Run tests matching error-handling scenarios:

```bash
pytest tests/ -v -k "invalid or error or malformed or missing"
```
