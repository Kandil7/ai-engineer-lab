# Fine-Tuning 03: Training Data Preparation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Instruction set | The instruction-answer pairs the model trains on | clean, deduplicated |
| Instruction format | The consistent user/assistant shape | {"instruction", "answer"} |
| Quality filtering | Dropping wrong or truncated examples | clean set |
| Deduplication | Removing exact and near-duplicate examples | better generalization |
| Train/eval split | Held-out set excluded before training | fixed and recorded |
| Audit | The pre-training report on the set | format, balance, coverage |

---

## Alphabetical Glossary

### Audit

**Definition:** The pre-training report on the set: format consistency,
answer length distribution, label balance, and eval coverage. A set that
fails the audit is fixed before training.

**Example:**
```python
# audit report: 500 examples, 0 duplicates, eval covers all topics
```

**Related concepts:** Instruction set, Train/eval split

---

### Deduplication

**Definition:** Removing exact and near-duplicate examples. Near-duplicates
need normalization and similarity comparison. The deduplicated set
generalizes better.

**Example:**
```python
# two examples differing by one word -> one kept
```

**Related concepts:** Instruction set

---

### Instruction format

**Definition:** The consistent user/assistant shape of every example. The
model learns the format from the data; a mixed format teaches mixed
behavior.

**Example:**
```python
{"instruction": "ما حكم الصلاة في السفر؟", "answer": "القصر جائز"}
```

**Related concepts:** Instruction set

---

### Instruction set

**Definition:** The instruction-answer pairs the model trains on. A few
hundred clean examples beat thousands of noisy ones.

**Example:**
```python
# 500 deduplicated, audited examples
```

**Related concepts:** Quality filtering, Deduplication

---

### Quality filtering

**Definition:** Dropping low-quality examples: wrong answers, truncated
text, duplicated content. A data-engineering task, not a training task.

**Example:**
```python
# truncated answers removed before training
```

**Related concepts:** Instruction set

---

### Train/eval split

**Definition:** A held-out set excluded before training. Split by example,
not by topic; fixed and recorded so the same eval set measures every run.

**Example:**
```python
# 450 train, 50 eval, recorded in the run config
```

**Related concepts:** Audit

---

## Related Concepts

- **SFT**: the set feeds the SFT loss (topic 01)
- **Data engineering**: quality and dedup are data-engineering skills (stage 5)
- **Training runs**: the split is recorded in the run config (topic 04)

## Key Takeaways

1. The format is consistent across the whole set.
2. A few hundred clean examples beat thousands of noisy ones.
3. Deduplication improves generalization.
4. The eval set is fixed, recorded, and excluded from training.
5. Audit before training, never during.