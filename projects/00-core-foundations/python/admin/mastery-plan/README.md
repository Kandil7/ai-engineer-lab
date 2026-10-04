# Python Mastery Plan — Zero to Senior AI Engineer

A complete, measured plan to take `projects/00-core-foundations/python/` from a
syntax tutorial to a curriculum that produces a senior AI/backend engineer.

**Created:** 2026-07-29 · **Baseline:** commit `c4a4eec` · All numbers measured, not estimated.

---

## Start Here

| Read this | If you want |
|---|---|
| [00-MASTER-PLAN.md](00-MASTER-PLAN.md) | The full picture: baseline audit, 5 gaps, philosophy, tiers |
| [11-execution-roadmap.md](11-execution-roadmap.md) | What to do first, in what order, over 40 weeks |
| [10-remediation-backlog.md](10-remediation-backlog.md) | The 34 broken files and how to fix each |

**If you only do one thing:** fix `06-data-structures-algorithms/04-queues.py`
(it hangs forever) and `03-libraries/pandas/20-performance.py` (`SyntaxError`),
then add a CI gate. See [roadmap §8](11-execution-roadmap.md#8-getting-started).

---

## All Documents

| # | Document | Contents |
|---|---|---|
| 00 | [Master Plan](00-MASTER-PLAN.md) | Baseline, gap analysis, design philosophy, target state, tiers |
| 01 | [Content Standards](01-content-standards.md) | Canonical templates for exercises, lectures, glossaries, challenges, quizzes |
| 02 | [Phase 1 — Core Python](02-phase-1-core-python.md) | 41 → 52 topics; `_verify()` retrofit; 11 new stdlib topics |
| 03 | [Phase 2 — Advanced Python](03-phase-2-advanced-python.md) | 20 → 34 topics; concurrency, memory, typing, security |
| 04 | [Phase 3 — Data Libraries](04-phase-3-libraries.md) | pandas double-series fix; NumPy performance; Polars/PyArrow |
| 05 | [Phase 4 — Databases](05-phase-4-databases.md) | 23 → 64 topics; real Postgres, Redis, pgvector, vector stores |
| 06 | [Phase 5 — Backend](06-phase-5-backend.md) | FastAPI 25 → 52; observability, deployment, system design |
| 07 | [Phase 6 — DSA](07-phase-6-dsa.md) | 20 → 40 topics; interview patterns, DP, graphs |
| 08 | [Phases 7–9 — ML, MLOps, GenAI](08-phase-7-9-ml-mlops-genai.md) | ML depth; two entirely new phases |
| 09 | [Assessment System](09-assessment-system.md) | Quizzes, 200 code challenges, interview guides, 12 capstones |
| 10 | [Remediation Backlog](10-remediation-backlog.md) | 34 measured failures with root causes |
| 11 | [Execution Roadmap](11-execution-roadmap.md) | Sequencing, dependencies, parallelization, milestones |

---

## Baseline in One Table

| Metric | Now | Target |
|---|---|---|
| Phases | 7 | 9 |
| Exercise files | 277 | ~470 |
| Lectures / glossaries | 256 / 256 | ~450 / ~450 |
| Quizzes | 29 | ~120 |
| Code challenges | **0** | ~200 |
| Interview guides | 15 | ~45 |
| Capstones built | **0** (5 stubs) | 12 |
| Files that self-verify | **4 of 277** | all |
| **Failing files** | **34** | **0** |

---

## The Five Gaps

1. **Nothing is self-verifying** — 0 of 44 core files contain `assert`. No feedback loop.
2. **No cost model** — 0 of 20 advanced lectures mention complexity.
3. **Missing stdlib** — `logging`, `pytest`, `argparse`, `dataclasses`, `heapq`, `bisect`, `deque` all at 0 occurrences in Phase 1.
4. **No AI/production bridge** — `torch` 0 files (though installed), `openai` 0, `mlflow` 0, `Dockerfile` 0.
5. **Template drift** — three competing lecture formats; `Quick Reference` in 14 of 41.

Root cause: all 41 core files derive from W3Schools, which teaches syntax, not judgment.

---

## Two Honest Notes

**This is large.** ~900 new files across 40 weeks. Blocks 0–1 alone (10 weeks)
deliver a verified, correct 277-file curriculum — a legitimate stopping point if
scope needs cutting. Stop after milestone M2, not mid-authoring.

**Two decisions need your input** before execution:
- **Django** (R7): make it reference-only, or install and support it?
  Recommendation: reference-only. [Details](10-remediation-backlog.md#r7--django-cannot-run-at-all-20-files)
- **pandas** (R8): the 45-file double series — keep both renumbered into 38 topics,
  or drop one? Recommendation: keep both; the orphaned set is the more valuable
  content. [Details](10-remediation-backlog.md#r8--structural-pandas-double-series)

---

*Plan for the AI Engineer Lab. Reproduce any baseline number by running the named file.*
