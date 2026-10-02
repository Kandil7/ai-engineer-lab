# Production AI Skills Matrix (12 axes)

> The single artifact the 12-axis production roadmap asks for first: for each axis,
> "can I prove it with a link/test, or not yet?" An axis is claimed only with
> evidence (a path, a passing test, a deployed URL). Study without a shipped artifact
> does not count.
>
> Status legend: **Provable** (evidence exists) · **Partial** (some evidence) ·
> **Not yet** (no shipped artifact).

**Last updated:** 2026-09-30

| # | Axis | Evidence in this repo | Status |
| --- | --- | --- | --- |
| 1 | Python to production | `projects/00-core-foundations/python/01-core-python/`, `02-advanced-python/`; DevMate as a packaged service (`projects/04-ai-engineering/devmate/pyproject.toml`, 14 subpackages, ruff/mypy/pytest gates) | **Provable** |
| 2 | CS, Git, Linux, SQL, software engineering | `projects/00-core-foundations/git-linux/`, `ds-algo/`; `projects/00-core-foundations/python/04-databases/`; `projects/03-databases/postgres-design/`; 6 ADRs in `../decisions/README.md` | **Partial** — no networking artifact; no Alembic migration run recorded |
| 3 | Math and ML foundations | `projects/00-core-foundations/python/07-machine-learning/` (fundamentals 1-23, advanced 24-35, deep-learning 36-40); `projects/04-ai-engineering/applied-ml/` (5 lectures + `05-baseline-intent-classifier/`: rule baseline, Naive Bayes, source-split with a leakage assert, error report, `--verify` green) | **Provable** |
| 4 | Backend for AI | `projects/04-ai-engineering/devmate/src/devmate/api/main.py` (FastAPI `/ask` SSE); `docs/learning/paths/fastapi-ai-services.md`; 25 FastAPI topics | **Partial** — no per-corpus authorization; no public URL |
| 5 | Data engineering | `projects/00-core-foundations/data-engineering/` (15 lectures: 01-15, each with lecture + glossary + quiz + `--verify` exercise); `projects/04-ai-engineering/athar-lab/` (contracts + deterministic CLI); `devmate/src/devmate/ingest/` | **Partial** — real Shamela ingestion and dataset/embedding/index versioning not built |
| 6 | LLMs and RAG | `projects/04-ai-engineering/{rag-system,arabic-nlp,embeddings,prompt-engineering}/`; `devmate/src/devmate/{llm,index,retrieve,cache,guards}/`; `docs/curriculum/lectures/` | **Partial** — A3 ADRs (chunking, Qdrant vs Chroma) lack measured numbers |
| 7 | Evaluation and experimentation | `projects/04-ai-engineering/ai-evaluation/` (7 lectures); `devmate/src/devmate/eval/run_ragas.py` (offline harness); `evaluations/` (golden cases, datasets, reports) | **Partial** — no live end-to-end run; no eval gate in CI yet |
| 8 | Inference engineering | `projects/04-ai-engineering/model-serving/` (4 lectures); `projects/00-core-foundations/python/08-mlops/07-model-serving.py`, `08-inference-optimization.py` | **Not yet** — no vLLM/TTFT benchmark or written serving decision |
| 9 | DevOps and MLOps | `.github/workflows/ci.yml`; `infra/docker/docker-compose.yml`; `projects/00-core-foundations/python/08-mlops/`; `projects/06-devops/{ci-cd,deployment,llmops}/README.md` | **Partial** — no CD, staging, versioned release, or rollback |
| 10 | Operations and SRE | `projects/04-ai-engineering/devmate/docs/failure-modes.md`; `devmate/src/devmate/obs/` (Langfuse + cost); `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience` | **Partial** — no runbooks, SLIs/SLOs, tested backup/restore, or Game Day |
| 11 | Security, privacy, governance | `projects/04-ai-engineering/security/` (10 lectures); `devmate/src/devmate/guards/guardrails.py`; `projects/04-ai-engineering/rag-system/08-context-security` | **Partial** — no Athar threat model; no red-team artifacts |
| 12 | System design, product, leadership | `projects/00-core-foundations/python/10-system-design/` (5 lectures incl. ADRs); `docs/decisions/README.md` (6 ADRs); `docs/reference/interview-bank.md` (27 questions); `docs/reference/llm-production-architecture.md` | **Partial** — no published project case study |

## The first empty box

Per the roadmap's own rule, work starts where the evidence is thinnest. Ranked by
how empty:

1. **Axis 10 — Operations/SRE.** Only the failure-modes doc exists. Missing:
   runbooks, SLIs/SLOs, tested backup/restore, incident/postmortem, Game Day.
2. **Axis 7 — Evaluation harness (live).** The offline harness exists; the live
   end-to-end run and the CI gate do not.
3. **Axis 11 — Threat model.** No threat-model artifact.
4. **Axis 8 — Inference benchmark.** Nothing measured.

*(Axis 3 closed: the non-LLM baseline classifier shipped under
`applied-ml/05-baseline-intent-classifier/`.)*

## How to use this

1. Pick the axis with the weakest evidence that the current milestone needs.
2. Ship one artifact (a test, a runbook, a report) that upgrades its status.
3. Update the row and this file; a status change is the evidence of progress.

---

*Created 2026-09-30. Mirrors the 12-axis map; distinct from
`skills-matrix.md`, which is on the 10-week active-track axis set.*
