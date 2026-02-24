---
name: next-challenge
description: Generate the next AI challenge instructions based on README.md roadmap
---

You are responsible for generating the next AI challenge.

Follow these steps STRICTLY:

STEP 1 — Read README.md  
- Parse the 30-day challenge list.
- Identify the first challenge that does NOT yet have a corresponding folder named `day-{NN}`.
- Determine the correct day number.

STEP 2 — Validate  
- If all 30 folders already exist, respond:
  "All 30 challenges have already been generated."
  Then STOP.

STEP 3 — Create Folder
Create a new folder:

day-{NN}

Example:
day-01
day-02
...

Inside that folder create:

- instructions.md
- usage_examples.md

STEP 4 — Generate instructions.md

IMPORTANT RULES:

instructions.md MUST contain:

1. Title
2. Goal
3. What We Should Build
4. Functional Requirements (detailed and structured)
5. Python Topics Covered
6. AI Topics Covered
7. Acceptance Criteria

instructions.md MUST NOT:

- Contain code
- Contain diffs
- Contain implementation patches
- Contain a "How to Run" section (that belongs in usage_examples.md)
- Modify any existing code
- Reference other day folders

This file must describe WHAT to build, not HOW to modify code.

STEP 5 — Generate usage_examples.md

usage_examples.md MUST contain day-specific examples only.
Do NOT repeat generic setup steps from README.md (venv, pip install, env export).

1. How to Run — day-specific examples:
   - The exact command to run this challenge (e.g. `python src/main.py --prompt "Hello"`)
   - Any flags, arguments, or modes specific to this challenge
   - Example inputs and expected outputs where helpful

2. How to Run Tests — day-specific examples:
   - The exact pytest command for this challenge (e.g. `pytest tests/test_client.py -v`)
   - Any markers, filters, or environment notes specific to this challenge

usage_examples.md MUST NOT:

- Repeat generic steps already in README.md (venv setup, pip install, env vars export)
- Contain implementation details or code logic
- Reference other day folders

STEP 6 — Constraints

- Use the same tech stack as defined in README.md
- Do NOT read or inspect any folders except:
    - README.md
- Do NOT modify any existing files
- Do NOT generate implementation code
- Only create the new day folder and its markdown files

Be precise.
Be structured.
Be consistent with previous challenges.