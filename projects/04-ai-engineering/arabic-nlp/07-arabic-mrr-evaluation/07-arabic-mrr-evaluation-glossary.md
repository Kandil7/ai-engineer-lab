# Arabic NLP 07: MRR Evaluation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| MRR | Mean reciprocal rank of the first relevant passage | 1.0 = always first |
| Recall@k | Relevant passages found in the top k | 1.0 at k=5 |
| Golden set | Fixed Arabic queries with known relevant passages | verse, hadith, fiqh |
| Baseline threshold | The metric floor from a baseline run | recall@5 >= 0.8 |
| CI gate | Metrics enforced on every change | drop fails CI |
| Reciprocal rank | 1 / rank of the first relevant | 1/2 = 0.5 |
| Unanswerable query | A query with no relevant passage | abstention case |

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
# CI fails when recall@5 < baseline
```

**Related concepts:** Baseline threshold

---

### Golden set

**Definition:** A fixed set of Arabic queries with known relevant passages.
The yardstick every retrieval change is measured against.

**Example:**
```python
# 50 queries: verse, hadith, fiqh, unanswerable
```

**Related concepts:** Unanswerable query

---

### MRR

**Definition:** Mean reciprocal rank: the mean of the reciprocal ranks of
the first relevant passage. Rewards getting the answer to the top.

**Example:**
```python
# first relevant at rank 2 -> 0.5
```

**Related concepts:** Reciprocal rank, Recall@k

---

### Recall@k

**Definition:** Whether the relevant passages appear in the top k. Answers
"did we find the material?"

**Example:**
```python
# the one relevant passage in the top 5 -> 1.0
```

**Related concepts:** MRR

---

### Reciprocal rank

**Definition:** 1 divided by the rank of the first relevant passage. The
unit MRR averages.

**Example:**
```python
# rank 1 -> 1.0, rank 2 -> 0.5
```

**Related concepts:** MRR

---

### Unanswerable query

**Definition:** A query with no relevant passage in the corpus. Belongs in
the golden set to test abstention.

**Example:**
```python
# a question about a topic the corpus does not cover
```

**Related concepts:** Golden set

---

## Related Concepts

- **ANN search**: recall loss is measured with these metrics (topic 06)
- **Hybrid search**: the fused ranking is evaluated (topic 05)
- **Retrieval evaluation**: the same metrics in ai-evaluation (ai-evaluation 03)

## Key Takeaways

1. MRR rewards ranking the first relevant passage high.
2. Recall@k rewards finding the material.
3. The two metrics diagnose different failures.
4. The Arabic golden set is the yardstick.
5. The metrics gate changes in CI.