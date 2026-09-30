# Evaluation harness

`make eval` targets `eval/run_ragas.py`. The harness is implemented as the
package module `devmate.eval.run_ragas` (this folder documents the entry point).

## Run offline (default, no API key, no Qdrant)

```powershell
cd projects/04-ai-engineering/devmate
.venv\Scripts\python.exe -m devmate.eval.run_ragas --mode offline
.venv\Scripts\python.exe -m pytest tests/unit/test_eval_harness.py -q
```

Offline mode:

- Loads RAG golden set `evaluations/rag/datasets/devmate-golden.jsonl`
- Loads prompt golden set `evaluations/prompts/golden-cases/devmate.jsonl`
- Scores retrieval from recorded top-k (`evaluations/rag/baselines/devmate-offline-recordings.jsonl`)
- Scores answer properties from recorded answers (`evaluations/prompts/golden-cases/devmate-offline-answers.jsonl`)
- Writes a metrics report under `evaluations/rag/reports/`

## Run live retrieval (needs Qdrant + embeddings)

```powershell
# infra first (requires Docker):
# docker compose -f infra/docker/docker-compose.yml up -d postgres redis qdrant
# then ingest the repo, then:
.venv\Scripts\python.exe -m devmate.eval.run_ragas --mode live --top-k 10
```

Live mode scores retrieval only unless `--with-llm` is set. LLM answer scoring is
not wired in this harness commit and must not be claimed as measured.

## Threshold gate (for CI later, P1)

```powershell
.venv\Scripts\python.exe -m devmate.eval.run_ragas --mode offline --fail-under-hit-at-5 0.9
```

Exit code 1 when Hit@5 is below the threshold. Week 2–3 / P1 will wire this into
GitHub Actions for prompt and retrieve changes.

## Rules

- Every offline run must work with no network and no API key.
- Cost < $0.50 per run when a real provider is used.
- Fixture mode notes explicitly say retrieval/answers are not live measurements.
- Live numbers go in dated reports under `evaluations/rag/reports/`.

## Related paths

| Item | Path |
| --- | --- |
| Harness source | `src/devmate/eval/run_ragas.py` |
| Metrics | `src/devmate/eval/metrics.py` |
| Dataset loaders | `src/devmate/eval/datasets.py` |
| Prompt schema validator | `src/devmate/eval/validate_prompt_golden.py` |
| Golden sets | `evaluations/rag/datasets/`, `evaluations/prompts/golden-cases/` |
| Reports | `evaluations/rag/reports/` |
