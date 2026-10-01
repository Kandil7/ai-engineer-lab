# Progress Dashboard — Full-Stack AI Engineer Lab

> Quick-read status summary. Update at weekly and monthly reviews.

**Last updated:** 2026-09-30 (skills-mastery content + 11 challenge sets shipped; Production AI Systems track added 2026-09-30; previous 2026-08-02)

---

## Current Plan

**[Active Track — 10-Week AI Engineer](active-track-10-week.md)**, adopted 2026-08-02 by
[ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md).

The 12-month [`master-roadmap.md`](master-roadmap.md) is demoted to the **long track** — not
active. [`phase-2-athar-baligh.md`](phase-2-athar-baligh.md) follows the active track.

**Strategic follow-on:** [`../learning/design/production-ai-systems-engineer-roadmap.md`](../learning/design/production-ai-systems-engineer-roadmap.md)
— Production AI Systems / AI Platform track (P1–P8). Gap analysis 2026-09-30: active track
covers ~60–70% of the role (LLM application layer); missing depth is serving engines,
gateway/routing, cost enforcement, SLO operations, and experiment tracking. Start after A4/A6.

### Current focus

**Week 0/1** — CI green, `devmate stats` shipped; LLM layer in progress. Details:
[`../tracking/current-focus.md`](../tracking/current-focus.md).

---

## Where things actually stand

### Substantial completed work (June–July 2026)

| Area | Evidence | Scale |
| --- | --- | --- |
| Core Python | `python/01-core-python/` | 52 topics, lecture + glossary each |
| Advanced Python | `python/02-advanced-python/` | 38 topics — decorators, generators, context managers, async, type hints, dataclasses, ABC, functools, itertools, descriptors, metaclasses, threading, logging, patterns + production engineering (Unicode/Arabic text, SoC, code review, test strategy) |
| Data libraries | `python/03-libraries/` | numpy, pandas, matplotlib, scipy — pandas + matplotlib exercises finished 2026-07-29 |
| FastAPI | `python/05-web-frameworks/fastapi/` | 25 topics, each with an exercise |
| AI curriculum | `04-ai-engineering/` | 6,947 lines — LLM APIs, prompting, embeddings, RAG, agents, evaluation, deployment, multi-agent, safety |
| Agents curriculum | `04-ai-engineering/agents/` | 10 exercises + lectures + quizzes |
| Security curriculum | `04-ai-engineering/security/` | 10 exercises + lectures + quizzes |
| fast.ai track | `04-ai-engineering/fastai-deep-learning/` | 13 modules + quizzes |
| Workspace system | `.ai/`, `templates/`, `registries/` | 21 prompts, 21 workflows, 16 templates, 6 registries |
| ADRs | `docs/decisions/` | 5 |

### Skills-mastery delivery (2026-09-30)

Closing the Athar skills-table gaps in `projects/00-core-foundations/python/`:

| Deliverable | Evidence |
| --- | --- |
| 11 new topics (3-file format) | `02-advanced-python/35-38`, `04-databases/` migrations + backup, `10-system-design/01-05` |
| System design phase | contracts, queues, consistency, failure modes, ADRs |
| 11 challenge sets (Bronze/Silver/Gold) | measured guards (comparison budgets, call counts, tracemalloc ceilings) |
| Skills mastery map | [SKILLS_MASTERY_MAP.md](../../projects/00-core-foundations/python/SKILLS_MASTERY_MAP.md) |
| Verification | 186 tests: starter fails with NotImplementedError, solution passes 100% |

### The gap this dashboard exists to surface

**Written: 6,947 lines of AI teaching material. Running: zero AI services.**

```text
04-ai-engineering/rag-system/         → .gitkeep + README
04-ai-engineering/prompt-engineering/ → .gitkeep + README
04-ai-engineering/embeddings/         → .gitkeep + README
07-capstone/thanaweyagpt/*            → .gitkeep + README
```

`grep -c TODO` across all 19 AI exercise files returns 0 — they are finished reference
implementations, not practice scaffolds. The active track exists to invert this ratio, and the
governing rule (no new lectures until DevMate is deployed) is the mechanism.

### Not started

Go beyond two exercise scaffolds · frontend · deployment · CI *(week 0)* · SQL *(week 4)* ·
classical ML *(week 11+)* · MCP *(weeks 5–6)*.

---

## Snapshot

| Metric | Count | Notes |
| --- | --- | --- |
| Active-track milestones | 1 / 10 | A1 done; A2/A3 in progress |
| Long-track milestones | 0 / 13 | deferred under ADR-0004 |
| ADRs | 5 | 0004 and 0005 added 2026-08-02 |
| Python files | 354 | foundations |
| AI exercise lines | 6,947 | curriculum, not services |
| **Deployed services** | **0** | ← the number that matters; target week 4 |
| Daily logs | 1 | 2026-07-18 |
| Weekly reviews | 0 | protocol exists, unused |
| Source summaries | 1 | Go stdlib HTTP |
| Commits (last 30d) | 3 | 2026-07-29 most recent |

---

## At Risk

- **Output mode.** The demonstrated pattern is producing curriculum, not shipping systems.
  Watch for week-0 scope drifting into "let me first write a lecture on X."
- **Review cadence unused.** 1 daily log, 0 weekly reviews since June. The staleness test
  added in week 0 makes this visible rather than optional.
- **Commit gap.** Nothing since 2026-07-29. The plan requires daily commits.
- **Buffer discipline.** Weeks 11–12 are float. If they fill with new scope, the plan fails
  the same way its predecessor did.

---

## Active Track Progress

| Week | Milestone | Deliverable | Status |
| --- | --- | --- | --- |
| 0 | A1 | CI green + `devmate stats` | ✅ Done |
| 1 | A2 | LLM layer, traced and costed | 🔄 In Progress |
| 2–3 | A3 | RAG + eval harness + 2 ADRs | 🔄 In Progress |
| 4 | A4 | **Public URL** + SQL sprint | 🔲 Planned |
| 5–6 | A5 | Agent, 4 tools, MCP server | 🔲 Planned |
| 7 | A6 | Cache, guardrails, hardening | 🔲 Planned |
| 8 | A7 | Portfolio | 🔲 Planned |
| 9–10 | A8, A9 | 40 applications, first interview | 🔲 Planned |
| 11+ | A10 | Deferred ML sprint | 🔲 Planned |

---

## Long Track (not active)

| Phase | Status |
| --- | --- |
| 0 — Foundations | Partial — Python well beyond target; Go and web barely started |
| 1 — Backend (Go) | Deferred |
| 2 — Frontend | Deferred |
| 3 — AI Fundamentals | Superseded by the active track |
| 4 — RAG Systems | Superseded — active track weeks 2–3 |
| 5 — AI Agents | Superseded — active track weeks 5–6 |
| 6 — System Design + DevOps | Partial — active track weeks 0, 4, 7 |
| 7 — Capstone (ThanaweyaGPT) | Deferred; DevMate is the active vehicle |

---

## Last Period

**2026-06-26 → 2026-08-02**

- **Shipped:** matplotlib exercises 1–20, pandas exercises 1–24, inner-classes lecture, SciPy
  lectures + tests, Django lectures, fast.ai modules 10–13, AI security quizzes, agent quizzes,
  LEARNING_SYSTEM.md, WEEKLY_PROTOCOL.md
- **Not shipped:** any running service; any deployment; any evaluation run
- **Learned:** the workspace can produce curriculum at high volume. The constraint is not
  capability or effort — it is that the output was pointed at teaching material instead of at
  a system.
- **Changed:** plans reconciled, tracking corrected, output mode constrained by an explicit rule
