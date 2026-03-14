# Day 15 – Basic Agent Loop

## Goal

Build a simple AI agent that operates in a reasoning loop: it receives a task, decides what to do next (reason or use a tool), executes the action, observes the result, and repeats until it produces a final answer.

## What We Should Build

A command-line agent that accepts a natural language task and runs a loop where the LLM reasons about what to do next. The agent supports a small set of built-in tools (e.g., calculator, string utility), calls them when the LLM decides to, and feeds results back into the loop until the LLM signals it is done.

## Functional Requirements

### 1. Agent Loop

- The agent runs a loop with a configurable maximum number of iterations (default: 10).
- Each iteration the agent sends the current task and accumulated context to the LLM.
- The loop terminates when:
  - The LLM returns a final answer (no tool call needed), or
  - The maximum number of iterations is reached.

### 2. LLM Reasoning Step

- Each loop iteration sends a prompt containing:
  - The original task
  - The history of previous thoughts and tool results
- The LLM must respond in one of two structured formats:
  - **Tool call**: specifies a tool name and its arguments
  - **Final answer**: a plain text response to the original task
- The response format must be parsed deterministically (use a structured JSON output schema via Pydantic).

### 3. Built-in Tools

Implement at least three tools the agent can invoke:

| Tool | Description |
|---|---|
| `calculator` | Evaluates a basic arithmetic expression string (e.g. `"3 * (4 + 2)"`) |
| `word_count` | Returns the number of words in a given text string |
| `reverse_string` | Returns the reversed version of a given string |

Each tool must:
- Accept a single string argument
- Return a string result
- Be registered in a tool registry (a plain dict or simple class — no decorators required)

### 4. Tool Execution

- After the LLM returns a tool call, the agent executes the matching tool.
- The tool result is appended to the agent's context as an observation.
- If the LLM calls an unknown tool, the agent records an error observation and continues.

### 5. Output

- The agent prints each reasoning step to stdout:
  - Iteration number
  - LLM thought (tool call or reasoning note)
  - Tool result (if applicable)
- At the end, the agent prints the final answer.
- If the maximum iterations are reached without a final answer, print a timeout message.

### 6. Configuration

- Maximum iterations must be configurable via a CLI flag.
- The task must be passed as a CLI argument.

## Python Topics Covered

- Control flow: loops, conditions, early exit
- Pydantic models for parsing structured LLM responses
- Dictionary-based tool registry
- Exception handling for tool execution errors
- CLI argument parsing

## AI Topics Covered

- Agent reasoning loop (think → act → observe → repeat)
- Structured LLM output for decision-making
- Tool-calling pattern via prompt engineering
- Context accumulation across loop iterations
- Termination conditions for agent loops

## Acceptance Criteria

- [ ] Agent accepts a task via CLI and runs the reasoning loop
- [ ] LLM response is parsed into a Pydantic model with `tool_call` or `final_answer` fields
- [ ] All three tools (`calculator`, `word_count`, `reverse_string`) are implemented and callable
- [ ] Tool results are fed back into the next iteration as observations
- [ ] The loop terminates correctly on final answer or max iterations
- [ ] Each iteration prints the step number, action taken, and result
- [ ] Unknown tool names produce an error observation and the loop continues
- [ ] Tests cover: tool execution, response parsing, loop termination on max iterations
