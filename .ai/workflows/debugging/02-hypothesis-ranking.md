---
id: debugging/02-hypothesis-ranking
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: debugging
entry_point: false
---

# Debugging Workflow — 02 Hypothesis Ranking

- **Prompt:** `.ai/prompts/roles/debugging-specialist.md`

## Inputs

- Symptom capture from step 01

## Steps

1. Generate multiple candidate root causes.
2. Rank by probability with evidence **for** and **against** each.
3. Do **not** attempt a fix yet.

## Artifacts Produced

- Ranked hypotheses table in `debugging-session.md`

## Exit Criteria

- At least 2–3 ranked hypotheses with evidence. Top hypothesis identified.

## Next

→ `03-diagnostics.md`
