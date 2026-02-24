# Coding Challenges: Day 06 – Day 15

---

## Day 06 – Async Batch LLM Caller

### Goal
Call the LLM API concurrently for a batch of prompts using Python's `asyncio`.
Control concurrency with a semaphore to avoid rate-limit errors. Return all results
including partial failures so one bad call does not cancel the rest.

### What to Build
- An `async_ask(prompt, model, max_tokens) -> AsyncLLMResponse` coroutine wrapping the Anthropic async client
- An `AsyncLLMResponse` dataclass holding `content`, `input_tokens`, `output_tokens`
- A `BatchResult` dataclass with `index`, `prompt`, `response`, `error`, `elapsed_seconds`, and a `success` property
- A `BatchProcessor` dataclass with `max_concurrency`, `model`, and an async `process(prompts) -> list[BatchResult]` method
- A `main.py` that runs 5 prompts concurrently and prints results with total wall-clock time
- Async tests with `pytest-asyncio` and `AsyncMock` covering: all success, partial failure, concurrency limit respected

### Python Skill Focus
- **`asyncio`** — `async/await`, `asyncio.gather`, `asyncio.Semaphore`
- **`AsyncMock`** — mocking coroutines in tests with `unittest.mock.AsyncMock`
- **`pytest-asyncio`** — `@pytest.mark.asyncio` and `asyncio_mode = "auto"`
- **Dataclasses** — `BatchResult` with a computed `success` property
- **Error isolation** — wrapping each task in `try/except` inside `asyncio.gather`

### AI Concept Focus
- **Concurrent LLM calls** — parallel requests reduce total wall time for batch jobs
- **Rate limiting** — `asyncio.Semaphore(N)` as a concurrency gate to stay within API limits
- **Partial failure handling** — returning results even when some calls fail mid-batch
- **Latency measurement** — `time.perf_counter()` around async calls to profile per-prompt timing

---

## Day 07 – Prompt Version Manager CLI

### Goal
Build a CLI tool to create, list, show, compare, and delete versioned prompt templates
stored as JSON files on disk. Practice building a real, useful developer tool with Typer.

### What to Build
- A `PromptRecord` dataclass with fields: `name`, `content`, `version`, `description`, `tags`, `created_at`
- A `PromptStore` class that saves/loads records as JSON files in a `.prompts/` directory, named `{name}__{version}.json`
- A Typer CLI with 5 commands: `add` (reads content from stdin), `list` (rich table), `show`, `compare` (two versions side by side), `delete`
- A `main.py` entry point
- Tests using `tmp_path` pytest fixture covering: save/load roundtrip, load missing raises, list all, delete

### Python Skill Focus
- **Typer** — commands, `Argument`, `Option`, `typer.prompt()`, `raise typer.Exit(1)`
- **`pathlib.Path`** — `Path.glob`, `Path.read_text`, `Path.write_text`, `Path.unlink`
- **`dataclasses.asdict`** — serializing dataclasses to dicts for `json.dumps`
- **`rich`** — `Table` for formatted CLI output
- **`tmp_path`** pytest fixture — safe file-system tests without cleanup

### AI Concept Focus
- **Prompt versioning** — why production AI systems version prompts like code
- **Prompt comparison** — side-by-side diff of two prompt versions for A/B testing decisions
- **Template metadata** — tracking `created_at`, `version`, `tags` for audit and search
- **Prompt management workflow** — add → test → version → compare → promote

---

## Day 08 – Embedding Generator + Cosine Similarity Search

### Goal
Generate text embeddings via API, then find the most semantically similar texts
from a corpus using cosine similarity. Implement the math manually before using numpy.

### What to Build
- A `cosine_similarity_manual(a, b) -> float` function using pure Python math
- A `cosine_similarity_numpy(a, b) -> float` function using numpy vectorized ops
- A `top_k_similar(query_embedding, corpus_embeddings, k) -> list[tuple[int, float]]` function
- A `get_embedding(text) -> list[float]` and `get_embeddings(texts) -> list[list[float]]` using OpenAI embeddings API
- A `SimilaritySearcher` class with `add_documents(texts)` and `search(query, top_k) -> list[SearchResult]`
- A `SearchResult` dataclass with `text`, `score`, `index` and a readable `__repr__`
- Tests (no API calls): identical vectors = 1.0, orthogonal = 0.0, zero vector = 0.0, top-K sorted descending

### Python Skill Focus
- **numpy** — `np.dot`, `np.linalg.norm`, vectorized similarity over a matrix
- **Type hints** — `NDArray`, `Sequence[float]`, `list[tuple[int, float]]`
- **Dataclasses** — `SearchResult` with custom `__repr__`
- **Sorting** — `sorted(..., key=lambda x: x[1], reverse=True)`
- **Batch API calls** — reducing round-trips by embedding multiple texts in one request

### AI Concept Focus
- **Embeddings** — dense vectors where similar meanings cluster together in vector space
- **Cosine similarity** — dot product normalized by magnitudes, range -1 to 1, direction not magnitude
- **Semantic search** — finding similar *meaning*, not matching keywords
- **Embedding batching** — why you batch texts in one API call instead of calling one at a time

---

## Day 09 – Text Chunker with Multiple Strategies

### Goal
Build a text chunker that splits long documents into smaller pieces using three
interchangeable strategies: fixed-size, sentence-based, and recursive. No LLM calls —
pure Python text processing with the strategy pattern.

### What to Build
- A `ChunkConfig` dataclass with `chunk_size`, `chunk_overlap`, `min_chunk_size`
- A `Chunk` dataclass with `text`, `index`, `start_char`, `end_char`, `char_count` property
- A `BaseChunker` abstract class (`ABC`, `@abstractmethod chunk(text) -> list[Chunk]`)
- Three concrete chunkers: `FixedSizeChunker` (character windows with overlap), `SentenceChunker` (groups sentences until size limit), `RecursiveChunker` (tries `\n\n`, `\n`, `. `, ` ` separators in order)
- A `main.py` that chunks a 500-word text with all 3 strategies and prints chunk counts and sizes
- Tests: multiple chunks produced, sequential indexes, size respected, min_chunk_size filters tiny chunks

### Python Skill Focus
- **Abstract base class** — `ABC` + `@abstractmethod` enforces implementation at class instantiation
- **Strategy pattern** — swap chunking behavior by passing a different chunker object
- **Dataclasses** — `ChunkConfig` as config, `Chunk` as output value object
- **Regex** — `re.split(r'(?<=[.!?])\s+', text)` for sentence splitting
- **Generators** — optionally yield chunks instead of building a list

### AI Concept Focus
- **Why chunking** — LLMs have context windows; long documents must be split before embedding
- **Chunk size trade-offs** — too small loses context, too large adds noise to retrieval
- **Overlap** — repeating content at chunk boundaries ensures queries spanning two chunks still match
- **Sentence vs fixed** — sentence chunking preserves semantic units; fixed-size is predictable for indexing

---

## Day 10 – In-Memory Vector Store

### Goal
Build a simple in-memory vector store from scratch — no ChromaDB, no FAISS.
Store documents with embeddings and query by cosine similarity using numpy matrix operations.

### What to Build
- A `Document` dataclass with `text`, `embedding`, `metadata`, and auto-generated `doc_id` (uuid)
- A `QueryResult` dataclass with `document` and `score`, plus a clean `__repr__`
- A `VectorStore` class with: `add(doc)`, `add_many(docs)`, `query(embedding, top_k, filter_metadata)`, `count` property
- Batch cosine similarity using numpy matrix multiply (`@` operator) rather than a Python loop
- Metadata filtering applied before similarity computation
- Tests: add and count, query returns top-K, results sorted by score descending, metadata filter, empty store

### Python Skill Focus
- **numpy** — matrix multiply `matrix @ query` for batch dot products, `np.argsort` for ranking
- **`TypeVar` + `Generic[T]`** — optionally make `VectorStore[T]` generic over document type
- **`uuid`** — `str(uuid.uuid4())` for unique document IDs
- **Cache invalidation** — `self._matrix = None` on add, recompute lazily on query
- **Dataclasses** — immutable `QueryResult`, mutable `Document`

### AI Concept Focus
- **Vector store internals** — an embedding matrix + metadata list + similarity computation
- **Batch similarity** — computing query vs all docs at once with matrix ops vs one-by-one loops
- **Metadata filtering** — filtering by tags/source before scoring reduces noise in results
- **Store design** — separation of write path (add) from read path (query)

---

## Day 11 – Simple RAG Pipeline

### Goal
Build an end-to-end Retrieval-Augmented Generation pipeline in a single class.
Load text, chunk it, embed chunks, store them, then answer questions using retrieved context.
Make it fully testable by injecting the embed and complete functions.

### What to Build
- A `RAGConfig` dataclass: `chunk_size`, `chunk_overlap`, `top_k`, `model`, `max_tokens`
- A `RAGAnswer` dataclass: `question`, `answer`, `sources` (list of chunk previews), `num_chunks_used`
- A `RAGPipeline` class with constructor accepting `config`, `embed_fn`, `complete_fn` (all injectable)
- `add_document(text, metadata)` — chunks, embeds, stores
- `query(question) -> RAGAnswer` — embeds question, retrieves top-K chunks, builds prompt, calls LLM
- A `_build_prompt(question, context)` method that formats the RAG prompt
- Default implementations using OpenAI embeddings + Anthropic completions
- Tests using fake `embed_fn` and `complete_fn` — no real API calls

### Python Skill Focus
- **Dependency injection** — pass `embed_fn` and `complete_fn` as callables, swap for tests
- **`Callable[[str], list[float]]`** — type hint for injectable functions
- **Composing components** — chunker + embedder + store + LLM in one coordinated class
- **Type hints** — `Callable`, `Optional`, full annotations on pipeline methods
- **Dataclasses** — config and result objects with clear fields

### AI Concept Focus
- **End-to-end RAG** — the full loop: chunk → embed → store → retrieve → prompt → answer
- **Context injection** — inserting retrieved chunks into the prompt before the question
- **Source attribution** — tracking which chunks were used so the caller knows what grounded the answer
- **Retrieval quality** — why what you retrieve determines the quality of the answer

---

## Day 12 – File Document Indexer

### Goal
Build a document indexer that reads `.txt` and `.md` files from a directory,
generates embeddings, and persists the index to a JSON file so it survives
process restarts without re-indexing unchanged files.

### What to Build
- A `LoadedDocument` dataclass with `path`, `content`, `extension`, `name` property
- A `load_directory(dir, recursive) -> list[LoadedDocument]` function using `pathlib.Path.glob`
- An `IndexedDocument` dataclass: `name`, `path`, `content_preview`, `embedding`, `char_count`
- A `DocumentIndexer` class: loads existing index from JSON on init, `index(name, content)` adds and saves, `search(query, top_k)` retrieves, `stats` property
- A CLI with `index` (process a folder), `search` (query), and `stats` commands
- Tests using `tmp_path`: save/load roundtrip, persistence across instances, directory loading filters by extension

### Python Skill Focus
- **`pathlib`** — `Path.glob("**/*")`, `Path.read_text`, `Path.write_text`, `Path.is_dir`, `Path.suffix`
- **JSON persistence** — `json.dumps(asdict(obj))` for saving, `ClassName(**data)` for loading
- **Error handling** — `PermissionError`, `UnicodeDecodeError` caught gracefully when reading files
- **`dataclasses.asdict`** — one-liner serialization of nested dataclasses
- **`tmp_path`** pytest fixture — file-system tests that clean up automatically

### AI Concept Focus
- **Document indexing** — batch processing files and storing embeddings for later retrieval
- **Persistent index** — saving embeddings to disk avoids re-embedding on every run
- **Incremental updates** — skip files already in the index, only process new/changed files
- **File-based knowledge base** — practical pattern for RAG over a folder of documents

---

## Day 13 – Conversation Memory Manager

### Goal
Build a conversation memory manager that tracks message history and enforces a
token budget by trimming the oldest messages when the budget is exceeded.
Support both a hard token limit and a max message count.

### What to Build
- A `Message` dataclass with `role: Literal["system", "user", "assistant"]` and `content`, plus `to_dict()`
- A `MemoryConfig` dataclass: `max_tokens`, `max_messages`, `system_prompt`, `token_counter: Callable[[str], int]`
- A `ConversationMemory` class using `collections.deque` internally
- `add(role, content)` — appends message and calls `_enforce_budget()`
- `get_messages() -> list[dict]` — returns system prompt + full history as list of dicts
- `token_count` property — computed total across all messages
- `_enforce_budget()` — `popleft()` until within both limits
- Tests: add message, get messages includes system, token budget trims oldest, message limit trims, clear resets

### Python Skill Focus
- **`collections.deque`** — `appendright` / `popleft` in O(1) vs `list.pop(0)` in O(n)
- **`Literal` type** — `Literal["system", "user", "assistant"]` for role type safety
- **Dependency injection** — `token_counter: Callable[[str], int]` makes memory model-agnostic
- **Properties** — `token_count` as a computed `@property` not stored state
- **Dataclasses with callable fields** — `field(default_factory=...)` for callable defaults

### AI Concept Focus
- **Context windows** — LLMs have hard token limits; history must fit within them
- **Sliding window memory** — discard oldest messages to stay within budget
- **Token budget vs message count** — two separate limits: token budget + message count cap
- **Memory strategies** — verbatim sliding window is the simplest; summarization-based compression is an extension

---

## Day 14 – ChromaDB Mini-Indexer

### Goal
Replace an in-memory vector store with ChromaDB — a persistent, embeddable vector database.
Index documents, persist them to disk, then query across process restarts without re-indexing.
Practice wrapping a third-party library behind your own clean interface.

### What to Build
- A `StoreResult` dataclass: `doc_id`, `text`, `score`, `metadata`
- A `ChromaStore` class wrapping ChromaDB: `__init__` accepts `collection_name`, `persist_dir`, `embed_fn`
- `add(doc_id, text, metadata)` — adds to ChromaDB collection
- `query(query_text, top_k, where) -> list[StoreResult]` — queries and converts distance to similarity score
- `count` property, `delete(doc_id)` method
- A `main.py` that: indexes 5 docs, queries, exits, re-instantiates with same `persist_dir`, queries again (proves persistence)
- Tests using `EphemeralClient` (no disk): add, query, metadata stored, delete, empty returns empty

### Python Skill Focus
- **Adapter pattern** — hiding ChromaDB's API behind your own `ChromaStore` interface
- **Third-party library integration** — `chromadb.PersistentClient` vs `EphemeralClient`
- **`pathlib.Path`** — passing persist directory as a typed `Path` object
- **Type hints** — `dict[str, Any]`, `Callable[[str], list[float]] | None`
- **Score conversion** — ChromaDB returns distances (0 = identical, 2 = opposite); convert to similarity

### AI Concept Focus
- **Persistent vector store** — embeddings survive process restarts; no re-embedding on relaunch
- **Collection management** — namespacing documents into named collections in ChromaDB
- **Metadata filtering** — ChromaDB `where` clauses filter by metadata before similarity ranking
- **Embedding function plug-in** — pass your own embedder or use ChromaDB's built-in default

---

## Day 15 – Tool Registry Pattern

### Goal
Build a decorator-based tool registry where functions self-register as callable tools
with a name, description, and JSON schema. This is the foundation of any agent
that needs to select and call tools based on LLM output.

### What to Build
- A `ToolDefinition` dataclass: `name`, `description`, `parameters_schema` (JSON schema dict), `fn` (the callable)
- A `ToolRegistry` class with an internal `dict[str, ToolDefinition]`
- A `@registry.tool(name, description)` decorator that registers the decorated function
- A `get(name) -> ToolDefinition` method and a `list_tools() -> list[dict]` method (returns schemas for LLM prompt)
- A `call(name, **kwargs) -> Any` method that looks up and invokes the tool
- Example tools: `calculator` (add/subtract/multiply), `word_count`, `get_current_date`
- Tests: registration, lookup, call, unregistered name raises, list_tools returns correct schema

### Python Skill Focus
- **Decorators** — `@registry.tool(...)` as a method-based parameterized decorator
- **`functools.wraps`** — preserve decorated function metadata
- **`inspect`** — `inspect.signature` to extract parameter names and annotations
- **`dataclasses`** — `ToolDefinition` as a typed container for tool metadata
- **`dict` as a registry** — `dict[str, ToolDefinition]` as the backing store

### AI Concept Focus
- **Tool registry** — how agents maintain a catalogue of available tools
- **Tool schemas** — JSON schema descriptions that tell the LLM what each tool does and what inputs it takes
- **Tool selection** — LLM chooses a tool by name from the registry based on the schema descriptions
- **Function calling** — the pattern underlying OpenAI function calling and Anthropic tool use
