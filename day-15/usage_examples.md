# Day 15 – Usage Examples

## How to Run

Run the agent with a task:

```bash
python src/main.py --task "What is 12 * (3 + 7)?"
```

Run with a custom max iterations limit:

```bash
python src/main.py --task "How many words are in 'the quick brown fox'?" --max-iterations 5
```

Run a task requiring string manipulation:

```bash
python src/main.py --task "Reverse the string 'hello world' and tell me the result."
```

### Example Output

```
[Step 1] Thought: I need to reverse the string 'hello world'.
[Step 1] Tool call: reverse_string("hello world")
[Step 1] Observation: "dlrow olleh"

[Step 2] Final answer: The reversed string is "dlrow olleh".
```

### Timeout Example

```bash
python src/main.py --task "Tell me a long story step by step." --max-iterations 3
```

```
[Step 1] ...
[Step 2] ...
[Step 3] ...
Max iterations reached. No final answer produced.
```

## How to Run Tests

Run all tests for day-15:

```bash
pytest tests/ -v
```

Run only tool execution tests:

```bash
pytest tests/test_tools.py -v
```

Run only agent loop tests:

```bash
pytest tests/test_agent.py -v
```

Run response parsing tests:

```bash
pytest tests/test_agent.py -v -k "parse"
```

Run with stdout output visible (useful for debugging loop steps):

```bash
pytest tests/ -s
```
