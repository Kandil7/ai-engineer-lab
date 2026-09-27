# AI Evaluation 03: Retrieval Evaluation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Recall@k | Relevant passages found in the top k | 2/3 at k=5 |
| Precision@k | Relevant passages among the top k | 2/5 |
| MRR | Reciprocal rank of the first relevant passage | 1.0 = always first |
| Baseline threshold | Metric floor set from a baseline run | recall@5 >= 0.8 |
| Ranked results | Retrieved passages in score order | top k first |
| CI gate | Metrics enforced on every change | drop fails CI |

---

## Alphabetical Glossary

### Baseline threshold

**Definition:** The metric floor set from a baseline run, then enforced in
CI. Without it the gate has no teeth.

**Example:**
```python
# recall@5 >= 0.8, MRR >= 0.7
```

**Related concepts:** CI gate

---

### CI gate

**Definition:** The golden-set metrics enforced on every change. A change
that drops recall@5 below the threshold fails CI.

**Example:**
```python
# CI fails when recall@5 < baseline threshold
```

**Related concepts:** Baseline threshold

---

### MRR

**Definition:** Mean reciprocal rank: the reciprocal of the rank of the
first relevant passage. 1.0 when the answer is always first, 0.5 when
always second. For single-answer queries.

**Example:**
```python
# first relevant at rank 2 -> 1/2 = 0.5
```

**Related concepts:** Recall@k, Precision@k

---

### Precision@k

**Definition:** Of the top k results, how many are relevant. Answers "how
much noise did we show?" Matters when the context budget is tight.

**Example:**
```python
# 2 of the top 5 are relevant -> 0.4
```

**Related concepts:** Recall@k

---

### Ranked results

**Definition:** Retrieved passages in score order, best first. All three
metrics operate on the top k of this ordering.

**Example:**
```python
# retrieved[:k] in score order
```

**Related concepts:** Recall@k, MRR

---

### Recall@k

**Definition:** Of the relevant passages, how many appear in the top k.
Answers "did we find the material?" The primary retrieval metric for RAG.

**Example:**
```python
# 2 of 3 relevant passages in the top 5 -> 2/3
```

**Related concepts:** Precision@k, MRR

---

## Related Concepts

- **Gold dataset**: the relevant passages come from the golden set (topic 01)
- **Reranking**: precision@k improves when ranking improves (rag-system 03)
- **Faithfulness**: recall gates whether the answer can be grounded (topic 02)

## Key Takeaways

1. Recall@k: did we find the material?
2. Precision@k: how much noise did we show?
3. MRR: how high did the first relevant passage rank?
4. The three metrics diagnose different failures.
5. Thresholds from a baseline, enforced in CI.