# Architecture Decision Records (ADRs)

ADRs capture **why** a decision was made, the options considered, and the consequences. They are
the architectural memory of the workspace. New ADRs are created with `infra/scripts/new-adr.ps1`.

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| [0001](0001-repo-centric-workspace.md) | Repo-centric agentic workspace | Accepted | 2026-06-26 |
| [0002](0002-prompt-modularization.md) | Prompt modularization & `.ai` namespace | Accepted | 2026-06-26 |
| [0003](0003-hybrid-stack-go-fastapi.md) | Hybrid stack — Go core + FastAPI AI | Accepted | 2026-06-26 |
| [0004](0004-adopt-10-week-ai-engineer-track.md) | Adopt the 10-week AI-Engineer track as the active plan | Accepted | 2026-08-02 |
| [0005](0005-vector-db-qdrant-over-chromadb.md) | Vector DB — Qdrant primary, ChromaDB as a one-week comparison | Accepted | 2026-08-02 |
| [0006](0006-adopt-master-ai-engineering-curriculum.md) | Lift the lecture moratorium — adopt the Master AI Engineering curriculum | Accepted | 2026-08-02 |
| [0007](0007-adopt-learning-os-knowledge-registry.md) | Adopt a knowledge registry as the Learning OS backbone | Accepted | 2026-10-10 |

## Lifecycle

```
Proposed → Accepted → (Superseded by ADR-XXXX | Deprecated)
```

## Conventions

| Rule | Detail |
|------|--------|
| File naming | `NNNN-kebab-title.md` (4-digit, zero-padded) |
| Required section | Every ADR must have a non-empty **Consequences** section |
| Registry sync | Keep `registries/decision-log.yaml` in sync with this index |
| Content | Each ADR includes: Context, Decision Drivers, Options Considered, Decision, Consequences |

## Creating a New ADR

Run the PowerShell script:
```powershell
infra/scripts/new-adr.ps1 -Title "Your Decision Title"
```

Or manually:
1. Copy `templates/adr.template.md` to `docs/decisions/NNNN-kebab-title.md`
2. Fill in context, options, decision, and consequences
3. Add to this index table
4. Update `registries/decision-log.yaml`

*Last updated: 2026-08-06*
