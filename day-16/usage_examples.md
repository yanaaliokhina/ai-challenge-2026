# Day 16 – Usage Examples

## How to Run

Ask the LLM to pick and run a tool based on your prompt:

```bash
python src/main.py --prompt "What time is it right now?"
# Tool:      get_current_datetime
# Arguments: {}
# Result:    2026-05-26 14:32:01

python src/main.py --prompt "How many words are in 'the quick brown fox'?"
# Tool:      word_count
# Arguments: {"text": "the quick brown fox"}
# Result:    4

python src/main.py --prompt "Convert 37 degrees Celsius to Fahrenheit"
# Tool:      celsius_to_fahrenheit
# Arguments: {"celsius": 37}
# Result:    98.6

python src/main.py --prompt "What time is it?" --verbose
# INFO: Prompt: What time is it?
# Tool:      get_current_datetime
# Arguments: {}
# Result:    2026-05-26 14:32:01
```

## How to Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run only registry logic tests
pytest tests/test_tool_registry.py -v

# Run only built-in tool tests
pytest tests/test_tools.py -v

# Run only LLM integration flow tests (no real API calls)
pytest tests/test_main.py -v
```
