---
id: debugging/01-symptom-capture
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: debugging
entry_point: true
---

# Debugging Workflow — 01 Symptom Capture

- **Prompt:** `.ai/prompts/roles/debugging-specialist.md`
- **Template:** `templates/bug-report.template.md` → `templates/debugging-session.template.md`

## Inputs

- Observed wrong behavior, logs, error output, the conditions it occurs under

## Steps

1. Record exact symptoms: what happened, expected vs. actual, reproduction steps.
2. Capture environment and the relevant code/context.
3. Determine reproducibility (always / intermittent / cannot reproduce).

## Artifacts Produced

- `bug-report.md` (project folder or `docs/learning/`)
- New `debugging-session.md` started

## Exit Criteria

- Symptoms and reproduction documented. If not reproducible → improve evidence capture first.

## Next

→ `02-hypothesis-ranking.md`
