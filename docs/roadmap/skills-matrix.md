# Skills Matrix — AI Engineer Lab

> Track skill levels across the journey. Update monthly.
> Scale: 1 (aware) → 10 (authority). Targets set by the
> [active track](active-track-10-week.md).

**Last updated:** 2026-09-30 (added Production AI Systems rows; previous 2026-08-02)

---

## Assessment principle

**A level requires evidence — a file path, a passing test, a deployed URL.** Study without a
shipped artifact caps a skill at level 3 ("can use with documentation"), no matter how much
material was covered. This is why several rows below show a large gap between the volume of
material studied and the level assigned.

---

## Active-track skills

Targets are the level needed to interview credibly for a remote AI engineer role.

| Skill | Target | Current | Evidence | Next step |
| --- | --- | --- | --- | --- |
| Python (language) | 7 | **6** | `python/01-core-python/` (52 topics), `02-advanced-python/` (38 topics) | Apply in a real service, not exercises |
| Python (production) | 7 | **3** | `02-advanced-python/35-38` (Unicode, SoC, review, test strategy) + challenge sets | Apply in a real service, not exercises — week 0 |
| Clean code / typing | 6 | **4** | `02-advanced-python/36-37` (SoC, refactoring) + challenge sets with structural guards | ruff + mypy green in CI — week 0 |
| Testing (pytest) | 6 | **4** | `python/tests/`, `02-advanced-python/18,38` + regression-gate challenge set | Test a real service; LLM-aware testing — week 7 |
| Git | 7 | **4** | 25+ commits, 3 PRs | Rebase, conflict resolution, 5 clean PRs — week 0 |
| **CI/CD** | 6 | **1** | none | GitHub Actions green — week 0 |
| FastAPI | 7 | **4** | `05-web-frameworks/fastapi/` (25 topics + exercises) | Ship a real API — week 4 |
| LLM APIs | 7 | **2** | curriculum only | Streaming, structured outputs, retries — week 1 |
| Prompt engineering | 7 | **3** | `04-ai-engineering/ai-automation/02-prompt-engineering.py` | Versioned templates in a running system — week 1 |
| **Observability** | 6 | **1** | none | Langfuse + cost tracking — week 1 |
| Embeddings | 6 | **2** | curriculum only | Real corpus, measured — week 2 |
| Chunking | 7 | **2** | curriculum only | 3 strategies compared on a golden set — week 2 |
| Vector DB (Qdrant) | 7 | **2** | cheat-sheet, compose service | Ingest and query at scale — week 2 |
| RAG (end-to-end) | 8 | **2** | 835 lines of exercise code, nothing running | Working pipeline with metrics — weeks 2–3 |
| **Evaluation** | 7 | **1** | `evaluations/` scaffolded, empty | Golden set + RAGAS — week 2 |
| **SQL** | 6 | **2** | `04-databases/` (sql-fundamentals, sqlite, migrations/backup topics) | Real schema, indexes, query plans — week 4 |
| Docker | 6 | **2** | compose exists; cheat-sheet | Multi-stage build, deploy — week 4 |
| Deployment | 6 | **1** | none | Public URL — week 4 |
| Agents | 7 | **2** | 10 exercises + lectures, nothing running | 4 tools, ReAct, step caps — weeks 5–6 |
| **MCP** | 6 | **1** | mentioned in 2 quizzes | Build an MCP server — week 6 |
| Caching (Redis) | 5 | **1** | compose service only | Semantic cache with hit rate — week 7 |
| Guardrails / security | 6 | **2** | 10 security exercises | Block real injection attempts — week 7 |
| System design | 6 | **3** | `10-system-design/` (5 topics + 5 challenge sets), 2 design docs, 5 ADRs | Explain DevMate's architecture cold — week 8 |
| Technical English | 7 | **4** | repo docs in English | Recorded explanations, mocks — week 8 |

### Reading this table

The pattern is consistent: **curriculum-level exposure (2) with production-level targets
(6–8)**. That gap is not a knowledge problem — the material has been covered in depth. It is
an evidence problem, and the active track is structured to close it week by week.

Rows in **bold** are at level 1 — genuinely untouched, not merely unapplied.

---

## Production AI Systems track (deferred until P0 gate)

Targets from [`../learning/design/production-ai-systems-engineer-roadmap.md`](../learning/design/production-ai-systems-engineer-roadmap.md).
Current levels from the 2026-09-30 repo audit.

| Skill | Target | Current | Evidence | Next step |
| --- | --- | --- | --- | --- |
| Model serving (vLLM/TGI) | 7 | **2** | curriculum only; no server started | P5 lab on RTX 5000 |
| LLMOps release gates | 7 | **3** | llmops README; prompts versioned in DevMate | P1 eval gate + P6 rollback |
| Observability ops (SLOs) | 7 | **4** | Langfuse code + compose service | P2 dashboards, SLOs, alerts |
| Cost engineering | 7 | **3** | `obs/cost.py` ledger only | P3 budgets + routing |
| Reliability / AI SRE | 7 | **3** | client fallback exists; load/integration tests empty | P4 |
| GPU / K8s orchestration | 5–6 | **1** | READMEs describe unbuilt manifests | P7 only if postings demand |
| Evaluation infrastructure | 8 | **3** | golden set + baseline; harness missing | P1 |
| Gateway / multi-tenant routing | 6 | **1** | 3 providers in client, no router | P6 |
| Experiment tracking (MLflow+) | 5 | **1** | interview questions only | P5–P6 as needed |

---

## Long-track skills (deferred)

| Skill | Target | Current | Status |
| --- | --- | --- | --- |
| PostgreSQL (depth) | 6 | 2 | Partial — week 4 SQL sprint covers the basics |
| ML fundamentals | 5 | 2 | Deferred to week 11+ (A10) |
| PyTorch | 4 | 1 | Deferred to week 11+ (A10) |
| Kubernetes | 3 | 1 | Post-employment |

---

## Level definitions

| Level | Description |
| --- | --- |
| 1 | Aware — know what it is, no hands-on |
| 2 | Exposure — completed tutorials or exercises, nothing shipped |
| 3 | Basic — can use with documentation open |
| 4 | Working — can build simple things independently |
| 5 | Working+ — can build moderate features and debug them |
| 6 | Intermediate — can architect solutions and handle edge cases |
| 7 | Advanced — can teach it, optimize it, defend design choices |
| 8 | Expert — production-grade mastery, performance tuning |
| 9 | Specialist — deep expertise, contributes to the ecosystem |
| 10 | Authority — recognized expert, shapes best practice |

---

## Target progression by week

| Week | Skills upgraded |
| --- | --- |
| 0 | CI 1→5 · Git 4→6 · Clean code 4→6 · Python production 3→4 |
| 1 | LLM APIs 2→5 · Observability 1→5 · Prompt eng 3→5 |
| 2–3 | Embeddings 2→5 · Chunking 2→6 · Qdrant 2→6 · RAG 2→6 · Evaluation 1→6 |
| 4 | FastAPI 4→6 · SQL 2→5 · Docker 2→5 · Deployment 1→5 |
| 5–6 | Agents 2→6 · MCP 1→5 |
| 7 | Caching 1→5 · Guardrails 2→5 · Testing 4→6 |
| 8 | System design 3→5 · Technical English 4→6 |
| 11+ | ML fundamentals 2→4 · PyTorch 1→3 |

---

## Monthly review check

1. Update `Current` — **only with evidence**; a path, a test, or a URL.
2. Verify every `Evidence` path still exists.
3. Refresh `Next step` for anything completed.
4. Flag any active-track skill more than 3 levels below target at its scheduled week.
5. Re-audit against [`../reference/python-ai-engineer-checklist.md`](../reference/python-ai-engineer-checklist.md).
