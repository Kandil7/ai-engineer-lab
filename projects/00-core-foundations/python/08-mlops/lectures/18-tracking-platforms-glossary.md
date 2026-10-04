# Tracking Platforms — Glossary 18

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Run record | Contract | id, config, metrics, artifacts, provenance for one run |
| MLflow | Platform | Open-source, self-hosted, full-lifecycle tracking |
| W&B | Platform | Managed platform for collaboration and sweeps |
| Comet | Platform | Managed platform for training and production monitoring |
| Neptune | Platform | Managed metadata store for many long-running runs |
| Sacred | Library | Lightweight config/seed capture with no server |
| Sweep | Tracking | A managed hyperparameter search over runs |
| Artifact | Run | A file a run produces (checkpoint, plot, dataset ref) |
| Provenance | Run | git sha, data version, and seed identifying a run |
| Data residency | Policy | Where run data is legally allowed to live |
| Tracker adapter | Engineering | One logging interface swappable across backends |
| Lock-in | Risk | A switching cost created by hard-coded vendor calls |

## Detailed Definitions
### Run record
**Definition**: The five-field unit every tracker stores: run id, config,
time-series metrics, artifacts, and provenance. The contract you own; the
platform implements it.
```python
{
    "run_id": "...",
    "config": {...},
    "metrics": {...},
    "artifacts": [...],
    "provenance": {"git_sha": "...", "data_version": "...", "seed": 0},
}
```
**Related**: Provenance, Tracker adapter

### MLflow
**Definition**: The open-source tracking platform: Tracking, Projects, Models,
and a Registry; self-hosted (file store, server, database) or managed via
Databricks. Framework-agnostic and the full-lifecycle default.
```python
mlflow.log_params({...})
mlflow.log_metric("val_acc", 0.91, step=10)
```
**Related**: W&B, Run record

### W&B (Weights & Biases)
**Definition**: A managed platform centered on collaboration: rich dashboards,
shareable reports, sweeps, and versioned artifacts. The research-lab favorite.
**Related**: Comet, Sweep

### Comet
**Definition**: A managed platform emphasizing experiment comparison and
production model monitoring, covering training and serving in one tool.
**Related**: W&B, Neptune

### Neptune
**Definition**: A managed metadata store built for many concurrent, long-running
runs and high-frequency metric logging; offers a self-hosted option.
**Related**: Sacred, W&B

### Sacred
**Definition**: A minimal open-source library that captures run configuration,
seeds, and results with almost no ceremony; no server, no dashboards.
**Related**: Run record

### Sweep
**Definition**: A platform-managed hyperparameter search that launches, tracks,
and compares many runs automatically.
**Related**: W&B, Run record

### Artifact
**Definition**: A file a run produces. Keep large blobs in object storage and log
the reference; do not push gigabytes through the tracking API.
**Related**: Run record

### Provenance
**Definition**: The evidence that identifies a run: git sha, data version, and
seed. Without it, a metric cannot be reproduced or audited.
**Related**: Run record

### Data residency
**Definition**: The legal constraint on where run data may live; decides managed
SaaS versus self-hosted before any feature comparison.
**Related**: MLflow, Neptune

### Tracker adapter
**Definition**: One `log_run()` interface over the five-field contract so the
backend (MLflow, W&B, a dict) is swappable without touching training code.
**Related**: Run record, Lock-in

## Key Concepts Summary
### The contract
- id, config, metrics, artifacts, provenance — every tracker, every run.

### The selection order
- Hosting (data residency) → scope → collaboration → cost.

### The reversibility rule
- Own the contract and the export; the platform is replaceable.

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Run record — ___
2. W&B — ___
3. Sacred — ___
4. Sweep — ___
5. Data residency — ___

**Answers:** 1-b, 2-d, 3-e, 4-c, 5-a where a=where data may legally live,
b=id/config/metrics/artifacts/provenance, c=managed hyperparameter search,
d=managed collaboration platform, e=library for config capture.
