---
id: architecture/propose-decision
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: architecture
entry_point: true
---

# Architecture Workflow — Propose Decision

- **Prompt:** `.ai/prompts/roles/system-architect.md` (+ `tasks/adr-writer.md`)
- **Template:** `templates/adr.template.md`

## Inputs

- A technology/architecture choice candidate (often surfaced by a feature or review)

## Steps

1. Frame the context and decision drivers.
2. Lay out 2–3 options with pros/cons.
3. Recommend an option with rationale tied to drivers.
4. Draft consequences (positive, negative, follow-ups).

## Artifacts Produced

- A draft ADR (status: Proposed)

## Exit Criteria

- Draft ADR with a non-empty Consequences section.

## Next

→ `review-architecture.md` (validate) then `record-adr.md` (finalize).
