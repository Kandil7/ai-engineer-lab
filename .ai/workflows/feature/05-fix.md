---
id: feature/05-fix
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: feature
entry_point: false
---

# Feature Workflow — 05 Fix

- **Prompt:** `.ai/prompts/tasks/review-summarizer.md` + `roles/pair-programmer.md`

## Inputs

- `ai-review.md` from step 04

## Steps

1. Summarize review findings into a prioritized fix list (preserve severity).
2. Fix **Critical** and **High** first; **Medium** when feasible.
3. You implement the fixes; AI assists with hints.
4. Re-run tests; if a bug needs investigation, branch to the debugging workflow.
5. Record what went wrong and the lesson in `mistakes.md`.

## Artifacts Produced

- Updated `src/` + `tests/`
- `projects/<path>/mistakes.md`

## Exit Criteria

- No open Critical/High findings (or explicitly deferred with reason).
- Tests green.

## Next

→ `06-reflect.md`
