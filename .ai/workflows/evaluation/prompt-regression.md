---
id: evaluation/prompt-regression
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: evaluation
entry_point: true
---

# Evaluation Workflow — Prompt Regression

Guard prompts against drift when they change.

- **Prompt:** `.ai/prompts/critics/prompt-auditor.md`
- **Template:** `templates/evaluation-report.template.md`

## Inputs

- A prompt under `.ai/prompts/...` and its golden cases in `evaluations/prompts/golden-cases/`

## Steps

1. Run the prompt against fixed golden inputs.
2. Check: no invented requirements, bounded structure, correct section coverage,
   constraint adherence (e.g. reviewer keeps severity; planner stays MVP-first).
3. Compare against the stored regression snapshot.
4. Fail if output adds unjustified components or drops required sections.

## Artifacts Produced

- `evaluations/prompts/regressions/<prompt-id>-<date>.md`

## Exit Criteria

- Prompt passes its golden set; regression snapshot updated if intentionally changed.

## Next

→ Bump version in `registries/prompt-registry.yaml`.
