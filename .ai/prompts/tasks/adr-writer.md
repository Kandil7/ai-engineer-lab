---
id: task.adr-writer
layer: task
version: 1.0.0
status: active
owner: workspace
uses_skills: [adr-writing]
pairs_with_roles: [system-architect, project-planner]
constraints: [consequences-required, options-compared, repo-first]
---

# Task: ADR Writer

Capture an architectural decision as an ADR.

## Steps

1. State the **context** and decision drivers (real constraints).
2. List the options considered with pros/cons.
3. State the decision and its one-paragraph rationale.
4. Write the **Consequences** (required) — positive, negative, follow-ups.

## Constraints

- Fill `templates/adr.template.md` exactly; the Consequences section must not be empty.
- Numbering and file creation are handled by `infra/scripts/new-adr.ps1` — do not invent a number.
- A weak rationale fails review; tie the decision to drivers.

## Output

The ADR markdown under `docs/decisions/NNNN-<slug>.md`, then update `docs/decisions/README.md`
index and `registries/decision-log.yaml`.
