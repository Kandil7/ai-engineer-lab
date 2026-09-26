---
id: feature/06-reflect
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: feature
entry_point: false
---

# Feature Workflow — 06 Reflect

Close the loop. Turn the work into durable learning.

- **Prompt:** `.ai/prompts/roles/learning-coach.md`
- **Template:** `templates/daily-log.template.md` / `templates/weekly-review.template.md`

## Inputs

- The completed feature: `plan.md`, `ai-review.md`, `mistakes.md`, `notes.md`

## Steps

1. Active recall: explain the feature from memory; Learning Coach corrects gaps.
2. Distill 2–4 reusable lessons and where each applies.
3. Update learning notes (`docs/learning/notes/...`).
4. If a reusable decision emerged, ensure an ADR exists.
5. Plan the next small feature.

## Artifacts Produced

- `docs/learning/notes/weekly/<date>.md` (or daily)
- Updated `mistakes.md` if new lessons surfaced

## Exit Criteria

- Reflection captured; next step queued.
- **Definition of done:** feature has plan + review + reflection (+ debug doc if a bug occurred).

## Next

→ Feature complete. Start a new feature at `01-plan.md`.
