# Day 14 – Memory Buffer for Chat

## Goal

Build a stateful chat session that maintains a rolling conversation history (memory buffer) across multiple turns, injecting prior context into each new LLM request.

## What We Should Build

A CLI-based multi-turn chat application that:

- Accepts user messages interactively in a loop
- Appends each user message and assistant reply to an in-memory buffer
- Injects the full conversation history into each subsequent LLM request
- Limits the buffer to a configurable maximum number of turns to prevent context overflow
- Supports a command to clear the memory buffer and restart the conversation

## Functional Requirements

### 1. Memory Buffer

- Maintain a list of message objects, each with a `role` (`user` or `assistant`) and `content` field
- Append every user message and every assistant reply to the buffer after each turn
- The buffer must preserve insertion order

### 2. Turn Limit (Sliding Window)

- Accept a `--max-turns` CLI argument (default: 10)
- When the buffer exceeds `max-turns` pairs (user + assistant), drop the oldest pair from the front
- The system prompt, if present, must never be dropped from the buffer

### 3. System Prompt

- Accept an optional `--system` CLI argument that sets a system-level instruction
- The system prompt must be prepended to every LLM request as a `system` role message (or equivalent header)
- It must not count toward the turn limit

### 4. Interactive Chat Loop

- Display a `You:` prompt and read input from stdin
- After receiving the LLM reply, print it prefixed with `Assistant:`
- Continue the loop until the user types `exit` or `quit`

### 5. Memory Reset Command

- If the user types `/clear`, reset the buffer to empty (keeping the system prompt if set)
- Print a confirmation message: `[Memory cleared]`

### 6. Buffer Inspection Command

- If the user types `/history`, print all messages currently in the buffer in order
- Format: `[role]: content` for each message

### 7. LLM Integration

- Send the full current buffer (including system prompt) to the LLM on every turn
- Use the same `LLMClient` pattern established in earlier days (httpx-based)
- The model and API base URL must be configurable via environment variables or constants

### 8. Graceful Exit

- On `exit` or `quit`, print `Goodbye.` and terminate cleanly
- Handle `KeyboardInterrupt` (Ctrl+C) gracefully with the same message

## Python Topics Covered

- State management with mutable data structures (list of dicts)
- Sliding window / deque trimming logic
- Interactive stdin loop
- argparse for CLI arguments
- Clean control flow with command dispatch

## AI Topics Covered

- Conversation memory basics
- Multi-turn context injection
- System prompt role
- Context window management (sliding window strategy)
- Stateful vs. stateless LLM interactions

## Acceptance Criteria

- [ ] Sending multiple messages in sequence results in contextually aware replies (the LLM references prior turns)
- [ ] Setting `--max-turns 2` causes the oldest turn pair to be dropped once the limit is exceeded
- [ ] `/clear` resets the buffer; the next reply has no prior context
- [ ] `/history` prints all buffered messages in order with correct roles
- [ ] `--system "You are a pirate"` causes the assistant to maintain that persona across all turns
- [ ] `exit` / `quit` / Ctrl+C all terminate cleanly with `Goodbye.`
- [ ] Tests cover: buffer append, sliding window trim, `/clear`, `/history`, system prompt preservation
