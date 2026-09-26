# AI Workspace Architecture (`.ai/`)

The `.ai/` directory is the "brain" of the repo: how AI operating modes are composed and invoked.

## Prompt Layering

Each AI run is assembled deterministically:

```text
1. system/workspace-governor.md      (global rules)
2. roles/<role>.md                   (who you are)
3. tasks/<task>.md                   (the specific job, optional)
4. system/output-format-rules.md     (output shape)
5. critics/<critic>.md | repair/*    (optional follow-up pass)
```

This keeps prompts **modular** — no monolithic mega-prompt. Format rules live once in
`output-format-rules.md` (DRY); each prompt only declares its own constraints.

## Roles ↔ Workflows ↔ Templates

| Role | Primary workflow | Template produced |
|------|------------------|-------------------|
| Project Planner | feature/01-plan | project-plan |
| System Architect | feature/02-design | architecture-review / adr |
| Pair Programmer | feature/03-build | (code, notes) |
| Code Reviewer | feature/04-review | code-review |
| Debugging Specialist | debugging/* | debugging-session |
| Source Learning Agent | learning/* | source-* |
| Principal System Designer | architecture/*, evaluation/* | architecture-review / eval |
| Learning Coach | feature/06-reflect, learning | daily/weekly-review |

## Critics & Repair

- **Critics** run a second adversarial pass (architecture-validator, code-quality-validator,
  prompt-auditor) and emit findings with severity — they never rewrite.
- **Repair** prompts handle failure modes: missing context, over-engineering, wrong output shape.

## Registration & Governance

Everything in `.ai/` is registered in:
- `registries/prompt-registry.yaml` — prompt id, version, owner, status, constraints
- `registries/workflow-registry.yaml` — workflow id, steps, inputs, outputs
- `registries/decision-log.yaml` — ADR index synchronized with docs/decisions/
- `registries/template-registry.yaml` — template inventory
- `registries/skills-registry.yaml` — reusable capability tracking

This registration system is the single source of truth for what exists and what each
artifact is allowed to do.

## Prompt Composition Example

```text
Feature request enters the workspace:
    ↓
workspace-governor.md sets the global rules and constraints
    ↓
roles/project-planner.md defines who the AI is and decomposes the work
    ↓
system/output-format-rules.md enforces the output shape (plan.md)
    ↓
(Optional) critics/architecture-validator.md reviews the plan
```

## Current State

All 21 prompts (system, roles, tasks, critics, repair) and 21 workflows (feature,
debugging, learning, architecture, evaluation) exist with `status: active` and are
registered in `registries/`. `tests/*/validate.ps1` gates the inventories and their
cross-references in CI. `task.implementation-planner` is deprecated in favor of
`role.project-planner`; it stays on disk for provenance.

*Last updated: 2026-09-26*
