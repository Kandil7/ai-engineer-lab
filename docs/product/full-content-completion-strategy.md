# Full Learning Content & Roadmap — Completion Plan

> How to finish **every section and every topic** of the production-AI roadmap, using the
> workspace's existing conventions. This is the execution plan for two source documents:
>
> - `roadmap/production-ai-systems-engineer.md` — the 11 competency areas, tool stack,
>   learning phases, and portfolio bar.
> - `docs/roadmap/production-ai-systems-engineer.md` — the 12 axes and the P1–P8
>   production phases (with the current evidence scoreboard).
>
> Companions: [`learning-strategy.md`](learning-strategy.md) (the study loop),
> `IMPLEMENTATION-GUIDE.md` (the lecture standard), and
> [`../roadmap/production-skills-matrix.md`](../roadmap/production-skills-matrix.md)
> (the evidence scoreboard this plan updates).

**Last updated:** 2026-10-02

---

## 1. What "complete" means

A roadmap section is complete only when **both** hold. Content without an artifact is
study; an artifact without content is a demo. Neither counts alone.

1. **The concept is taught** in a full-detail teaching unit (below).
2. **A proof artifact exists** that the skills matrix can cite: a path, a passing test, a
   measured number, a URL, or an ADR.

### 1a. The lecture standard (per `.md`)

A lecture is "full detail" when it follows `IMPLEMENTATION-GUIDE.md`:

```text
# <Module> NN: <Topic>
## Topic Overview              (2-3 paragraphs: what, why, what is hard)
## Learning Objectives         (5-7 bullets)
## Prerequisites               (1-3 bullets)
## 1..7. <Concept>             (each: idea, analogy, complete code, when it fails,
                               connection to the exit test; ### subsections)
## Real-World Application
## Common Mistakes             (5-7, with examples)
## Key Takeaways               (5 bullets)
## Self-Check Questions        (3-6)
## Further Reading / Connections
```

Target: **250-400 lines / at least 6.5 KB**, versus the ~90-line abbreviated form.
The physical-line proxy undercounts unwrapped paragraphs; judge by section coverage and
character count too. A lecture under 4 KB is "thin" and is a work item.

### 1b. The teaching-unit standard (per topic)

A topic is complete when its folder holds all four artifacts:

| Artifact | File pattern | Shape |
| --- | --- | --- |
| Lecture | `<topic>-lecture.md` | the standard above |
| Glossary | `<topic>-glossary.md` | Quick Reference Table + Alphabetical Glossary |
| Quiz | `<topic>-quiz.md` (or `quizzes/`, `challenges/NN/quiz.md`) | Score Tracker + 8-10 questions + reveal + scoring guide |
| Exercise | `<topic>.py` (layout varies) | runnable; `--verify` self-checks pass offline |

The exercise's `--verify` is the proof the content is executable, not just prose.

### 1c. The verification gate

Every completed batch must pass:

```powershell
# content gate (DevMate only; other projects self-verify)
& .venv/Scripts/python.exe -m pytest -q          # cwd projects/04-ai-engineering/devmate
# workspace gates (all five, warnings fail)
powershell -NoProfile -ExecutionPolicy Bypass -File tests/prompts/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/workflows/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/templates/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/registries/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/repo-structure/validate.ps1
# docs gate: 0 broken relative links under docs/
```

---

## 2. Cure audit (corrected 2026-10-02)

The prior audit under-counted quizzes because it missed two nested layouts. Measured
directly this session:

| Measure | Count |
| --- | --- |
| Lecture files | 598 |
| With a glossary | 598 (100%) |
| **With a quiz in any layout** | **186** |
| **Without any quiz** | **412** |
| Thin lectures (< 4 KB) | 99 (100% inside `python`) |
| Lectures with a runnable exercise | 538* |

\* Exercise count is a lower bound: `agents`, `ai-automation`, `fastai-deep-learning`,
and `security` ship `.py` files whose names do not match the lecture stem, so the
automated check under-reports them. Verify per unit during its batch.

### Quiz layouts (all three count as complete)

- next to the lecture: `<topic>-quiz.md`
- sibling folder: `quizzes/<topic>-quiz.md` (e.g. `08-mlops`, `09-genai`)
- challenge folder: `challenges/NN-topic/quiz.md` (e.g. `python/10-system-design`)

### Where the 412 missing quizzes and 99 thin lectures sit

Every gap is in the legacy `00-core-foundations/python` curriculum (481 lectures), except
**one** missing quiz in `04-ai-engineering/prompt-engineering/03-chain-of-thought`.

| Module | Lectures | Have quiz | **Need quiz** | **Thin** |
| --- | --- | --- | --- | --- |
| `python/01-core-python` | 53 | 14 | **39** | 1 |
| `python/02-advanced-python` | 38 | 4 | **34** | 0 |
| `python/03-libraries` | 137 | 0 | **137** | 36 |
| `python/04-databases` | 73 | 5 | **68** | 32 |
| `python/05-web-frameworks` | 74 | 1 | **73** | 20 |
| `python/06-data-structures-algorithms` | 20 | 0 | **20** | 1 |
| `python/07-machine-learning` | 40 | 0 | **40** | 9 |
| `python/08-mlops` | 16 | 16 | 0 (done) | 0 |
| `python/09-genai` | 25 | 25 | 0 (done) | 0 |
| `python/10-system-design` | 5 | 5 | 0 (done) | 0 |
| `prompt-engineering/03-chain-of-thought` | 1 | 0 | **1** | 0 |
| **Total** | **482** | **70** | **412** | **99** |

Thin lists (exact files) are in §5; they are dominated by `03-libraries` (matplotlib 3-D
and numpy/scipy plotting), `04-databases` (PostgreSQL/Redis/SQL basics), and
`05-web-frameworks` (all 20 Django basics at ~3 KB each).

---

## 3. Traceability — every roadmap section, mapped

### 3.1 The 11 competency areas → repo home → proof → status

Status legend: **Provable** (evidence exists) · **Partial** (some evidence) · **Not yet**.

| # | Area | Learning home | Proof artifact | Status | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | **Data engineering** | `00-core-foundations/data-engineering/` (15), `03-databases/*`, `athar-lab/` | athar contracts + deterministic CLI; `devmate/ingest/` | Partial | New units done: 08-15 (batch/streaming, ETL/CDC, lakehouse, data quality, feature stores/pipelines, versioning/lineage, storage/DB); remaining: real Shamela ingestion (A3) |
| 2 | **ML development** | `python/07-machine-learning/` (40), `applied-ml/` (5), `fine-tuning/` (6) | `applied-ml/05-baseline-intent-classifier/` (12/12, macro-F1 1.0) | Partial | Quizzes + 9 thin in 07-ml; add pruning/distillation unit |
| 3 | **MLOps core** | `python/08-mlops/` (16), `06-devops/{ci-cd,deployment,llmops}/` | ruff/mypy/pytest CI; prompt golden tests | Partial | Experiment-tracking lab; eval CI gate (P1); registry + promote/rollback (P6) |
| 4 | **Cloud infra** | `06-devops/docker/`, `infra/docker/`, `devmate/docker/Dockerfile` | compose stack; image builds | Partial | K8s manifests (P7, demand-gated); cloud notes post-employment |
| 5 | **Serving & APIs** | `model-serving/` (4), `python/08-mlops/07-08`, `devmate/api/` | `devmate` `/ask` SSE + health | Partial | vLLM/TTFT lab (P5); Docker for the API; gRPC note |
| 6 | **Monitoring & observability** | `devmate/obs/`, `ai-evaluation/` (7), `python/08-mlops` | `obs/cost.py`; Langfuse wiring | Partial | SLOs + alerts + runbooks (P2); drift test (P4) |
| 7 | **Scalability & performance** | `devmate/cache/`, `python/10-system-design/` (5) | `semantic_cache.py`; failure-modes doc | Partial | Load tests + dynamic batching (P4/P5) |
| 8 | **Security & compliance** | `security/` (10), `python/09-genai/*safety*`, `rag-system/08-context-security` | `devmate/guards/guardrails.py` | Partial | Threat model; red-team suite (P4) |
| 9 | **Testing & QA** | `devmate/tests/`, `python/08-mlops`, `tests/*/validate.ps1` | unit tests; 5 validators; link check | Partial | Real integration + load suites (P4) |
| 10 | **Cost optimization** | `devmate/obs/cost.py`, `python/08-mlops`, `09-genai/18-caching-and-cost` | cost ledger | Partial | Budgets + routing + chargeback (P3) |
| 11 | **Team & leadership** | `docs/`, `.ai/`, `python/02-advanced-python/37-code-review-and-refactoring` | ADR set; prompt/workflow registries; this doc | Partial | Runbooks (P6); public case study + OSS PR (P8) |

Tool-stack table and learning-phases checklist map onto the same rows; the tool stack is
satisfied by the proof artifacts above (Docker/compose, CI, MLflow in P1/P6, Prometheus in
P2). The formal-education items the top-level roadmap lists (certificates, conferences)
are **out of scope** per `scope-definition.md` and carry no repo artifact.

### 3.2 The 12 axes → same artifacts (scoreboard)

`docs/roadmap/production-skills-matrix.md` already holds the 12-axis rows with status.
This plan changes no status by itself; it supplies the work that moves each row. The four
weakest (the "first empty box"), in order: **axis 10 (SRE)**, **axis 7 (live eval + CI
gate)**, **axis 11 (threat model)**, **axis 8 (inference benchmark)**.

### 3.3 `docs/product/` — the operating contract

| Product doc | Rule it imposes | How this plan satisfies it |
| --- | --- | --- |
| `ai-learning-operating-manual.md` | Every session leaves an artifact; AI explains/reviews, learner owns logic | Each batch writes quizzes/lectures (artifacts) and passes the gate |
| `learning-strategy.md` | Source → artifact pipeline; active recall + spacing | Quizzes are the recall instrument; glossary is the spaced-review sheet |
| `scope-definition.md` | Out: production SaaS, autonomous loops, K8s/prod infra, PII | P7 is demand-gated and labelled; no tenant data touched |
| `feature-priorities.md` | P0-P3 ordering; quality non-negotiable at P0/P1 | Content and P1/P2 are P0/P1; P7/P8 are P2/P3 |
| `workspace-goals.md` | 5-axis, quality targets, evidence | Matrix rows + validators are the evidence |
| `12-month-plan.md` | Superseded 2026-08-02 (ADR-0004) | Retained only for Go/frontend/DevOps post-employment |

---

## 4. How to complete one unit (the pipeline)

Run this loop for one `<axis>/<module>/` at a time.

1. **Pick the unit** by the order in §5. Read the existing `<topic>-lecture.md` and the
   exercise.
2. **Expand the lecture** to the §1a standard if it is thin. Preserve existing content; add
   the missing sections.
3. **Refresh the glossary** (`<topic>-glossary.md`) to the §1b shape.
4. **Write the quiz** with 8-10 questions, a score tracker, reveal blocks, and a scoring
   guide. Tie the hard questions to the exit test.
5. **Confirm or extend the exercise** so it runs offline with `--verify`; if one exists,
   add the missing assertions.
6. **Run the gate** (§1c). Fix until green.
7. **Update the matrix** (`production-skills-matrix.md`) if the unit closes an axis gap.

Order within a unit: lecture, glossary, quiz, exercise — the quiz and exercise derive from
the lecture, so writing it first keeps them consistent.

### Batching and parallelization

- One **module** (or one sub-folder of a large module) per batch. A batch is done when its
  units pass the gate.
- Do not mix axes in a batch; context switching costs more than parallelism gains.
- Large modules (`03-libraries` 137, `05-web-frameworks` 74, `04-databases` 73) are
  sub-batched by their own sub-folders (`numpy`, `pandas`, `matplotlib`, `scipy`, `polars`;
  `django`, `fastapi`; the 7 database sub-folders).
- Parallelize only after the format is locked by a first sub-batch in the module. Quizzes
  are independent and well-suited to subagents; lectures and the gate stay serial.

---

## 5. The order of work

Two workstreams. Content is mechanical, batches cleanly, and can start now. Platform
phases are gated by the active track (§5.2) and must not steal Build time from weeks 0-10.

### 5.1 Content workstream (start here)

| Order | Module | Lectures | Need quiz | Thin | Batches |
| --- | --- | --- | --- | --- | --- |
| done | `python/08-mlops` | 16 | 0 | 0 | 16 quizzes ✅ |
| done | `python/09-genai` | 25 | 0 | 0 | 25 quizzes ✅ |
| done | `python/06-data-structures-algorithms` | 20 | 0 | 0 | 20 quizzes + 1 lecture ✅ |
| done | `python/02-advanced-python` | 38 | 0 | 0 | 34 quizzes (+4 existing) ✅ |
| done | `python/07-machine-learning` | 40 | 0 | 0 | 40 quizzes + 9 lectures ✅ |
| 1 | `python/01-core-python` | 53 | 39 | 1 | 2 |
| 4 | `python/01-core-python` | 53 | 39 | 1 | 2 |
| 5 | `python/05-web-frameworks` | 74 | 73 | 20 | fastapi (52), django (22) |
| 6 | `python/04-databases` | 73 | 68 | 32 | 7 sub-folders |
| 7 | `python/03-libraries` | 137 | 137 | 36 | numpy (34), pandas (51), matplotlib (30), scipy (16), polars (6) |
| 8 | `prompt-engineering/03-chain-of-thought` | 1 | 1 | 0 | 1 |

Thin-lecture lists for the expansion work:

- `01-core-python`: `02-get-started-lecture.md`
- `03-libraries` (36): matplotlib 3-D/plotting (`04-markers`, `05-line`, `06-grid`,
  `06-labels`, `07-box-violin`, `08-subplot`, `09-3d-plots`, `09-scatter`, `10-bars`,
  `11-animation`, `11-histograms`, `12-pie-charts`, `13-box-plots`, `14-area-plots`,
  `15-contour-plots`, `16-wireframe`, `17-surface-plot`, `18-3d-scatter`, `19-3d-line`,
  `20-3d-surface`), numpy (`01-introduction`, `02-getting-started`, `03-basic-functions`,
  `04-statistics`, `05-integration`, `06-interpolation`, `08-linear-algebra`, `09-fft`,
  `10-spatial-data`, `11-image-processing`, `12-io`, `20-styling`),
  scipy (`04-statistics`, `07-optimization`)
- `04-databases` (32): the PostgreSQL/SQL/Redis basics (`01`–`12` as listed in §2)
- `05-web-frameworks` (20): all 20 Django basics (`01`–`20`)
- `06-dsa`: `12-linear-search-lecture.md`
- `07-machine-learning` (9): `24`–`32` (pipelines, leakage, validation, metrics,
  calibration, imbalance, boosting, feature engineering/selection)

### 5.2 Platform workstream (P-track, after the A-track gate)

Gate to start (from `docs/roadmap/production-ai-systems-engineer.md`): A4 (public URL) and
A6 (hardening) done; `eval/` harness prints a table; P-track does not steal build time.

| Phase | Deliverable → proof | Axis closed |
| --- | --- | --- |
| P1 | Live RAG eval + judge pinning + **CI eval gate** | 7 |
| P2 | SLOs, dashboard, alert rules, error taxonomy | 6, 10 |
| P3 | Cost budgets, model routing, chargeback, break-even ADR | 10 |
| P4 | Load + integration tests, failure-modes v2, red-team schedule | 9, 11 |
| P5 | vLLM serving lab, TTFT/TPOT report, quant comparison | 8 |
| P6 | Gateway, eval-gated promote/rollback, runbooks | 3, 11 |
| P7 | K8s manifests (demand-gated) | 4 |
| P8 | Live URL + README-as-spec + OSS PR + case study | 12 |

### 5.3 New units (small, high-value)

- **Axis 5** — dataset/embedding/index versioning manifest (a DVC-style pointer +
  reproducibility test in `athar-lab` or `devmate/ingest`).
- **Axis 8** — inference benchmark unit (real vLLM TTFT/TPOT, replacing the arithmetic-only
  `model-serving/02-self-hosted-models.py`).
- **Axis 2** — networking unit (HTTP/DNS/TLS basics; the only empty sub-area).
- **Unit-integrity** — verify exercises for `agents`, `ai-automation`,
  `fastai-deep-learning`, `security` (their `.py` layouts differ from the check).

---

## 6. Per-unit checklist

```text
[ ] <topic>-lecture.md has all 9 sections, >= 250 lines / 6.5 KB (or >= 4 KB minimum)
[ ] <topic>-glossary.md has the quick table + alphabetical entries
[ ] <topic>-quiz.md has 8-10 questions + reveal + scoring guide
[ ] <topic>.py runs offline and `--verify` exits 0 (layout verified per area)
[ ] no broken relative links
[ ] five validators exit 0
[ ] production-skills-matrix.md row updated if the unit closes an axis gap
```

---

## 7. Conventions

- **No frontmatter** on lecture/glossary/quiz/exercise files. They are content, not
  governed `.ai` assets.
- **Match the neighbors.** Copy the nearest sibling layout; do not invent one.
- **Stay grounded.** Anchor examples to Athar, DevMate, Qdrant, or the local hardware.
- **Do not fabricate measurements.** A claimed number must come from a run.
- Exercises self-verify; there is no repo-wide pytest for `projects/`, so `--verify` plus
  the five validators are the gate.

---

## 8. Progress log

- 2026-10-01 — `python/08-mlops` complete: 16 quizzes (`quizzes/NN-topic-quiz.md`).
- 2026-10-01 — `python/09-genai` complete: 25 quizzes (`quizzes/NN-topic-quiz.md`).
- 2026-10-02 — audit corrected (186 with quiz, 412 missing, 99 thin); plan re-keyed to both
  roadmaps and `docs/product/`.
- 2026-10-02 — `python/06-data-structures-algorithms` complete: 20 quizzes; the truncated
  `12-linear-search-lecture.md` expanded (1.8 KB → 12.5 KB); exercise runs, exit 0.
- 2026-10-02 — `00-core-foundations/data-engineering` complete to 15 units: added 08 (batch vs
  streaming, Lambda/Kappa), 09 (ETL vs ELT + CDC), 10 (lakehouse, Iceberg/Delta), 11 (data quality
  frameworks), 12 (feature stores), 13 (feature pipelines), 14 (data versioning + lineage), 15
  (storage + database selection). Each has lecture, glossary, quiz, and a `--verify` exercise;
  all eight exercises exit 0, ruff clean, five validators green.
- 2026-10-02 — `python/02-advanced-python` complete: 34 quizzes added (topics 01–34); topics
  35–38 already had `challenges/NN/quiz.md`. All 38 lectures now have a quiz.
- 2026-10-02 — `python/07-machine-learning` complete: 40 quizzes; the 9 thin advanced
  lectures (24–32) expanded to full detail. Module now 0 thin.

*Created 2026-10-01 as a 12-axis content strategy. Rewritten 2026-10-02 to cover the whole
roadmap. Update §2 and §8 when a block of units completes.*
