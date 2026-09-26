---
id: feature/04-review
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: feature
entry_point: false
---

# Feature Workflow — 04 Review

- **Prompt:** `.ai/prompts/roles/code-reviewer.md`
- **Critic:** `.ai/prompts/critics/code-quality-validator.md`
- **Template:** `templates/code-review.template.md`
- **Script:** `infra/scripts/new-review.ps1`

## Inputs

- The code written in step 03 (`src/`, `tests/`)

## Steps

1. Run the Code Reviewer over the most important 2–3 files.
2. Record findings by **severity** (Critical/High/Medium/Low) with exact file references.
3. Run the Code Quality Validator critic for a second pass.
4. Assign an overall score and an approval decision.

## Artifacts Produced

- `projects/<path>/ai-review.md`
- Entry appended to `registries/review-log.yaml` (via `new-review.ps1`)

## Exit Criteria

- `ai-review.md` exists with severities and a decision.
- **Approval checkpoint:** review complete before marking feature done.

## Next

→ `05-fix.md` (if findings) else `06-reflect.md`
