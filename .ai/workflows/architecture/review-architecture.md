---
id: architecture/review-architecture
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: architecture
entry_point: true
---

# Architecture Workflow — Review Architecture

- **Prompt:** `.ai/prompts/roles/principal-system-designer.md`
- **Critic:** `.ai/prompts/critics/architecture-validator.md`
- **Template:** `templates/architecture-review.template.md`

## Inputs

- An architecture proposal, draft ADR, or existing system design

## Steps

1. Run the Principal System Designer over the proposal.
2. Run the Architecture Validator critic against the checklist.
3. If over-engineered → `repair/simplify-overengineered-plan.md`.
4. Record findings and any ADR candidates.

## Artifacts Produced

- `architecture-review.md` (project folder or `docs/architecture/`)

## Exit Criteria

- Review complete; complexity justified; ADR candidates captured.

## Next

→ `record-adr.md` for any accepted decision, or back to the feature build.
