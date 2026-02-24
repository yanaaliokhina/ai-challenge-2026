---
name: implement-challenge
description: Implement the most recently generated AI challenge and mark it as completed in README.md
---

You are responsible for implementing the latest generated challenge.

Follow these steps STRICTLY.

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
STEP 3 — Implement Based on instructions.md
----------------------------------

- Carefully read instructions.md
- Extract functional requirements
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

If appropriate:
- Add pytest tests
- Mock LLM API calls
- Keep tests deterministic

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
