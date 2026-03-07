---
name: implement-challenge
description: Implement the most recently generated AI challenge and mark it as completed in README.md
---

You are responsible for implementing the latest generated challenge.

Follow these steps STRICTLY.

----------------------------------
AVAILABLE SKILLS
----------------------------------

Before implementing, check for active Claude skills in .claude/skills/.
If a skill matches the scaffolding needs of this challenge,
invoke it automatically — do not duplicate what the skill already provides.

----------------------------------
STEP 1 — Detect Latest Challenge
----------------------------------

- Find the highest-numbered folder matching: day-{NN}
- Confirm it contains:
    - instructions.md
    - src/ (may be empty)

If no challenge folder exists:
Respond:
"No challenge folder found."
Then STOP.

----------------------------------
STEP 2 — Read Allowed Files
----------------------------------

You may read ONLY:

- CLAUDE.md
- README.md
- day-{NN}/instructions.md

You MUST NOT:
- Read other day folders
- Inspect unrelated src directories
- Modify other challenges

----------------------------------
STEP 3 — Analyse Requirements and Implement Based on instructions.md
----------------------------------

- Carefully read instructions.md
- Extract ALL functional requirements
- Identify every distinct behaviour, edge case, and failure mode
- Before writing any boilerplate, check .claude/skills/ for a matching skill.
  If project-scaffold or another relevant skill exists, invoke it to generate
  the base structure, then layer challenge-specific logic on top.
- Implement the solution inside:

    day-{NN}/src/

You may create:
- Python modules
- Supporting files
- tests/ folder inside day-{NN} (if required)

Follow STRICT rules:

- Use only approved tech stack (see CLAUDE.md)
- Write clean, typed Python
- Include docstrings
- Use proper error handling
- Add logging if relevant
- Use async only if needed
- Do not overengineer
- Keep scope ≤ 3 hours equivalent effort

----------------------------------
STEP 4 — Testing
----------------------------------

Create day-{NN}/tests/ and write pytest tests.

Rules:
- One test file per logical module (e.g. tests/test_parser.py, tests/test_client.py)
- Cover every requirement identified in Step 3:
    - Happy-path cases
    - Edge cases (empty input, boundary values, max/min)
    - Error / exception cases
    - Integration-level cases where relevant
- Mock ALL external calls (LLM APIs, HTTP, file I/O where needed)
- Keep tests deterministic — no randomness, no real network calls
- Use descriptive test names: test_<unit>_<scenario>_<expected_result>
- Every test must have a one-line docstring stating what it verifies

Import rules:
- A global conftest.py already exists and adds src/ to sys.path — do NOT create another conftest.py
- NEVER add sys.path.insert in individual test files
- Import modules directly by name: `from embedding_client import ...` NOT `from src.embedding_client import ...`
- Mock target strings must use the direct module name: `"embedding_client.httpx.post"` NOT `"src.embedding_client.httpx.post"`

----------------------------------
STEP 5 — Create or Update usage_examples.md
----------------------------------

Create or update day-{NN}/usage_examples.md with day-specific examples only.
Do NOT repeat generic setup steps from README.md (venv, pip install, env vars export).

1. How to Run — day-specific examples:
   - The exact command to run this challenge (e.g. `python src/main.py --prompt "Hello"`)
   - Any flags, arguments, or modes specific to this challenge
   - Example inputs and expected outputs where helpful

2. How to Run Tests — day-specific examples:
   - The exact pytest command for this challenge (e.g. `pytest tests/test_client.py -v`)
   - Any markers, filters, or environment notes specific to this challenge

----------------------------------
STEP 6 — Mark as Completed
----------------------------------

Open README.md.

Locate the section for "Day {NN}".

Update its status to:

✅ DONE

If no status exists, append:
Status: ✅ DONE

Do NOT modify other days.

----------------------------------
STRICT RULES
----------------------------------

- Do not modify other day folders
- Do not comment code
- Do not refactor previous challenges
- Do not introduce new frameworks
- Keep implementation clean and minimal
- Follow CLAUDE.md rules strictly