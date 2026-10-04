# Phase 8 — MLOps: Production Machine Learning

The bridge from trained models to production systems: reproducibility,
tracking, versioning, serving, monitoring, and the full deployment lifecycle.

## Exercises (21)

| # | File | Topics |
|---|------|--------|
| 1 | 01-reproducibility.py | Seeds, env fingerprints, content hashing, run records |
| 2 | 02-experiment-tracking.py | Params/metrics/artifacts, leaderboards, run lifecycle |
| 3 | 03-data-versioning.py | Content addressing, provenance, diffs, safe retraining |
| 4 | 04-model-registry.py | Versions, lifecycle stages, gated promotion, rollback |
| 5 | 05-model-packaging.py | Joblib/ONNX/pyfunc, signatures, dependency capture |
| 6 | 06-docker-for-ml.py | Dockerfiles, layers, multi-stage, GPU images, 12-factor |
| 7 | 07-model-serving.py | FastAPI endpoints, validation, latency, health checks |
| 8 | 08-inference-optimization.py | Quantization, ONNX opt, batching, pruning, golden tests |
| 9 | 09-pipeline-orchestration.py | DAGs, Prefect/Airflow, idempotency, retries, caching |
| 10 | 10-data-validation.py | Pandera schemas, statistical checks, train/serve skew |
| 11 | 11-monitoring-and-drift.py | PSI, prediction drift, delayed labels, alert policies |
| 12 | 12-ci-cd-for-ml.py | Eval gates, DVC in CI, staged promotion |
| 13 | 13-feature-stores.py | Entities, feature views, point-in-time joins, online/offline |
| 14 | 14-ab-testing-models.py | Sample size, chi-squared, t-test, guardrails |
| 15 | 15-cost-optimization.py | Unit costs, spot instances, dedup, budgets |
| 16 | 16-case-study-e2e.py | Full lifecycle: data → train → registry → serve → monitor → promote |
| 17 | 17-model-governance.py | Fairness, bias detection, explainability, model cards |
| 18 | 18-tracking-platforms.py | MLflow, W&B, Comet, Neptune, Sacred, selection |
| 19 | 19-resource-and-performance-metrics.py | Latency, throughput, utilization, efficiency, gates |
| 20 | 20-continuous-training.py | Triggers, champion/challenger, thrash guards |
| 21 | 21-deployment-strategies.py | Shadow, canary, blue-green, A/B, rollback |

## Lectures

Every topic has a **full-detail lecture** (`lectures/NN-topic-lecture.md`) and
a **glossary** (`lectures/NN-topic-glossary.md`). Each lecture covers the
complete topic, every use case, and real-world scenarios for AI engineers in
production.

## Prerequisites

- Phase 7 Machine Learning (`07-machine-learning/`)
- Python + NumPy + pandas + scikit-learn

## Running

```bash
python 01-reproducibility.py            # run one exercise
python run_smoke_tests.py --phase 8     # run the whole phase
pytest tests/unit/test_mlops.py -q      # unit tests
```

## Production Path

The capstone (`16-case-study-e2e.py` + lecture) walks one model release
through all 15 practices — the template for any production ML system.
