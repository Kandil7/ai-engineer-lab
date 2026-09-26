---
id: debugging/04-fix-verification
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: debugging
entry_point: false
---

# Debugging Workflow — 04 Fix & Verification

- **Prompt:** `.ai/prompts/roles/debugging-specialist.md` + `roles/pair-programmer.md`

## Inputs

- Confirmed root cause from step 03

## Steps

1. Implement a fix that addresses the **root cause**, not just the symptom.
2. Add a regression test that fails before the fix and passes after.
3. Verify the original reproduction no longer triggers the bug.
4. Document root cause + how it was found in `mistakes.md` and the debugging session.

## Artifacts Produced

- Code + regression test
- Completed `debugging-session.md`
- Updated `mistakes.md`

## Exit Criteria

- Bug no longer reproduces; regression test added; no new failures.

## Next

→ Resume the feature workflow, or close out.
