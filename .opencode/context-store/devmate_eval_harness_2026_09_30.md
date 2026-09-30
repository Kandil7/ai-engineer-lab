---
id: devmate_eval_harness_2026_09_30
reported_by: builder
created_at: 2026-09-30T15:29:55.751Z
---

# Eval harness foundation shipped (2026-09-30, session 2)

## What landed
- src/devmate/eval/metrics.py — Hit@1/5/10, MRR, answer-property checks (offline-safe)
- src/devmate/eval/datasets.py — loaders for RAG + prompt golden JSONL, report writer
- src/devmate/eval/run_ragas.py — offline/live CLI entry (`python -m devmate.eval.run_ragas`)
- evaluations/rag/baselines/devmate-offline-recordings.jsonl — 10 recorded top-k lists
- evaluations/prompts/golden-cases/devmate-offline-answers.jsonl — 10 recorded answers
- evaluations/rag/reports/2026-09-30-eval-harness.md — first harness report
- tests/unit/test_eval_harness.py — 10 offline tests
- eval/README.md updated

## Offline harness run (verified)
Retrieval cases 10
Hit@1 0.600 (6/10)
Hit@5 1.000 (10/10)
Hit@10 1.000 (10/10)
MRR 0.742
Answer cases 10
Answer pass rate 1.000 (10/10)
Report: evaluations/rag/reports/2026-09-30-eval-harness.md

## DevMate gate
ruff check clean; ruff format clean; mypy src/ clean (36 files); pytest 52 passed.

## Blockers / not done
- Langfuse: compose documents manual UI key creation (langfuse 2.x has no env key seeding). .env keys still required for live traced ask.
- Live retrieval eval needs docker compose (qdrant + postgres + redis) + ingest. Docker server 29.7.2 available; compose not started (requires approval).
- Live LLM answer scoring not wired; do not claim it.
- P-track still gated on A4/A6.

## How to run
cd projects/04-ai-engineering/devmate
.venv\Scripts\python.exe -m devmate.eval.run_ragas --mode offline
.venv\Scripts\python.exe -m pytest tests/unit/test_eval_harness.py -q

