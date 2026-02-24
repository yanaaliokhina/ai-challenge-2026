# Claude Project Rules

You are operating inside a structured AI learning project.

## 🔒 File Access Rules

You are allowed to read:

- README.md (only to detect next challenge)

You MUST NOT:

- Read other day folders
- Inspect src/ directories
- Modify existing challenge folders
- Refactor code
- Analyze unrelated files

---

## 🧱 Tech Stack Rules

All challenges must use the SAME tech stack:

- Python 3.11+
- FastAPI (when API is needed)
- Pydantic
- asyncio
- httpx
- pytest
- Optional: Redis
- Optional: local file storage

---

## 🧠 AI Scope Rules

AI depth level: beginner → intermediate.

Allowed topics:
- LLM API usage
- Prompt templates
- Structured outputs
- Embeddings
- RAG basics
- Agents
- Sub-agents
- Tool usage
- Guardrails
- Evaluation basics
- Token measurement
- Latency measurement
- Retry/fallback

Avoid:
- Enterprise orchestration
- Complex distributed architecture
- Kubernetes
- Production DevOps systems

---

## 📂 Folder Naming Rules

Each challenge must:

- Be created as `day-{NN}`
- Include:
    - instructions.md
    - usage_examples.md

instructions.md:
- Functional requirements only
- No code

usage_examples.md:
- Day-specific run examples only (flags, arguments, example inputs/outputs)
- Day-specific test examples only (specific test files, markers, or edge cases)
- No generic setup instructions — those live in README.md

---

## 🧩 Behavioral Rules

- Do not over-engineer.
- Do not modify previous work.
- Do not comment code.
- Do not introduce new frameworks.
- Keep scope ≤ 3 hours of implementation.
- Keep requirements clear and structured.
- Focus on learning AI fundamentals.