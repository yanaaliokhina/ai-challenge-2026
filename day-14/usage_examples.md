# Day 14 – Usage Examples

## How to Run

Start an interactive chat session with default settings (10-turn memory):

```bash
python src/main.py
```

Start with a custom system prompt:

```bash
python src/main.py --system "You are a concise technical assistant."
```

Start with a reduced memory window (keep only the last 3 turn pairs):

```bash
python src/main.py --max-turns 3
```

Combine both options:

```bash
python src/main.py --system "You are a helpful cooking guide." --max-turns 5
```

### Example Session

```
You: What is the capital of France?
Assistant: The capital of France is Paris.

You: And what is it known for?
Assistant: Paris is known for the Eiffel Tower, world-class cuisine, fashion, and art museums like the Louvre.

You: /history
[user]: What is the capital of France?
[assistant]: The capital of France is Paris.
[user]: And what is it known for?
[assistant]: Paris is known for the Eiffel Tower, world-class cuisine, fashion, and art museums like the Louvre.

You: /clear
[Memory cleared]

You: What did I ask you before?
Assistant: I don't have any record of previous messages. How can I help you?

You: exit
Goodbye.
```

## How to Run Tests

Run all tests for this challenge:

```bash
pytest tests/ -v
```

Run only the buffer logic tests:

```bash
pytest tests/test_memory_buffer.py -v
```

Run only the sliding window trim tests:

```bash
pytest tests/test_memory_buffer.py -v -k "trim or window or max_turns"
```

Run with stdout captured (useful for command dispatch tests):

```bash
pytest tests/ -v -s
```
