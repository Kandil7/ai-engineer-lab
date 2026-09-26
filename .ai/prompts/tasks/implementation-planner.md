---
id: task.implementation-planner
layer: task
version: 1.0.0
status: deprecated
owner: workspace
deprecated_in_favor_of: role.project-planner
pairs_with_roles: [project-planner, system-architect]
constraints: [mvp-first, file-structure-required, repo-first]
---

# Task: Implementation Planner (DEPRECATED)

> Deprecated 2026-09-26: this task duplicates `roles/project-planner.md` — both fill
> `templates/project-plan.template.md` with file structure, acceptance criteria, and
> ordered tasks. Use the Project Planner instead. Kept on disk for provenance; do not
> wire it into any workflow.
---

# Task: Implementation Planner

Turn an approved spec/architecture into a concrete, ordered implementation plan.

## Steps

1. Confirm the MVP slice.
2. Sequence tasks with dependencies and rough estimates.
3. Specify the file structure to create/modify.
4. Define acceptance criteria and how each will be verified.
5. List risks and open questions.

## Constraints

- Fill `templates/project-plan.template.md`.
- Required: Proposed File Structure, MVP First, Acceptance Criteria, Open Questions.
- No implementation code — this is a plan.
