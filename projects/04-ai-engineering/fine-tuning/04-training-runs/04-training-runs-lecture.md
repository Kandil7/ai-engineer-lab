# Fine-Tuning 04: Training Runs

## 🎯 Topic Overview

A training run is a reproducible experiment: config, data, model, and
metrics all recorded. This lecture covers the run config, monitoring
during training, checkpointing, and the discipline of comparing runs
against each other.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write a complete, recorded run config
2. Monitor loss and eval metrics during training
3. Checkpoint and resume a run
4. Compare runs against a baseline
5. Reproduce a run from its recorded config

---

## 1. The Run Config

The config captures everything: base model, adapter rank, learning rate,
batch size, epochs, the data split, and the seed. The config is recorded
with the run — a run without its config is unreproducible. The roadmap's
exit test: "the training run is reproducible from its config."

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

## 2. Monitoring During Training

Training loss falls; eval loss on the held-out set is the honest signal.
A rising eval loss while training loss falls is overfitting — stop or
reduce epochs. The eval set is the same across runs, so the eval loss is
comparable. The roadmap's exit test: "the model is evaluated during
training."

## 3. Checkpointing

Checkpoints save the adapter state periodically. A run interrupted by an
OOM or a power cut resumes from the last checkpoint, not from zero. The
checkpoint carries the step and the config hash — resuming with a
different config is a different run.

## 4. Comparing Runs

Runs are compared on the same eval set: baseline vs candidate, metric by
metric. A candidate that improves eval loss but degrades a downstream
metric is a tradeoff, made explicit. The comparison is the evidence for
the next decision — keep the adapter, change the rank, change the data.

## 5. Reproducibility

A recorded config plus a fixed seed plus the same data version reproduces
the run. The data version is part of the config — a changed dataset is a
changed run. Reproducibility is what makes the training loop an
experiment loop instead of a guessing game.

## Common Mistakes

- A run without a recorded config.
- Watching only training loss (overfitting invisible).
- No checkpoints (an OOM restarts from zero).
- Comparing runs on different eval sets.
- Changing the data without changing the version.

## Key Takeaways

1. The config captures everything and is recorded with the run.
2. Eval loss on the held-out set is the honest signal.
3. Checkpoints make runs resumable.
4. Runs compare on the same eval set.
5. Config + seed + data version reproduces the run.