# Evaluation harness

`make eval` targets `eval/run_ragas.py`, which does not exist yet — building it is the Week 2–3 deliverable (Module 4 of `docs/curriculum/practice/04-evaluation-observability-practice.md`), not a bug.

Contents to be created by the learner:

- `run_ragas.py` — the harness entry point `make eval` calls
- golden set lives at `../../../../evaluations/rag/datasets/devmate-golden.jsonl`
- results/reports land under `../../../../evaluations/rag/reports/`

Rules: every run must work offline (mock or recorded LLM responses), print a metrics table, and cost < $0.50 per run when a real provider is used.
