# Fine-Tuning 04: Training Runs

## Topic Overview

A training run is a reproducible experiment: config, data, model, and metrics all
recorded so the run can be repeated and compared. Without that discipline a fine-tune is
a one-off whose result nobody can explain or improve, and the next attempt starts from
zero.

This lecture covers the run config that captures everything, why eval loss on a held-out
set is the honest signal while training loss is not, checkpointing for resilience to OOM
and interruption, comparing runs against a baseline on the same data split, and the
reproducibility rules that make the training loop an experiment loop rather than a
guessing game.

The comparison discipline is the part that most people skip. Two runs are only comparable
when the data version, the eval set, and the metric are identical; a "better" run on a
different split is not a better run, it is a different experiment.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write a complete, recorded run config.
2. Monitor eval loss during training and detect overfitting.
3. Checkpoint and resume a run.
4. Compare runs against a baseline on the same data split.
5. Reproduce a run from its config, seed, and data version.
6. Explain why the data version is part of the config.

## Prerequisites

- Fine-Tuning 03 (training data) for the data version and eval set.
- Fine-Tuning 02 (LoRA/QLoRA) for the hyperparameters the config holds.

---

## 1. The Run Config

### Everything that matters

The config captures the base model, the adapter rank, the learning rate, the batch size,
the epochs, the data split, and the seed:

```python
config = {
    "base_model": "qwen2.5-7b",
    "rank": 16,
    "lr": 2e-4,
    "batch_size": 4,
    "epochs": 3,
    "data_split": "v1",
    "seed": 42,
}
```

### Why records, not memory

A run without a recorded config is unreproducible. Six weeks later, "which learning rate
did we use?" has no answer, and the improvement cannot be repeated or built on. The config
is recorded with the run, in the run directory or the experiment tracker, and it travels
with the artifact.

### The data version is part of the config

The data version is a config field, not an external detail, because a different dataset is
a different run. Recording it makes the cross-run comparison valid.

## 2. Monitoring During Training

### Training loss and eval loss

Training loss falls as the model fits the data. Eval loss on the held-out set is the
honest signal. A fall in training loss with a rise in eval loss is overfitting:

```python
def is_overfit(train_loss: float, eval_loss: float) -> bool:
    return train_loss < 0.05 and eval_loss > train_loss * 3
```

```python
assert is_overfit(0.01, 0.5)  # memorized training, failed evaluation
assert not is_overfit(0.2, 0.25)  # healthy: eval tracks train
```

### What to watch

| Metric | Healthy | Overfit |
| --- | --- | --- |
| Training loss | Decreasing | Near zero |
| Evaluation loss | Decreasing | Rising |
| Eval quality | Improving | Degrading |

### Stopping

When eval loss starts rising, stop. Training longer only lowers training loss and worsens
generalization. Early stopping is the simplest control; a low rank is another.

## 3. Checkpointing

### Why checkpoints

A run interrupted by an OOM, a power cut, or a rental time limit should resume from the
last checkpoint, not restart from zero. Checkpoints save the adapter state periodically
along with the step and the config hash.

### What the checkpoint carries

The checkpoint carries the step and the config, so resuming with a different config is
detected as a different run. A checkpoint without its config is a weight file, not a
resumable run.

### Retention

Keep the best checkpoint by eval loss and the last checkpoint. Keeping every checkpoint
for a long run wastes storage; keeping none wastes the run if it is interrupted at the
end.

## 4. Comparing Runs

### Same split, same metric

Runs are compared on the same eval set and the same metric. The exercise enforces it:

```python
def better(candidate: dict, baseline: dict) -> bool:
    assert candidate["data_split"] == baseline["data_split"], (
        "runs compare only on the same data version"
    )
    return candidate["eval_loss"] < baseline["eval_loss"]
```

Comparing a candidate on `v2` against a baseline on `v1` is refused, because the
difference is partly the data, not the training.

### The delta is the evidence

The comparison is the evidence for the next decision: keep the adapter, change the rank,
change the data. Record baseline, candidate, metric, and delta so the decision is
reviewable with numbers rather than memory.

### The tradeoff

A candidate that improves eval loss but degrades a downstream metric (faithfulness, format
compliance) is a tradeoff to be made explicitly, not a win to be celebrated.

## 5. Reproducibility

### The three inputs

A recorded config plus a fixed seed plus the same data version reproduces the run.
The seed controls the sampling and any stochastic initialization, so a run without a
recorded seed is not reproducible even with the same config.

### Why it matters

Reproducibility is what makes the training loop an experiment loop: change one thing,
re-run, compare. Without it, every run is a fresh lottery and no lesson accumulates. This
is the same measured-experiment discipline used in RAG evaluation, applied to training.

### The artifact link

The reproducible run's output is the adapter, recorded in the model registry (Fine-Tuning
05) with its config, data version, and eval results, so the artifact and the run that
produced it stay connected.

## Real-World Application

- Recording the Athar SFT run's config (base, rank 16, lr 2e-4, data `v1`, seed 42) so the
  adapter can be reproduced.
- Watching eval loss and stopping when it rises, instead of training the full epoch count
  into overfitting.
- Comparing a rank-8 adapter against the rank-16 baseline on the same eval set.
- Resuming an interrupted QLoRA run from the last checkpoint.

## Common Mistakes

1. **A run without a recorded config.** Unreproducible and unexplainable.
2. **Watching only training loss.** Overfitting stays invisible until production.
3. **No checkpoints.** An OOM restarts the run from zero.
4. **Comparing runs on different eval sets or data versions.** The comparison is
   meaningless.
5. **Changing the data without a new version.** Silent, invalid comparisons.
6. **No recorded seed.** The run cannot be reproduced.

## Key Takeaways

1. The config captures everything and is recorded with the run; the data version is a
   config field.
2. Eval loss on the held-out set is the honest signal; rising eval loss with falling
   training loss is overfitting.
3. Checkpoints make runs resumable after OOM or interruption.
4. Runs compare only on the same eval set and data version; the delta is the evidence.
5. Config plus seed plus data version reproduces the run and connects it to the artifact.

## Self-Check Questions

1. Name four fields a run config must record and why each matters.
2. What does a rising eval loss with a falling training loss indicate, and what do you do?
3. Why is comparing a `v2` candidate against a `v1` baseline invalid?
4. What three inputs reproduce a run, and why is the seed one of them?
5. Why is the data version part of the config rather than external context?

## Further Reading / Connections

- Fine-Tuning 03 (training data) — the data version and eval set the run references.
- Fine-Tuning 05 (model registry) — where the run's artifact and results are recorded.
- Fine-Tuning 02 (LoRA/QLoRA) — the hyperparameters the config holds.
- `docs/reference/llm-production-architecture.md` — evaluation and experiment discipline.
