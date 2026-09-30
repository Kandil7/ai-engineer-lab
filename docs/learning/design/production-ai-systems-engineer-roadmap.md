# Production AI Systems Engineer Roadmap

### Context

Repo fullstack-ai-engineer-lab. User asked for a Production AI Systems Engineer roadmap plus an audit of current content and what is left. Used researcher (job market) and architect (repo audit) agents in parallel. Wrote docs/roadmap/production-ai-systems-engineer.md and updated tracking files.

### Explanation

Market research (2026) defines the role as platform substrate work: serving, LLMOps, observability, cost, reliability, gateway, evals infrastructure. The active 10-week DevMate track already covers the LLM application layer (client, tracing, cost ledger, RAG, agents, guardrails, deployment plans). The audit found curriculum-heavy, production-light content elsewhere: model-serving demos without servers, README-only DevOps folders, and empty eval/load/integration test directories in DevMate. The Production track is therefore sequenced as Phase 3 after A4/A6, not as a concurrent plan. Phases P1-P8: eval platform, SLOs, cost enforcement, reliability, self-hosted serving lab on RTX 5000, gateway, optional k8s, platform capstone.

### Alternatives

Option A: replace the active 10-week track with a production AI track immediately. Rejected: contradicts ADR-0004, splits focus, and repeats the curriculum-instead-of-shipping failure mode. Option B: write a generic career roadmap with no repo audit. Rejected: user asked what current content covers and what is left. Option C: treat this as a concurrent second track starting now. Rejected by both research synthesis and audit: gate on A4/A6 first.

### Rationale (Why this?)

Production AI Systems roles require evidence that the current repo mostly lacks (running eval gates, SLOs, cost enforcement, measured serving numbers). Building that evidence on DevMate preserves the cumulative-project strategy while targeting a deeper role family. Hardware constraint is honest: RTX 5000 sm_75 supports a measurement lab, not a hyperscale claim.

### Exercises

1) Run gap tables in production-ai-systems-engineer.md §3 against the repo every monthly review. 2) When A4 lands, open P1 and implement the eval gate first. 3) In the P5 lab, measure TTFT/TPOT on Ollama vs vLLM and record numbers. 4) Draft interview answers for the system-design prompts in §8 using DevMate architecture. 5) Track remote postings weekly for AI Platform / LLMOps titles and note location clauses.

### Next Steps

Finish active-track week 1 (LLM layer + Langfuse + golden cases). Keep P-track parked until A4. When ready for P1, implement eval harness and CI gate. Consider MLflow only if postings demand it.

### Follow-up (2026-09-30)

Advanced A2 without starting P-track. Shipped week-1 prompt golden cases:
`evaluations/prompts/golden-cases/devmate.jsonl` (10 cases) and offline schema
validation in `devmate/src/devmate/eval/validate_prompt_golden.py` plus
`tests/unit/test_prompt_golden.py`. Path resolution initially used the wrong
parent count (`parents[3]` resolved inside the DevMate project); corrected to
`parents[6]` (repo root). Ruff complexity/print issues fixed by splitting
validators and using `sys.stderr`/`sys.stdout`. Full DevMate gate verified:
ruff 0, format clean, mypy 0, pytest 42 passed. Remaining A2: Langfuse keys +
live traced `devmate ask`.

### Follow-up 2 (2026-09-30, eval harness)

Implemented offline eval harness foundation for A3/P1: metrics, dataset loaders,
`python -m devmate.eval.run_ragas`, recorded retrieval/answer fixtures, and unit
tests. Offline run verified: Hit@5 1.000, answer pass rate 1.000, report at
`evaluations/rag/reports/2026-09-30-eval-harness.md`. Full DevMate gate: ruff 0,
format clean, mypy 0, pytest 52 passed. Langfuse blocked on manual UI key creation
(compose documents the step). Docker server 29.7.2 is available; compose was not
started because docker-compose requires approval under workstation safety rules.
P-track remains gated on A4/A6.

---
