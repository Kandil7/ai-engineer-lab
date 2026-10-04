# Weekly Protocol — Daily Loop, Weekly Review, Artifact Rules

> The operating cadence of this workspace. Executed daily; reviewed every Saturday.
>
> **Consolidated 2026-08-02.** This file absorbs the former `docs/LEARNING_SYSTEM.md`, whose
> directory references (`docs/daily-logs/`, `docs/weekly-reviews/`, `docs/adrs/`,
> `/projects/athar/`) pointed at paths that do not exist in this repo. All paths below are
> verified.

---

## 1. Mission

> **Every hour of learning produces an artifact in the repo.**

Not notes for their own sake — a file that later work can build on, review, or cite. A session
that ends with nothing committed did not happen.

---

## 2. Daily loop

Aligned to the [active track](roadmap/active-track-10-week.md), 5+ hours:

| Block | Time | Activity | Artifact |
| --- | --- | --- | --- |
| **Build** | 3h | The week's deliverable — code first | code + tests |
| **Learn** | 1h | One topic, docs-first, **after** building it | `docs/learning/source-summaries/` |
| **Review** | 1h | AI code review, debugging log | `ai-review.md`, `mistakes.md` |
| **Recall** | 30m | Explain today's work without notes; plan tomorrow | `docs/learning/daily-logs/YYYY-MM-DD.md` |

Build precedes learn deliberately. Reading a chapter before writing the code produces
recognition; reading it after produces answers to questions you actually have.

---

## 3. Artifact locations

**These are the real paths.** Nothing lands anywhere else.

| Type | Location | Created by |
| --- | --- | --- |
| Daily log | `docs/learning/daily-logs/YYYY-MM-DD.md` | `infra/scripts/new-daily-log.ps1` |
| Weekly review | `docs/reviews/weekly/YYYY-WXX.md` | `infra/scripts/new-review.ps1` |
| Monthly review | `docs/reviews/monthly/YYYY-MM.md` | `infra/scripts/new-review.ps1` |
| ADR | `docs/decisions/NNNN-kebab-title.md` | `infra/scripts/new-adr.ps1` |
| Source summary | `docs/learning/source-summaries/<source>.md` | `templates/source-*.template.md` |
| Deep dive | `docs/learning/deep-dives/<topic>.md` | manual |
| Eval report | `evaluations/rag/reports/<date>-<subject>.md` | `templates/evaluation-report.template.md` |
| Feature artifacts | `<project>/plan.md`, `ai-review.md`, `notes.md`, `mistakes.md` | `.ai/workflows/feature/` |

---

## 4. Weekly review

**Every Saturday.** File: `docs/reviews/weekly/YYYY-WXX.md`

```markdown
# Weekly Review — Week WXX (YYYY-MM-DD)

## Accomplished
- [ ]

## Artifacts Produced
| Artifact | Location | Status |
|----------|----------|--------|

## Blockers & Resolutions
- Blocker:
  Resolution:

## Metrics
- Hours: __h
- Commits: __
- Milestone progress: A_ → __%
- Sources studied: __
- **Services running: __**   ← the number that matters

## Next Week
| Day | Focus | Target Artifact |
|-----|-------|-----------------|
| Sun | | |
| Mon | | |
| Tue | | |
| Wed | | |
| Thu | | |
| Fri | | |
| Sat | Weekly review | YYYY-WXX.md |

## Reflections
```

Then update: [`docs/tracking/current-focus.md`](tracking/current-focus.md) (**required** — a
staleness test fails the suite after 8 days), and
[`docs/roadmap/progress-dashboard.md`](roadmap/progress-dashboard.md).

---

## 5. Weekly success criteria

- **1+ commit per day** with a real artifact
- Weekly review written **every Saturday**
- `current-focus.md` updated to the next window
- 1+ source studied → 1 summary in `docs/learning/source-summaries/`
- The week's milestone deliverable shipped, or the slip explained in the review

---

## 6. Monthly review

Every 4 weeks, additionally:

- **The 30-day rule** — something must work end to end. Not "progressed": working.
- Update [`skills-matrix.md`](roadmap/skills-matrix.md) — **evidence only**; a path, a test, or
  a URL. Study without a shipped artifact caps a skill at level 3.
- Re-audit [`../reference/python-ai-engineer-checklist.md`](reference/python-ai-engineer-checklist.md)
- Update [`milestones.md`](roadmap/milestones.md) statuses
- Ask: is the plan still right? Record any change as an ADR, not a silent edit.

---

## 7. Source → artifact rule

Every source studied produces something:

```text
Source (book / docs / repo / notebook)
    ↓  read or watch
Extract: key concepts + one example + one exercise
    ↓
Apply in the active project
    ↓
Document in docs/learning/source-summaries/
    ↓
Review using .ai/prompts/
    ↓
Reflect in the weekly review
```

Workflows: [`.ai/workflows/learning/`](../.ai/workflows/learning/) — one per source type.

---

## 8. Learning tracks

| Track | Status | Where |
| --- | --- | --- |
| **DevMate** — RAG, agents, MCP, production | **Active** | [`active-track-10-week.md`](roadmap/active-track-10-week.md) |
| Athar — Arabic RAG | Phase 2 | [`phase-2-athar-baligh.md`](roadmap/phase-2-athar-baligh.md) |
| Baligh — Arabic LLM fine-tuning | Phase 2 | [`phase-2-athar-baligh.md`](roadmap/phase-2-athar-baligh.md) |
| Classical ML | Week 11+ | [`reference/ml-fundamentals-map.md`](reference/ml-fundamentals-map.md) |

---

## 9. Standing rules

1. Stuck longer than **45 minutes** → log it in `mistakes.md`, move on, return later.
2. Documentation is written **while** building, never after.
3. **Commit daily**, minimum.
4. Last block of the day is **review**, not new material.
5. Reaching for another source "to be sure you understood" is **procrastination**. Return to
   the code.
6. **No new lecture, glossary, or quiz until DevMate is deployed** — the governing rule from
   [ADR-0004](decisions/0004-adopt-10-week-ai-engineer-track.md).

*Last updated: 2026-08-02*
