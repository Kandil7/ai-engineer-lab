# Fine-Tuning 03: Training Data Preparation

## 🎯 Topic Overview

The instruction set decides what the model learns. A small, clean,
deduplicated set of high-quality examples beats a large, noisy one. This
lecture covers the instruction format, quality filtering, deduplication,
and the train/eval split.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Format instruction data for the chat template
2. Filter low-quality examples
3. Deduplicate near-duplicate examples
4. Split into train and held-out evaluation sets
5. Audit the set before training

---

## 1. The Instruction Format

Each example is an instruction-answer pair, formatted for the chat
template. The instruction is the user turn; the answer is the assistant
turn. The format is consistent across the whole set — the model learns the
format from the data. A mixed format teaches a mixed behavior.

```python
{"instruction": "ما حكم الصلاة في السفر؟", "answer": "القصر جائز للمسافر"}
```

## 2. Quality Over Quantity

A few hundred clean examples beat thousands of noisy ones. Low-quality
examples — wrong answers, truncated text, duplicated content — teach the
model to produce them. The roadmap's exit test: "the training set is
clean and deduplicated." Quality filtering is a data-engineering task, not
a training task.

## 3. Deduplication

Near-duplicate examples waste capacity and bias the model toward repeated
patterns. Exact duplicates are trivial to remove; near-duplicates need
normalization and similarity comparison. The deduplicated set is smaller
and the model generalizes better.

## 4. The Train/Eval Split

A held-out set is excluded before training. The split is by example, not
by topic — the eval set must represent the same distribution. The split is
fixed and recorded, so the same eval set measures every training run. The
roadmap's exit test: "the model is evaluated on a held-out set."

## 5. Auditing Before Training

The set is audited before the run: format consistency, answer length
distribution, label balance, and the eval set's coverage. The audit is a
report, not a guess. A set that fails the audit is fixed before training,
never during.

## Common Mistakes

- Training on a noisy set (the model learns the noise).
- No deduplication (repeated patterns dominate).
- Eval set leaking into training.
- Split by topic instead of by example.
- No audit before the run.

## Key Takeaways

1. The format is consistent across the whole set.
2. A few hundred clean examples beat thousands of noisy ones.
3. Deduplication improves generalization.
4. The eval set is fixed, recorded, and excluded from training.
5. Audit before training, never during.