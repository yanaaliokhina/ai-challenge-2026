# Day 16 – Tool Registry Pattern

## Goal

Build a tool registry system that allows an LLM agent to discover and invoke named tools dynamically. This challenge introduces the core mechanism behind tool-calling in AI agents.

## What We Should Build

A Python module that:
- Allows functions to be registered as "tools" using a decorator
- Stores tool metadata (name, description, parameters) in a registry
- Accepts a tool invocation request (name + arguments) and dispatches it to the correct function
- Integrates with an LLM to let the model choose which tool to call based on a user prompt

## Functional Requirements

### 1. Tool Registration

- Implement a `@tool` decorator that registers a function into a global tool registry
- Each registered tool must store:
  - `name`: the function name (or an explicitly provided name)
  - `description`: a human-readable description of what the tool does
  - `parameters`: a dictionary describing expected input arguments (name, type, description)
- The registry must be accessible as a dictionary keyed by tool name

### 2. Tool Discovery

- Provide a function `list_tools()` that returns a list of all registered tools with their metadata
- The list must be serializable to JSON so it can be passed to an LLM as context

### 3. Tool Dispatch

- Implement a `call_tool(name: str, arguments: dict) -> str` function that:
  - Looks up the tool by name in the registry
  - Validates that all required arguments are present
  - Calls the function with the provided arguments
  - Returns the result as a string

### 4. LLM Integration

- Send the user prompt along with the list of available tools to the LLM
- Ask the LLM to respond with a structured tool call: tool name and arguments
- Parse the LLM response as JSON to extract `tool_name` and `arguments`
- Dispatch the call using `call_tool()` and return the result

### 5. Built-in Demo Tools

Register at least three example tools:
- A tool that returns the current date and time
- A tool that calculates the word count of a given text
- A tool that converts a temperature from Celsius to Fahrenheit

### 6. CLI Entry Point

- Accept a user prompt via `--prompt` flag
- Print the selected tool name, arguments, and the tool result to stdout

## Python Topics Covered

- Decorators and function metadata
- Dictionary-based registries
- Dynamic function dispatch
- JSON serialization
- Argument parsing with argparse

## AI Topics Covered

- Tool-calling mechanism
- Structured LLM output for tool selection
- Agent tool discovery pattern
- Prompt construction with tool context

## Acceptance Criteria

- Decorated functions appear in the registry with correct metadata
- `list_tools()` returns all registered tools in a JSON-serializable format
- `call_tool()` correctly dispatches to the right function and returns a string result
- `call_tool()` raises a descriptive error when an unknown tool name is provided
- `call_tool()` raises a descriptive error when required arguments are missing
- The LLM selects the correct tool based on the user prompt
- The CLI prints tool name, arguments, and result
- All behavior is covered by unit tests (no real LLM calls in tests)
