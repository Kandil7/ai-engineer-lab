# Architecture Overview

The Full-Stack AI Engineer Lab is a **Repo-Centric Agentic Workspace** organized in seven
logical layers. "Agents" are prompted operating modes (markdown), not runtime processes;
orchestration is human-led and workflow-driven.

## Layers

| Layer | Directory | Purpose |
|-------|-----------|---------|
| **1. Content** | `docs/` | Roadmap, learning paths, deep dives, decision records, cheat sheets |
| **2. Project** | `projects/` | Actual code: DevMate (RAG, LLM, agents), rag-system, capstone |
| **3. Workflow** | `.ai/workflows/` | Step-by-step procedures for planning, building, reviewing, debugging, learning |
| **4. Prompt** | `.ai/prompts/` | Modular operating modes (system / roles / tasks / critics / repair) |
| **5. Template** | `templates/` | Standardized artifact shapes (16 templates) |
| **6. Evaluation** | `evaluations/` | Golden cases, regressions, RAG datasets, reports, release gates |
| **7. Delivery** | `infra/` | Docker Compose, setup scripts, dev tooling |

## Request Lifecycle (Feature Example)

```text
feature request
  → feature/01-plan      (Project Planner → plan.md)
  → feature/02-design    (System Architect → architecture-review.md / ADR)   [if needed]
  → feature/03-build     (Pair Programmer → src/, tests/, notes.md)
  → feature/04-review    (Code Reviewer → ai-review.md)
  → feature/05-fix       (→ updated code, mistakes.md)
  → feature/06-reflect   (Learning Coach → learning notes)
  → DONE
```

### Alternative Entry Points

| Entry Type | Workflow | Output |
|-----------|----------|--------|
| New feature | feature/* | plan, code, review, notes |
| Bug report | debugging/* | debugging session, fix, mistake log |
| New source | learning/* | source summary, exercises |
| Design question | architecture/* | ADR, architecture review |

## Control Flow

- Entry = one of: new feature, new bug, new source, new design question.
- The workflow selects the appropriate template + prompt + target folder.
- Human executes/edits artifacts; outputs land at deterministic paths.
- Reviews feed fixes, ADRs, or learning notes.
- If context is insufficient → create `open-questions.md` in the project folder.

## Memory Model

| Type | What It Contains | Where |
|------|-----------------|-------|
| **Short-term** | Current task, workflow step, active source, project folder, prompt constraints | In-memory during session |
| **Long-term** | ADRs, reviews, debugging sessions, learning notes, eval reports, mistakes logs | Files in repo at deterministic paths |
| **Retrieval** | Navigation by path → registry → folder convention | `registries/` + folder structure |

No hidden opaque memory. Everything is explicit and file-based.

## Failure Points to Watch

- Overly-broad prompts that cause inconsistent outputs
- Duplication between `docs/` content and project-level notes
- Turning every capability into an "agent" instead of a simpler prompt
- Missing naming conventions causing untrackable artifacts
- Reviews without follow-up — findings should produce fixes or ADRs
- Source learning without project linkage — every source should connect to a project task

### Mitigations

| Failure Point | Mitigation |
|---------------|------------|
| Overly-broad prompts | Keep each prompt scoped to one function; registry enforces boundaries |
| Duplication | Cross-reference from project notes to docs; use relative links |
| Agent sprawl | Before creating a new agent, consider if a task prompt or template suffices |
| Missing conventions | Document in monorepo-structure.md; enforce in reviews |
| Orphaned reviews | Feature workflow includes fix step (05-fix); reviews always produce follow-up |
| Unlinked learning | Source summary template includes "Link to Project Task" section |

*Last updated: 2026-08-06*
