# Coding Challenges: Day 16 – Day 30

---

## Day 16 – ReAct Agent Loop

### Goal
Implement a ReAct (Reason + Act) agent loop from scratch. The agent reasons about
a task, decides which tool to call, calls it, observes the result, and repeats
until it reaches a final answer — all driven by LLM output parsing.

### What to Build
- A `Thought` dataclass: `reasoning`, `action`, `action_input`, `is_final`
- A `StepResult` dataclass: `thought`, `observation`, `step_number`
- A `ReActAgent` class with a `run(task) -> str` method that loops: think → act → observe → repeat
- A `_parse_llm_output(text) -> Thought` method that extracts `Thought:`, `Action:`, `Action Input:`, `Final Answer:` from LLM text
- A `_build_prompt(task, history) -> str` method assembling the ReAct-style prompt with tool descriptions and step history
- Integration with the `ToolRegistry` from Day 15 for tool lookup and calling
- A max steps limit to prevent infinite loops
- Tests: parse valid LLM output, parse final answer, max steps triggers stop, tool called correctly

### Python Skill Focus
- **State machine** — loop state: thinking, acting, observing, done
- **Regex parsing** — extracting structured data from freeform LLM text
- **Dataclasses** — `Thought`, `StepResult` as typed step records
- **Error handling** — malformed LLM output, unknown tool names, tool call failures
- **Type hints** — `list[StepResult]`, `Literal["thinking", "done"]`

### AI Concept Focus
- **ReAct loop** — Reason + Act: LLM alternates between reasoning steps and tool actions
- **Prompt scaffolding** — the ReAct prompt format: task + tool list + previous steps
- **Observation feeding** — tool results are fed back into the prompt as observations
- **Stop conditions** — `Final Answer:` token, max steps, or tool error terminates the loop

---

## Day 17 – Multi-Tool Agent

### Goal
Build an agent that selects and calls tools using structured JSON tool schemas —
the same pattern used by OpenAI function calling and Anthropic tool use.
The LLM returns a JSON object specifying which tool to call and with what arguments.

### What to Build
- A `ToolCall` dataclass: `tool_name`, `arguments: dict[str, Any]`, `call_id`
- A `ToolResult` dataclass: `call_id`, `tool_name`, `result`, `error`
- A `ToolCallingAgent` class that: builds a prompt with tool schemas, parses LLM JSON output into `ToolCall`, dispatches to the registry, returns `ToolResult`
- A `_build_tool_prompt(task, tools) -> str` method that formats tool schemas as JSON in the prompt
- A `_parse_tool_call(llm_output) -> ToolCall | None` method that extracts the JSON tool call
- At least 3 registered tools: `search_web` (stub), `calculate`, `get_weather` (stub)
- Tests: parse valid tool call JSON, unknown tool returns error result, argument mismatch handled

### Python Skill Focus
- **JSON parsing** — `json.loads` on LLM output, with defensive error handling
- **`dataclasses`** — `ToolCall`, `ToolResult` with `dict[str, Any]` fields
- **`TypedDict`** — optionally type tool argument schemas
- **Dispatch pattern** — `registry.call(name, **arguments)` as the execution layer
- **`uuid`** — generating `call_id` for correlating calls and results

### AI Concept Focus
- **Structured tool calling** — LLM outputs JSON specifying tool name + arguments
- **Tool schemas** — JSON schema descriptions that constrain what arguments the LLM can pass
- **Function calling pattern** — how OpenAI and Anthropic native tool use works under the hood
- **Tool result injection** — feeding tool output back into the next LLM prompt turn

---

## Day 18 – Sub-Agent Delegator

### Goal
Build a delegator that routes tasks to specialized sub-agents based on task type.
The main agent classifies the incoming task and hands it off to the right sub-agent:
summarizer, coder, or researcher.

### What to Build
- A `SubAgentTask` dataclass: `task_id`, `task_type`, `input`, `assigned_to`
- A `SubAgentResult` dataclass: `task_id`, `output`, `agent_name`, `success`
- A `BaseSubAgent` abstract class with `name`, `description`, `can_handle(task) -> bool`, `run(task) -> SubAgentResult`
- Three concrete sub-agents: `SummarizerAgent`, `CoderAgent`, `ResearcherAgent` — each with a specialized system prompt
- A `Delegator` class with a `register(agent)` method and a `delegate(input) -> SubAgentResult` method that: classifies the task via LLM, finds the right sub-agent, runs it
- A fallback if no sub-agent matches
- Tests: delegator routes to correct agent, fallback triggered for unknown type, sub-agent result structure correct

### Python Skill Focus
- **Abstract base class** — `BaseSubAgent` with `ABC` and `@abstractmethod`
- **Delegation pattern** — orchestrator owns routing; sub-agents own execution
- **Dataclasses** — typed task and result objects flowing between components
- **`list` of registered agents** — linear scan with `can_handle()` for routing
- **Type hints** — `list[BaseSubAgent]`, `SubAgentResult`

### AI Concept Focus
- **Sub-agent delegation** — one agent classifies and routes; specialists execute
- **Specialized system prompts** — each sub-agent has a system prompt tuned for its task type
- **Task classification** — using LLM to categorize user input before routing
- **Orchestration pattern** — coordinator + specialist agents without complex frameworks

---

## Day 19 – Async Agent Task Queue

### Goal
Process multiple agent tasks concurrently using `asyncio.Queue`.
A producer adds tasks to the queue; multiple worker coroutines consume and process them.
Collect all results when the queue is drained.

### What to Build
- A `QueuedTask` dataclass: `task_id`, `prompt`, `priority`, `created_at`
- A `TaskWorker` class with an async `process(task) -> AgentResult` method (calls LLM)
- An `AgentTaskQueue` class with: async `enqueue(task)`, async `run(num_workers) -> list[AgentResult]`, internal `asyncio.Queue`
- A `main.py` that enqueues 8 tasks, runs with 3 workers, prints results and total time
- Tests: all tasks processed, worker count respected, results collected correctly

### Python Skill Focus
- **`asyncio.Queue`** — producer/consumer pattern with `put` and `get`
- **`asyncio.gather`** — running multiple worker coroutines concurrently
- **Worker pool** — N workers draining a shared queue
- **`asyncio.wait_for`** — optional timeout per task
- **Dataclasses** — `QueuedTask`, `AgentResult` with `created_at` timestamps

### AI Concept Focus
- **Async agent execution** — processing many LLM requests without blocking
- **Task queue pattern** — decoupling task submission from task execution
- **Worker pool for LLMs** — limiting concurrent API calls while maximizing throughput
- **Result collection** — gathering all async results after queue is drained

---

## Day 20 – Agent Session Logger

### Goal
Build a context manager that logs every action an agent takes — tool calls,
LLM responses, errors, and timing — to a structured JSON log file.
The session starts on `__enter__` and flushes the log on `__exit__`.

### What to Build
- An `AgentEvent` dataclass: `event_type`, `timestamp`, `data: dict`, `elapsed_ms`
- An `AgentSessionLogger` context manager class with `__enter__` / `__exit__`
- Methods: `log_llm_call(prompt, response, tokens)`, `log_tool_call(name, args, result)`, `log_error(error)`
- On `__exit__`, write a JSON session file: `session_{timestamp}.json` with all events and a summary
- A `summary` property returning total events, total tokens, total errors, total elapsed time
- A `main.py` simulating a 5-step agent session and inspecting the output file
- Tests: events recorded, file written on exit, summary counts correct, context manager cleans up on exception

### Python Skill Focus
- **Context managers** — `__enter__` / `__exit__`, `contextlib.contextmanager`
- **`dataclasses`** — `AgentEvent` with auto timestamps
- **JSON file writing** — `json.dumps(list_of_dicts, indent=2)` to structured log file
- **`datetime.utcnow().isoformat()`** — ISO 8601 timestamps
- **Exception propagation** — `__exit__` receives `exc_type, exc_val, exc_tb`; still flush log

### AI Concept Focus
- **Agent observability** — logging every LLM call and tool use for debugging and auditing
- **Session-level tracking** — grouping events into a named session with a summary
- **Structured event logs** — JSON logs are queryable; plain text logs are not
- **Cost and token tracking** — accumulating token usage across all calls in a session

---

## Day 21 – CLI Chatbot with Tools

### Goal
Build an interactive command-line chatbot that uses conversation memory, a tool registry,
and an LLM backend. The chatbot runs a REPL loop: read input, check for tool triggers,
call LLM with history, print response, repeat.

### What to Build
- A `ChatSession` dataclass holding `ConversationMemory` and `ToolRegistry`
- A `ChatBot` class with a `chat(user_input) -> str` method that: adds message to memory, detects tool commands (`/tool <name> <args>`), calls LLM with full history, returns response
- A Typer CLI with a `run` command that starts the REPL loop and a `--model` option
- Special commands: `/tools` lists available tools, `/clear` resets memory, `/quit` exits
- Integration of at least 2 real tools: `calculator`, `word_count`
- A `main.py` entry point
- Tests: chat adds to memory, tool command dispatched, clear resets session, unknown tool handled

### Python Skill Focus
- **REPL pattern** — `while True: input → process → output → repeat`
- **Typer** — CLI entry point with options and a `run` command
- **Composing classes** — `ChatBot` owns `ConversationMemory` + `ToolRegistry`
- **String parsing** — detecting `/command arg` patterns in user input
- **`sys.exit` / `raise typer.Exit`** — clean shutdown on `/quit`

### AI Concept Focus
- **Chatbot with tools** — blending conversation memory with tool execution in one interface
- **Command routing** — user types `/tool calculator add 5 3` to invoke a tool directly
- **Context-aware responses** — LLM sees full conversation history on every turn
- **Tool-augmented chat** — giving the LLM access to tools it can suggest to the user

---

## Day 22 – Output Guardrails Validator

### Goal
Build a guardrails validator that checks LLM outputs against a set of rules before
returning them to the caller. Rules include: length limits, banned phrases, required
format, and an optional LLM-based safety check.

### What to Build
- A `GuardrailResult` dataclass: `passed`, `violations: list[str]`, `original`, `sanitized`
- A `BaseGuardrail` abstract class with `check(text) -> GuardrailResult`
- Concrete guardrails: `LengthGuardrail(min, max)`, `BannedPhrasesGuardrail(phrases)`, `RegexFormatGuardrail(pattern)`, `JsonSchemaGuardrail(schema)`
- A `GuardrailChain` class that runs all registered guardrails and aggregates violations
- A `main.py` that validates 5 example LLM outputs through the chain
- Tests: each guardrail passes/fails independently, chain aggregates violations, sanitized output returned

### Python Skill Focus
- **Abstract base class** — `BaseGuardrail` with `@abstractmethod check()`
- **Chain of responsibility** — `GuardrailChain` runs all guardrails and collects results
- **Regex** — `re.search`, `re.fullmatch` for format validation
- **Dataclasses** — `GuardrailResult` as a typed result object
- **Type hints** — `list[BaseGuardrail]`, `GuardrailResult`

### AI Concept Focus
- **Output guardrails** — validating LLM output before it reaches the user or downstream system
- **Safety layers** — banned phrases, length limits, format checks as a defence-in-depth strategy
- **Schema validation** — ensuring JSON outputs match the expected structure
- **Sanitization** — returning a cleaned version of the output alongside violation details

---

## Day 23 – Prompt A/B Comparison Tool

### Goal
Build a tool that runs two different prompt variants against the same set of inputs,
scores the responses on simple metrics, and produces a comparison report.
Practice structured experiment design without any ML framework.

### What to Build
- A `PromptVariant` dataclass: `name`, `template`, `version`
- An `ExperimentResult` dataclass: `variant_name`, `input`, `output`, `scores: dict[str, float]`, `latency_ms`
- A `PromptExperiment` class with: `add_variant(variant)`, `run(inputs, complete_fn) -> list[ExperimentResult]`, `report() -> str`
- Scoring functions: `score_length(text)`, `score_keyword_presence(text, keywords)`, `score_sentence_count(text)`
- A `main.py` that compares two prompt variants on 3 inputs and prints a side-by-side report
- Tests: results returned for each variant × input, scores are floats 0–1, report contains both variant names

### Python Skill Focus
- **Dataclasses** — `PromptVariant`, `ExperimentResult` as typed experiment records
- **`Callable`** — `complete_fn: Callable[[str], str]` injected for testability
- **`time.perf_counter`** — measuring latency per call
- **List comprehensions** — generating result matrix across variants × inputs
- **String formatting** — building a readable comparison report

### AI Concept Focus
- **Prompt experiments** — systematically comparing prompt variants on the same inputs
- **Scoring without ground truth** — proxy metrics like length, keyword presence, format compliance
- **A/B testing prompts** — the basic workflow: write two variants, run both, compare scores
- **Latency as a metric** — prompt length and complexity affect response time

---

## Day 24 – LLM Evaluation Harness

### Goal
Build an evaluation harness that loads test cases from a JSON file, runs each through
the LLM, scores the response against an expected answer, and outputs a results report
with pass rate and per-case details.

### What to Build
- A `TestCase` dataclass: `id`, `input`, `expected_output`, `tags: list[str]`
- An `EvalResult` dataclass: `test_case`, `actual_output`, `passed`, `score`, `latency_ms`
- An `EvaluationHarness` class with: `load_cases(path) -> list[TestCase]`, `run(cases, complete_fn) -> list[EvalResult]`, `report(results) -> str`
- Scoring functions: `exact_match`, `contains_expected`, `fuzzy_score` (word overlap ratio)
- A sample `test_cases.json` file with 5 test cases
- A `main.py` CLI: `python main.py --cases test_cases.json --scorer contains`
- Tests: load JSON, run with mock LLM, report pass rate, handle missing expected output

### Python Skill Focus
- **JSON file loading** — `json.loads(Path(path).read_text())`
- **Dataclasses** — `TestCase`, `EvalResult` as typed records
- **`Callable` injection** — `complete_fn` and `scorer_fn` both injectable
- **`argparse` or Typer** — CLI flags for `--cases`, `--scorer`, `--output`
- **Aggregate metrics** — pass rate, average score, average latency from a list of results

### AI Concept Focus
- **Evaluation harness** — the standard pattern for testing LLM behaviour against expected outputs
- **Scoring strategies** — exact match (strict), contains (lenient), fuzzy (partial credit)
- **Test case design** — structured input + expected output + tags for filtering
- **Pass rate reporting** — summarising results as % passed, average score, breakdown by tag

---

## Day 25 – Prompt Response Cache

### Goal
Build a caching layer that stores LLM responses keyed by a hash of the prompt.
Avoid re-calling the API for identical prompts. Support TTL expiry and optional
Redis backend alongside the default in-memory backend.

### What to Build
- A `CacheEntry` dataclass: `response`, `created_at`, `ttl_seconds`, `hit_count`, `is_expired` property
- A `BaseCache` abstract class with `get(key)`, `set(key, value, ttl)`, `invalidate(key)`, `clear()`
- An `InMemoryCache(BaseCache)` backed by `dict[str, CacheEntry]`
- An optional `RedisCache(BaseCache)` backed by `redis-py` (skip gracefully if Redis unavailable)
- A `CachedLLMClient` wrapper that: hashes the prompt with `hashlib.sha256`, checks cache before calling API, stores response on miss
- A `cache_stats()` method returning hit count, miss count, hit rate
- Tests: cache hit returns stored value, TTL expiry returns miss, hash is deterministic

### Python Skill Focus
- **`hashlib`** — `hashlib.sha256(text.encode()).hexdigest()` for stable cache keys
- **Abstract base class** — `BaseCache` defining the cache interface
- **`dataclasses`** — `CacheEntry` with `is_expired` computed property using `datetime`
- **Optional dependency** — `try: import redis / except ImportError: pass`
- **Decorator pattern** — optionally wrap `complete()` with cache logic via a decorator

### AI Concept Focus
- **Prompt caching** — identical prompts should hit cache, not the API, to save cost and latency
- **Cache key design** — hashing the full prompt + model + params for a unique, stable key
- **TTL expiry** — cached responses become stale; time-based expiry forces refresh
- **Cache hit rate** — the key metric: what % of calls are served from cache

---

## Day 26 – Latency Measurement Decorator

### Goal
Build a decorator that measures the latency of LLM API calls, collects statistics
over multiple runs, and produces a summary report with P50, P95, and P99 percentiles.

### What to Build
- A `LatencyRecord` dataclass: `function_name`, `elapsed_ms`, `timestamp`, `success`
- A `LatencyCollector` class that stores records and computes: `p50`, `p95`, `p99`, `mean`, `min`, `max`
- A `@measure_latency(collector)` decorator that wraps any function, records elapsed time, handles exceptions
- A `report(collector) -> str` function that formats a readable latency summary table
- A `main.py` that runs a mocked LLM call 20 times with simulated variable latency, then prints the report
- Tests: decorator records latency, failed calls recorded with `success=False`, percentiles calculated correctly

### Python Skill Focus
- **Decorators** — `@measure_latency(collector)` parameterized decorator with `functools.wraps`
- **`time.perf_counter`** — high-resolution timing in milliseconds
- **`statistics` module** — `statistics.median`, `statistics.mean` from stdlib
- **Percentile calculation** — `sorted_values[int(len * 0.95)]` for P95
- **`dataclasses`** — `LatencyRecord` as an immutable measurement record

### AI Concept Focus
- **LLM latency profiling** — measuring real response times to understand API performance
- **P50/P95/P99 percentiles** — why averages lie; tail latency matters for user experience
- **Latency as a model selection signal** — Haiku is faster; Sonnet is slower but smarter
- **Performance measurement** — the foundation of any SLA or cost/latency trade-off analysis

---

## Day 27 – Structured JSON Logger

### Goal
Build a structured logger that outputs every log entry as a JSON object to stdout
and optionally to a rotating log file. Every LLM call, tool use, and error should
produce a parseable, queryable log line.

### What to Build
- A `LogRecord` dataclass: `timestamp`, `level`, `module`, `message`, `extra: dict`
- A `JsonFormatter` class (subclass of `logging.Formatter`) that overrides `format()` to output JSON
- A `get_logger(name, log_file) -> logging.Logger` factory that attaches the `JsonFormatter`
- An `LLMCallLogger` helper with `log_request(model, prompt, tokens)` and `log_response(model, tokens, latency_ms)` methods
- A `main.py` that logs 3 LLM interactions and shows the resulting JSON log lines
- Tests: formatter outputs valid JSON, required fields present, extra fields included, file handler writes to disk

### Python Skill Focus
- **`logging` module** — `Logger`, `Handler`, `Formatter`, `StreamHandler`, `RotatingFileHandler`
- **Custom `Formatter`** — subclass and override `format(record) -> str`
- **`json.dumps`** — serializing log records with `default=str` for non-serializable types
- **`logging.LogRecord` attributes** — `name`, `levelname`, `getMessage()`, `exc_info`
- **`tmp_path`** in tests — verify file handler writes JSON lines to disk

### AI Concept Focus
- **Structured LLM logging** — every API call logged with model, token count, latency, prompt hash
- **JSON logs** — machine-readable logs enable querying, filtering, and dashboards
- **Observability fields** — what every LLM log entry should contain: model, tokens, latency, error
- **Log levels for AI** — DEBUG for full prompts, INFO for summaries, WARNING for retries, ERROR for failures

---

## Day 28 – LLM Test Suite with Mocks

### Goal
Write a thorough pytest test suite for an LLM client and a simple agent,
using `unittest.mock` to mock all API calls. No real tokens spent.
Practice every major pytest feature: fixtures, parametrize, mocking, async tests.

### What to Build
- A simple `LLMClient` class with `complete(prompt) -> str` and `async_complete(prompt) -> str` methods
- A simple `Agent` class that uses `LLMClient` and a `ToolRegistry`
- A test file with at least 12 tests covering:
  - `@pytest.fixture` — shared client, agent, mock response fixtures
  - `@pytest.mark.parametrize` — testing multiple prompts and expected outputs
  - `unittest.mock.patch` — patching `anthropic.Anthropic` and `anthropic.AsyncAnthropic`
  - `MagicMock` and `AsyncMock` — mocking sync and async API calls
  - `pytest.raises` — testing error handling paths
  - `@pytest.mark.asyncio` — testing async methods
  - `side_effect` — simulating retry scenarios with first-fail-then-succeed

### Python Skill Focus
- **`pytest.fixture`** — shared setup with function and module scope
- **`pytest.mark.parametrize`** — data-driven tests without repetition
- **`unittest.mock.patch`** — decorator and context manager forms
- **`MagicMock` vs `AsyncMock`** — knowing which to use for sync vs async code
- **`side_effect` as a list** — `[Exception(...), "success"]` for retry test sequences

### AI Concept Focus
- **Mocking LLM APIs** — never spend tokens in unit tests; always mock the API client
- **Testing agent behaviour** — verifying tool selection, output parsing, error handling without real calls
- **Deterministic test data** — fixed mock responses make tests reproducible
- **Coverage for AI code** — what to test: parsing, error handling, retry logic, not the LLM itself

---

## Day 29 – AI Observability Reporter

### Goal
Build a session metrics collector that tracks tokens used, latency, cost, and errors
across all LLM calls in a session, then generates a formatted summary report.
Practice aggregation and reporting with pure Python data structures.

### What to Build
- A `CallMetrics` dataclass: `model`, `input_tokens`, `output_tokens`, `latency_ms`, `success`, `error_type`, `timestamp`
- A `SessionMetrics` class with: `record(call_metrics)`, `total_tokens`, `total_cost`, `error_rate`, `avg_latency_ms`, `calls_by_model`
- A `MetricsReporter` class with `generate_report(session) -> str` — formats a table with all key metrics
- A `@track_call(session)` decorator that wraps LLM client methods and auto-records `CallMetrics`
- A `main.py` simulating 10 LLM calls (mix of models, some failures) and printing the report
- Tests: record adds metrics, total tokens sum correctly, error rate calculated, report contains model names

### Python Skill Focus
- **Dataclasses** — `CallMetrics`, `SessionMetrics` as typed measurement containers
- **`collections.defaultdict`** — grouping calls by model name
- **Aggregate properties** — `@property` for computed stats: `error_rate`, `avg_latency_ms`
- **Decorators** — `@track_call(session)` wraps calls and records metrics automatically
- **String formatting** — `f"{value:>10.2f}"` for aligned tabular report output

### AI Concept Focus
- **Session-level observability** — tracking all LLM calls within a single user session
- **Cost tracking** — accumulating per-call costs to get session-level spend
- **Error rate monitoring** — what % of LLM calls fail and why
- **Model usage breakdown** — which models were called, how many tokens each used

---

## Day 30 – Mini Standalone RAG Chatbot

### Goal
Build a complete, self-contained RAG chatbot in a single Python project.
Load documents from a folder, index them, and serve an interactive CLI chat interface
where answers are grounded in the indexed documents. This is your Day 30 showcase project.

### What to Build
- A document loader that reads `.txt` and `.md` files from a `./docs` folder
- A chunker (fixed-size with overlap), an embedder (OpenAI or stub), and an in-memory vector store
- A `RAGChatbot` class with `index_documents(folder)` and `chat(question) -> ChatResponse`
- A `ChatResponse` dataclass: `answer`, `sources: list[str]`, `num_sources`, `latency_ms`
- Conversation memory that keeps the last 10 exchanges
- A Typer CLI with two commands: `index --folder ./docs` and `chat` (starts REPL)
- A `README.md` inside `day-30/` explaining how to run the chatbot end-to-end
- Tests: indexing populates store, chat returns response with sources, memory accumulates

### Python Skill Focus
- **Integration** — combining all skills: dataclasses, pathlib, asyncio (optional), Typer, logging
- **Clean project structure** — single-day project that is self-contained and runnable in 5 minutes
- **`pathlib`** — file loading, directory scanning
- **Typer** — two-command CLI: `index` + `chat`
- **Dependency injection** — injectable embed and complete functions for testability

### AI Concept Focus
- **Full RAG chatbot** — document indexing + retrieval + generation + conversation memory in one project
- **Source-grounded answers** — every response cites which document chunks it used
- **Conversation-aware RAG** — conversation history included in the prompt alongside retrieved context
- **End-to-end demo** — a complete, explainable AI project you can run, show, and extend
