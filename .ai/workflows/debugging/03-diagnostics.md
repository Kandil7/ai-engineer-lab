---
id: debugging/03-diagnostics
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: debugging
entry_point: false
---

# Debugging Workflow — 03 Diagnostics

- **Prompt:** `.ai/prompts/roles/debugging-specialist.md`

## Inputs

- Ranked hypotheses from step 02

## Steps

1. Pick the cheapest diagnostic that discriminates between the top hypotheses.
2. Run it; record the result and what it rules in/out.
3. Iterate until the root cause is confirmed by evidence.

## Artifacts Produced

- Diagnostics table + confirmed root cause in `debugging-session.md`

## Exit Criteria

- Root cause confirmed with evidence (not assumed).

## Next

→ `04-fix-verification.md`
