# Fine-Tuning 03: Training Data Preparation

## Topic Overview

The instruction set decides what the model learns. A small, clean, deduplicated set of
high-quality examples beats a large, noisy one, and it beats it by a margin that surprises
people who assume more data is always better. In SFT the model imitates the data, so the
data's flaws become the model's flaws: a wrong answer teaches the model to be wrong, a
mixed format teaches a mixed format, and a duplicate teaches the model to over-weight one
pattern.

This lecture covers the instruction format and its consistency, quality filtering,
deduplication (exact and near), the train/eval split, and the discipline of auditing the
set before training. It is a data-engineering task, not a training task, and treating it
as such is most of the work.

The output of this lecture is a fixed, recorded data version that a training run can
reference, so the same set measures every run and a change to the data is a deliberate new
version rather than a silent drift.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Format instruction data consistently for the chat template.
2. Filter low-quality examples before they reach training.
3. Deduplicate exact and near-duplicate examples.
4. Split into a fixed train set and a held-out evaluation set.
5. Audit the set and produce an auditable data version.
6. Explain why data quality dominates data quantity in SFT.

## Prerequisites

- Fine-Tuning 01 (SFT) for what the training data teaches.
- Basic text handling and set operations in Python.

---

## 1. The Instruction Format

### The pair

Each example is an instruction-answer pair. The instruction is the user turn and the
answer is the assistant turn, formatted for the chat template:

```python
{"instruction": "ما حكم الصلاة في السفر؟", "answer": "القصر جائز للمسافر"}
```

### Consistency is the lesson

The format is identical across the whole set, because the model learns the format from
the data. A set where some answers carry citations and others do not teaches the model
that citations are optional. Consistency is enforced by a schema check on the whole set,
not by hoping the annotators were careful.

### The template travels

The same chat template used in training must be used at inference (Fine-Tuning 01). The
data preparation step is where the template is applied to every example, so a template
change is a data change and a new data version.

## 2. Quality Over Quantity

### The principle

A few hundred clean examples beat thousands of noisy ones. The model imitates what it
sees, so noise is imitated as faithfully as signal.

| Example count | Quality | Result |
| --- | --- | --- |
| 50 | Perfect | Minimal but clean |
| 200 | Good | Good for most tasks |
| 1000 | Clean | Excellent |
| 1000 | Noisy | Worse than 200 clean |

### What filtering removes

- Wrong or unverifiable answers.
- Truncated or malformed text.
- Examples that do not match the task.
- Examples whose format breaks the schema.

### Quality is a data-engineering task

Filtering is not a training concern. The training code does not know an answer is wrong;
only the data pipeline does. Build the filter into the pipeline so every run inherits the
same quality bar.

## 3. Deduplication

### Exact duplicates

Exact duplicates waste capacity and bias the model toward the repeated pattern. They are
cheap to remove by normalizing the instruction and keeping the first occurrence:

```python
def dedupe(examples: list[dict]) -> list[dict]:
    """Remove exact duplicates by normalized instruction."""
    seen: set[str] = set()
    out = []
    for ex in examples:
        key = ex["instruction"].strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(ex)
    return out
```

### Near-duplicates

Near-duplicates (the same question phrased slightly differently, or the same answer with
trivial edits) are harder. They need normalization plus a similarity comparison. Removing
them matters because a cluster of near-duplicates is a single pattern that the model
over-learns.

### Why it improves generalization

A deduplicated set spreads the same number of training steps across more distinct
patterns, so the model learns the task instead of memorizing a repeated example. This is a
generalization improvement, not a housekeeping chore.

## 4. The Train/Eval Split

### Held-out and fixed

A held-out evaluation set is excluded before training and kept out of every training run.
The split is recorded so the same eval set measures every run, which is what makes run
comparison meaningful (Fine-Tuning 04).

```python
def split(examples, eval_frac):
    """Split by example (not by topic) into train and eval."""
    n_eval = max(1, round(len(examples) * eval_frac))
    return examples[n_eval:], examples[:n_eval]
```

### Split by example, not by topic

The eval set must represent the same distribution as training. Splitting by topic (all
fiqh questions in eval, all verse questions in train) measures cross-topic generalization,
which may be interesting but is not what you usually want to gate on. Split by example so
the eval set looks like the training set.

### No leakage

No eval example appears in training. The exercise asserts this explicitly:
`assert not any(e in train for e in eval_set)`. Leakage here is the same failure as
everywhere else: the metric inflates and production disappoints.

### Group split when examples cluster

If examples share a source (a book, a document), split by the source so a source is
entirely in train or entirely in eval. This is the by-group rule from Applied ML 02
applied to instruction data.

## 5. Auditing Before Training

### The audit

Before the run, audit the set: format consistency, answer length distribution, task
coverage, label balance, and the eval set's representativeness. The audit is a report, not
a glance.

### Why before, not during

A problem found during training wastes the GPU hours already spent. A problem found in the
audit costs nothing. Fix the data before the run, and re-audit after any change.

### The data version

The audit produces a data version: a fixed, recorded snapshot of the cleaned, split set.
Training runs reference the data version, so a change to the data is a new version and the
comparison across runs stays valid (Fine-Tuning 04).

## Real-World Application

- Cleaning an Athar instruction set of fiqh question-answer pairs, removing exact and
  near-duplicates, and holding out a representative eval slice.
- Enforcing a schema that requires a citation field in every answer so the model learns
  citations are mandatory.
- Auditing answer-length distribution to catch a subset of answers that are truncated.
- Recording the data version so a faithfulness regression can be attributed to the data
  or the training.

## Common Mistakes

1. **Training on a noisy set.** The model learns the noise.
2. **No deduplication.** Repeated patterns dominate and the model over-weights them.
3. **Eval set leaking into training.** The metric inflates.
4. **Splitting by topic instead of by example.** The eval set does not represent the
   training distribution.
5. **No audit before the run.** Problems surface during training, wasting GPU hours.
6. **Changing the data without a new version.** Run comparisons silently break.

## Key Takeaways

1. A consistent format is the lesson the model learns from the data.
2. A few hundred clean examples beat thousands of noisy ones; filtering is a pipeline
   concern.
3. Deduplication (exact and near) improves generalization, not just tidiness.
4. The eval split is fixed, held out, by example, and split by group when sources cluster.
5. Audit before training and record a data version so runs stay comparable.

## Self-Check Questions

1. Why does a mixed-format dataset teach the model a mixed behavior?
2. Why is deduplication a generalization improvement and not just housekeeping?
3. Why split by example rather than by topic, and when would you split by group instead?
4. What does the audit check, and why does it run before training?
5. Why is the data version part of a reproducible run?

## Further Reading / Connections

- Fine-Tuning 01 (SFT) — what the data teaches and why format consistency matters.
- Fine-Tuning 04 (training runs) — how the data version makes runs comparable.
- Fine-Tuning 05 (model registry) — where the data version is recorded with the artifact.
- Applied ML 02 (train/validation/test and leakage) — the by-group split rule.
