# Fine-Tuning 04: Training Runs — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Run config | Everything the run needs, recorded | base, rank, lr, seed |
| Eval loss | The honest signal on the held-out set | rising = overfit |
| Checkpoint | Saved adapter state for resume | step + config hash |
| Baseline | The reference run to compare against | eval loss 0.5 |
| Data version | The dataset identity in the config | split v1 |
| Reproducibility | Config + seed + data version reruns the run | same result |

---

## Alphabetical Glossary

### Baseline

**Definition:** The reference run that candidates are compared against, on
the same eval set. The comparison is the evidence for the next decision.

**Example:**
```python
# baseline eval loss 0.5; candidate 0.4 -> keep the candidate
```

**Related concepts:** Eval loss

---

### Checkpoint

**Definition:** Saved adapter state at a step, carrying the step and the
config hash. A run resumes from the last checkpoint, not from zero.

**Example:**
```python
# resume from step 1200 after an OOM
```

**Related concepts:** Run config

---

### Data version

**Definition:** The dataset identity recorded in the config. A changed
dataset is a changed run.

**Example:**
```python
# data_split "v1" vs "v2" are different runs
```

**Related concepts:** Run config, Reproducibility

---

### Eval loss

**Definition:** The loss on the held-out set, the honest signal. Rising
eval loss while training loss falls is overfitting.

**Example:**
```python
# train 0.01, eval 0.5 -> overfitting
```

**Related concepts:** Baseline

---

### Reproducibility

**Definition:** Config plus fixed seed plus the same data version reproduces
the run. What makes the loop an experiment loop.

**Example:**
```python
# same config, same seed, same data -> same result
```

**Related concepts:** Run config, Data version

---

### Run config

**Definition:** Everything the run needs, recorded with it: base model,
rank, learning rate, batch size, epochs, data split, seed. A run without
its config is unreproducible.

**Example:**
```python
{"base_model": "qwen2.5-7b", "rank": 16, "lr": 2e-4, "seed": 42}
```

**Related concepts:** Reproducibility, Data version

---

## Related Concepts

- **LoRA/QLoRA**: the rank and base model in the config (topic 02)
- **Training data**: the data version in the config (topic 03)
- **Model registry**: the run's output is registered (topic 05)

## Key Takeaways

1. The config captures everything and is recorded with the run.
2. Eval loss on the held-out set is the honest signal.
3. Checkpoints make runs resumable.
4. Runs compare on the same eval set.
5. Config + seed + data version reproduces the run.