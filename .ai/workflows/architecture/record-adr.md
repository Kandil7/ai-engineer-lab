---
id: architecture/record-adr
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: architecture
entry_point: false
---

# Architecture Workflow — Record ADR

Finalize and index an accepted architectural decision.

- **Prompt:** `.ai/prompts/tasks/adr-writer.md`
- **Script:** `infra/scripts/new-adr.ps1`
- **Template:** `templates/adr.template.md`

## Inputs

- A reviewed draft ADR (from `propose-decision.md`)

## Steps

1. Run `new-adr.ps1 "<title>"` to allocate the next number and create the file from the template.
2. Fill context, options, decision, and Consequences.
3. Set status (Proposed → Accepted) and deciders.
4. Update `docs/decisions/README.md` index and `registries/decision-log.yaml`.

## Artifacts Produced

- `docs/decisions/NNNN-<slug>.md`
- Updated decision index + registry

## Exit Criteria

- ADR accepted, numbered, and indexed.
- **Approval checkpoint:** ADR accepted before any irreversible change.

## Next

→ Proceed with implementation per the decision.
