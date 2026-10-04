# MLOps — 18: Tracking Platforms

## Topic Overview

An experiment tracker is the system of record for training runs: every
hyperparameter, metric, artifact, and environment fingerprint, stored so runs can
be compared, reproduced, and audited. Lecture 02 taught the *run data model* and
MLflow, the open-source default. This lecture is about the *platform choice*: the
managed services (Weights & Biases, Comet, Neptune) and the lightweight library
(Sacred), and how to pick one without locking yourself into a decision you cannot
reverse.

The platforms differ along four axes: **hosting** (self-hosted versus managed
SaaS), **scope** (tracking only versus the full lifecycle), **collaboration**
(reports, sharing, teams), and **cost model** (free tier, per-seat, per-GB). The
choice is rarely about features alone; it is about who runs the server, who sees
the data, and what the bill looks like at scale.

The durable lesson is that the *run-record contract* is the same everywhere: a
run has an id, a config, metrics over time, artifacts, and provenance. If you
keep that contract explicit in your code, switching trackers is a thin adapter,
not a rewrite. The platforms are interchangeable at the boundary; the contract is
what you own.

## Learning Objectives

By the end of this lecture, you will be able to:
1. State the run-record contract every tracker must satisfy
2. Describe MLflow's open-source, self-hosted full-lifecycle model
3. Compare W&B, Comet, and Neptune as managed platforms
4. Explain where Sacred fits as a lightweight library
5. Choose a platform by hosting, scope, collaboration, and cost
6. Design tracker-agnostic logging so switching is an adapter, not a rewrite
7. Avoid the lock-in and data-egress traps of managed platforms

## Prerequisites

| Need | Where |
|---|---|
| The experiment data model | `08-mlops/lectures/02-experiment-tracking-lecture.md` |
| Model registry | `08-mlops/lectures/04-model-registry-lecture.md` |
| Reproducibility | `08-mlops/lectures/01-reproducibility-lecture.md` |

## 1. The Run-Record Contract

Whatever the platform, a run record has the same five parts. This is the
interface you program against; the platform is the implementation.

```python
# The contract: five fields, every tracker, every run.
run_record = {
    "run_id": "2026-10-02T09:14_a1b2",
    "config": {"lr": 3e-4, "batch": 64, "model": "resnet18"},
    "metrics": {"train_loss": [...], "val_acc": [...]},   # series over time
    "artifacts": ["checkpoints/best.pt", "confusion.png"],
    "provenance": {"git_sha": "a1b2c3", "data_version": "sha256:9f...", "seed": 0},
}
```

A tracker that captures these five is sufficient. Everything else — dashboards,
sweeps, sharing — is convenience built on top. Keeping the contract explicit in
your code is what makes the platform swappable.

## 2. MLflow: Open Source, Full Lifecycle

MLflow is the open-source reference implementation. It has four components:
**Tracking** (runs and metrics), **Projects** (packaged runs), **Models** (a
standard model format), and the **Model Registry** (Lecture 04). It is
self-hosted (a local `mlruns/` directory, a server, or a managed Databricks
offering) and framework-agnostic.

```python
import mlflow

with mlflow.start_run(run_name="resnet18-baseline"):
    mlflow.log_params({"lr": 3e-4, "batch": 64})
    mlflow.log_metric("val_acc", 0.91, step=10)
    mlflow.log_artifact("confusion.png")
```

**Choose MLflow when** you want to own the data, need the full lifecycle in one
open-source stack, or must self-host for privacy or cost. **The cost** is
operational: you run the server, the artifact store, and the database.

## 3. Weights & Biases: Managed Collaboration

W&B is a managed platform built around collaboration: rich run dashboards,
shareable reports, **sweeps** (managed hyperparameter search), and **artifacts**
(versioned datasets and models). It is the research-lab favorite because the
collaboration surface — a link a colleague can open — is first-class.

```python
import wandb

run = wandb.init(project="devmate", config={"lr": 3e-4, "batch": 64})
run.log({"val_acc": 0.91}, step=10)
run.log_artifact("checkpoints/best.pt")
```

**Choose W&B when** team collaboration, sharing, and managed sweeps matter more
than self-hosting. **The trade** is data residency: your metrics and artifacts
live in their cloud unless you pay for a self-hosted deployment.

## 4. Comet: Managed Comparison

Comet is a managed platform with a strong emphasis on **experiment comparison**
and **model production monitoring** — it tracks not just training runs but the
deployed model's behavior. It integrates with most frameworks and has a
lightweight free tier.

```python
from comet_ml import Experiment

exp = Experiment(project_name="devmate")
exp.log_parameter("lr", 3e-4)
exp.log_metric("val_acc", 0.91, step=10)
```

**Choose Comet when** you want training and production monitoring in one managed
tool and value comparison views. The trade is the same as W&B: managed hosting.

## 5. Neptune: Long-Running Runs

Neptune is a managed metadata store designed for **many, long-running runs** and
large-scale metadata — it handles thousands of concurrent experiments and
high-frequency metric logging without dropping points. It offers a self-hosted
option, which matters for teams with data-residency constraints.

```python
import neptune

run = neptune.init_run(project="team/devmate")
run["config/lr"] = 3e-4
run["metrics/val_acc"].append(0.91)
```

**Choose Neptune when** you run many long experiments, need high-frequency
logging, or need a self-hosted managed option. The trade is the managed model
unless you self-host.

## 6. Sacred: The Lightweight Library

Sacred is not a platform; it is a small open-source Python library for capturing
**configuration, seeds, and results** with minimal ceremony, optionally backed by
MongoDB. It does one thing — capture the run config and metrics — and does it
without a server.

```python
from sacred import Experiment

ex = Experiment("devmate")

@ex.config
def cfg():
    lr = 3e-4
    batch = 64

@ex.automain
def train(lr, batch):
    return {"val_acc": 0.91}
```

**Choose Sacred when** you want config/seed capture in a script with no
infrastructure, or you are embedding tracking into existing research code. **The
trade** is scope: no dashboards, no collaboration, no registry.

## 7. The Comparison Matrix and Selection

| Platform | Hosting | Scope | Collaboration | Best for |
|---|---|---|---|---|
| MLflow | self-hosted / managed | full lifecycle | basic | owning the stack |
| W&B | managed | tracking + sweeps | excellent | research teams |
| Comet | managed | training + prod monitor | strong | train + serve in one tool |
| Neptune | managed / self-hosted | large-scale metadata | strong | many long runs |
| Sacred | library | config capture | none | zero-infra scripts |

The selection questions, in order:

1. **Can the data leave your infrastructure?** If no, self-hosted MLflow or
   Neptune, or a self-hosted W&B deployment.
2. **Do you need collaboration and sweeps?** Managed W&B or Comet.
3. **Do you run many long jobs?** Neptune.
4. **Do you want zero infrastructure?** Sacred (or MLflow's local file store).

```python
def choose_tracker(can_leave_infra, needs_collab, many_long_runs):
    if not can_leave_infra:
        return "mlflow (self-hosted)" if not many_long_runs else "neptune (self-hosted)"
    if needs_collab:
        return "wandb"
    if many_long_runs:
        return "neptune"
    return "mlflow (local) or sacred"
```

## Every Use Case

- **Research lab**: W&B for shared dashboards and sweeps across a team.
- **Privacy-constrained enterprise**: self-hosted MLflow or Neptune.
- **Train-and-serve team**: Comet for training plus production monitoring.
- **Solo researcher**: Sacred or a local MLflow file store, no server.
- **Large-scale training**: Neptune for thousands of concurrent long runs.
- **Regulated industry**: self-hosted MLflow so the run record never leaves.
- **Startup**: managed W&B free tier until scale forces a self-hosted decision.

## Real-World Use Cases for AI Engineers

- **ML platform engineer**: ships a tracker-agnostic `log_run()` wrapper so teams
  can use W&B or MLflow without changing training code — the contract is owned by
  the platform, the backend is a config flag.
- **Privacy-bound engineer**: a bank cannot send metrics to a SaaS; self-hosted
  MLflow keeps the run record inside the perimeter while preserving the full
  lifecycle.
- **Research engineer**: W&B sweeps replace a hand-rolled hyperparameter loop,
  and the shared run links make the weekly review a URL instead of a spreadsheet.
- **Startup engineer**: starts on W&B's free tier, then migrates to self-hosted
  MLflow when the bill and the data-residency requirement both arrive — the
  adapter makes it a one-line change.
- **LLM fine-tuning (Baligh)**: Neptune for many long adapter-training runs with
  high-frequency loss logging.

## Common Mistakes to Avoid

### Mistake 1: Hard-coding one tracker into the training loop
Every `wandb.log` scattered through the code makes a switch a rewrite. Wrap it in
one `log_run()` and program against the contract.

### Mistake 2: Choosing managed SaaS before checking data residency
Metrics and artifacts can contain sensitive data. Confirm the data may leave the
infrastructure before picking a cloud tracker.

### Mistake 3: Ignoring the cost model at scale
Per-seat and per-GB pricing is cheap for 3 people and expensive for 300 runs a
day. Model the bill before committing.

### Mistake 4: Assuming a tracker is a registry
Tracking stores runs; a registry stores *promoted* models with lifecycle stages
(Lecture 04). They are different concerns.

### Mistake 5: No artifact store plan
Logging a 10 GB checkpoint to a SaaS tracker on every run is a surprise bill.
Keep large artifacts in object storage and log the reference.

### Mistake 6: Abandoning the run record when the platform changes
The five-field contract is yours. Export it, keep it, and the platform is
replaceable.

## Best Practices

1. Program against the five-field run-record contract, not a vendor SDK
2. Wrap logging in one adapter (`log_run`) so the backend is swappable
3. Decide hosting by data residency first, features second
4. Keep large artifacts in object storage; log references, not blobs
5. Use the tracker's registry or MLflow's for promotion, not the tracking store
6. Model the cost at your expected run volume before committing
7. Export run records periodically so you own the history
8. Standardize run naming so comparisons are meaningful
9. Log provenance (git sha, data version, seed) on every run
10. Re-evaluate the platform at each order-of-magnitude scale change

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Log a metric point | ms | negligible | batch high-frequency points |
| Log a large artifact | seconds-minutes | O(artifact) | log a reference to object storage |
| Self-hosted MLflow | setup + ops | server + DB + store | local file store for solo work |
| Managed SaaS | zero setup | O(data) | free tier until scale |
| Migrate trackers | hours-days | — | a thin adapter + export |

## AI Engineering Relevance

**Where this shows up:** every training run you will ever do. The tracker is how
runs become comparable and reproducible; the platform choice is how you trade
operational burden for managed convenience.

| Concept here | Used for |
|---|---|
| Run-record contract | Swappable, owned experiment history |
| MLflow | Self-hosted full lifecycle |
| W&B / Comet / Neptune | Managed collaboration and scale |
| Sacred | Zero-infra config capture |
| Selection questions | Hosting, scope, collaboration, cost |

**Scale note:** the tracker decision is reversible only if the contract is
explicit. At 10 runs a week a managed free tier is fine; at 10,000 a day the
cost model and data residency dominate, and self-hosted MLflow or Neptune wins.
Design for the switch from day one.

## Practice Exercises

### Exercise 1: The Run Record (Easy)
Define a `RunRecord` dataclass with id, config, metrics, artifacts, and
provenance; write `to_dict`/`from_dict` and round-trip it.

### Exercise 2: Tracker Adapter (Medium)
Define a `Tracker` protocol with `start`, `log_metric`, `log_artifact`, and
`end`; implement a `MemoryTracker` and a `NullTracker`, and log a run through
each without changing the caller.

### Exercise 3: Selection Function (Medium)
Implement `choose_tracker(can_leave_infra, needs_collab, many_long_runs)` and
test each branch.

### Exercise 4: Cost Model (Hard)
Implement `monthly_cost(runs_per_day, points_per_run, artifact_gb_per_run,
price_per_seat, seats, price_per_gb)` and compare a managed plan against a
self-hosted estimate; find the break-even run volume.

## Summary

| Concept | Description |
|---|---|
| Run-record contract | id, config, metrics, artifacts, provenance |
| MLflow | Open-source, self-hosted, full lifecycle |
| W&B | Managed, collaboration, sweeps |
| Comet | Managed, training + production monitoring |
| Neptune | Managed/self-hosted, many long runs |
| Sacred | Lightweight library, zero infrastructure |

The tracker is the system of record for experiments; the platform is an
implementation detail behind a contract you own. Choose by hosting, scope,
collaboration, and cost — and keep the adapter thin so the choice stays
reversible.

## Quick Reference

| Task | Idiom |
|---|---|
| Start a run | `start_run()` / `wandb.init()` / `Experiment()` |
| Log a metric | `log_metric(name, value, step)` |
| Log an artifact | keep the blob in object storage, log the reference |
| Self-host | MLflow server + DB + object store |
| Switch trackers | a `log_run` adapter over the contract |

## Next Steps

Next: **[19 Resource and Performance Metrics](19-resource-and-performance-metrics-lecture.md)** —
measuring what the model costs to run.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://mlflow.org/, https://wandb.ai/, https://www.comet.com/
