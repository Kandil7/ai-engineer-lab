---
id: feature/03-build
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: feature
entry_point: false
---

# Feature Workflow — 03 Build

You write the code. AI assists step by step.

- **Prompt:** `.ai/prompts/roles/pair-programmer.md` (+ `tasks/feature-builder.md`)

## Inputs

- `plan.md` (and `architecture-review.md` if present)

## Steps

1. Take the next task from `plan.md` (MVP-first order).
2. Run Pair Programmer: it names the file + interface shape; **you implement**.
3. Confirm each step before moving on; ask for a hint, not the full solution, when stuck.
4. Log friction and any AI-provided snippet you had to study into `notes.md`.

## Artifacts Produced

- `projects/<path>/src/...` (your code)
- `projects/<path>/tests/...`
- `projects/<path>/notes.md` (running log of what you learned/where you stuck)

## Exit Criteria

- MVP tasks implemented; code compiles/tests run.
- You can explain each piece from memory.

## Next

→ `04-review.md`
