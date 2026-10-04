# Roadmap — Long Track (not active)

> ## ⚠️ Not the active plan
>
> The plan of record is
> **[`docs/roadmap/active-track-10-week.md`](docs/roadmap/active-track-10-week.md)**, adopted
> 2026-08-02 by [ADR-0004](docs/decisions/0004-adopt-10-week-ai-engineer-track.md).
>
> This file and [`docs/product/12-month-plan.md`](docs/product/12-month-plan.md) describe the
> **long track**. The Go and frontend phases were **removed** to focus on AI Engineering; the
> ThanaweyaGPT capstone and the AI/system-design phases remain deferred. Its AI phases (3–5)
> are superseded by the active track's weeks 1–6.
>
> Retained because the phase structure, the source→artifact rule, and the resource mapping
> stay valid for when the long track resumes.

This roadmap maps **learning phases** to **concrete projects** and to the **build phases**
defined in the architecture spec. Each "phase" is a sprint of 2–4 weeks, not a single day.

---

## Learning Phases → Projects → Resources

| Phase | Theme | Primary Project(s) | Key Resources |
| ----- | ----- | ------------------- |---------------|
| 0 | Foundations | `projects/00-core-foundations/` | FreeCodeCamp, Odin Project, YouTube Crash Course |
| 3 | AI fundamentals + Prompts | `projects/04-ai-engineering/prompt-engineering` | ML for Beginners, Karpathy, HF NLP Course |
| 4 | RAG systems | `projects/04-ai-engineering/rag-system` | DeepLearning.AI RAG, Illustrated Transformer |
| 5 | AI agents | `projects/04-ai-engineering/agents` | HF Agents, Berkeley LLM Agents, Arize AI |
| 6 | System design + DevOps | `projects/05-system-design`, `projects/06-devops` | Docker course, System design resources |
| 7 | Capstone | `projects/07-capstone/thanaweyagpt` | All previous resources combined |

---

## Monthly Timeline

| Month | Focus | Resources | Lab Projects |
|-------|-------|-----------|-------------|
| 1 | HTML/CSS/JS basics | FreeCodeCamp, YouTube Crash Course | `00-core-foundations/` |
| 2 | JavaScript fundamentals | FreeCodeCamp, Odin Project | `00-core-foundations/` |
| 3 | Git + review | Pro Git, Odin Project | `00-core-foundations/git-linux/` |
| 8 | PostgreSQL + Redis | Official docs | `03-databases/` |
| 9 | Docker + deployment | Docker course | `06-devops/docker/` |
| 10 | Python for AI + LLMs | ML for Beginners, Karpathy | `04-ai-engineering/` |
| 11 | RAG pipeline | DeepLearning.AI RAG, HF NLP | `04-ai-engineering/rag-system/` |
| 12 | Agents + capstone | HF Agents, Berkeley, Arize | `04-ai-engineering/agents/` + capstone |

---

## Build Phases (implementation status)

### Phase 0 — Foundations ✅
Repo skeleton, README, ROADMAP, all templates, core role prompts, registries, ADR system.
**Acceptance:** deterministic folder structure exists; first templates + prompts available.

### Phase 1 — Core MVP ✅
One end-to-end feature workflow operational, with the full artifact chain:
`feature-spec → plan → architecture-review → build → ai-review → fix → reflect`.
**Acceptance:** at least one feature completed with all artifacts; no missing template in path.

### Phase 2 — Reliability
Learning workflows for docs/repo/book/notebook; source templates; prompt audits; tests for
prompts/workflows/templates.
**Acceptance:** source-learning path works on 2–3 real sources; prompt registry updated.

### Phase 3 — Scale / Optimization
Scaffolding scripts, repo validation tests, evaluation folders, improved registries,
project-level deep dives.
**Acceptance:** new project/service can be scaffolded rapidly; reviews + ADRs indexed.

### Phase 4 — Advanced Features
RAG eval harness, project-specific templates, advanced architecture docs, CI hooks, optional
local retrieval.
**Acceptance:** RAG project has eval reports + ADRs + design docs; capstone structure executable.

---

## Milestone 1 — Operational MVP Workspace

Considered done when one feature is completed with:
feature spec · plan · architecture note/ADR · implementation notes · code review ·
debug doc (if needed) · reflection/learning note. **(Reached in Phase 1.)**

---

## Source → Artifact Rule

Every source studied MUST produce a tangible artifact:

```
Source → Read/Watch
    ↓
Extract: Key concepts + example + exercise
    ↓
Apply in lab project
    ↓
Document in docs/learning/
    ↓
Review using .ai/prompts/
    ↓
Reflect in docs/learning/notes/weekly/
```
