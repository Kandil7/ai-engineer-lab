---
id: feature/02-design
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: feature
entry_point: false
---

# Feature Workflow — 02 Design

Run when the feature touches **system boundaries** (new service, schema change, cross-cutting
concern). Otherwise skip to `03-build.md`.

- **Prompt:** `.ai/prompts/roles/system-architect.md` (or `principal-system-designer.md` for large systems)
- **Critic:** `.ai/prompts/critics/architecture-validator.md`
- **Template:** `templates/architecture-review.template.md` (+ `templates/adr.template.md` if a decision is recorded)

## Inputs

- `plan.md` from step 01
- Relevant existing architecture docs / ADRs

## Steps

1. Run the System Architect: components, data flow, schema, scalability, failure points, tradeoffs.
2. Run the Architecture Validator critic; if over-engineered → `repair/simplify-overengineered-plan.md`.
3. For any hard-to-reverse choice, record an ADR via `architecture/record-adr.md`.

## Artifacts Produced

- `projects/<path>/architecture-review.md`
- (optional) `docs/decisions/NNNN-<slug>.md`

## Exit Criteria

- Architecture review accepted; ADR candidates recorded.
- **Approval checkpoint:** architecture approved before large implementation.

## Next

→ `03-build.md`
