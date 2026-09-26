---
id: feature/01-plan
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: feature
entry_point: true
---

# Feature Workflow — 01 Plan

**Entry point** for any new feature. Start here.

- **Prompt:** `.ai/prompts/roles/project-planner.md`
- **Template:** `templates/project-plan.template.md`

## Inputs

- Feature request / idea
- `feature-spec.md` (if it exists) in the project folder
- Project path under `projects/...`

## Steps

1. Read the feature request and any existing `feature-spec.md`.
2. Run the Project Planner: restate goal, define MVP-first, decompose into ordered tasks.
3. Propose the file structure and acceptance criteria.
4. Surface open questions; if scope is unclear, stop and ask (do not guess).

## Artifacts Produced

- `projects/<path>/plan.md`

## Exit Criteria

- `plan.md` exists with MVP scope, file structure, acceptance criteria, and open questions.
- **Approval checkpoint:** plan approved before build.

## Next

→ `02-design.md` (if it touches system boundaries) or `03-build.md`.
