# Embeddings 04: Quality Evaluation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Golden pairs | Hand-verified text pairs with expected similarity | positive + negative |
| Positive pair | Same concept, different wording | 0.9 expected |
| Negative pair | Different concepts, similar wording | 0.3 expected |
| Cosine similarity | The measured closeness | compared to target |
| Retrieval accuracy | Correct docs in the top-k | end-to-end |
| Consistency | Same text, same vector | 100% |
| Regression gate | Metrics on every embedding change | model swap |

---

## Alphabetical Glossary

### Consistency

**Definition:** The same text produces the same embedding every time. A
nondeterministic model breaks the cache and the retrieval.

**Example:**
```python
# embed(text) == embed(text) always
```

**Related concepts:** Regression gate

---

### Cosine similarity

**Definition:** The measured closeness between two embeddings. Compared to
the expected value in the golden pairs.

**Example:**
```python
cosine(embed(a), embed(b)) >= 0.85
```

**Related concepts:** Golden pairs

---

### Golden pairs

**Definition:** Hand-verified text pairs with an expected similarity.
Positive pairs: same concept, different wording. Negative pairs: different
concepts, similar wording.

**Example:**
```python
("النسبة المئوية", "Percentage", 0.85)
```

**Related concepts:** Positive pair, Negative pair

---

### Negative pair

**Definition:** Different concepts with similar wording. The control that
proves the model separates them.

**Example:**
```python
("النسبة المئوية", "Physics", 0.3)
```

**Related concepts:** Golden pairs

---

### Positive pair

**Definition:** Same concept, different wording. Should embed close.

**Example:**
```python
("ما هو العدد الأولي؟", "What is a prime number?", 0.9)
```

**Related concepts:** Golden pairs

---

### Regression gate

**Definition:** The metrics running on every embedding change — a model
swap, a normalization change. A drop is a regression.

**Example:**
```python
# CI fails when retrieval accuracy drops
```

**Related concepts:** Retrieval accuracy

---

### Retrieval accuracy

**Definition:** Whether the correct documents appear in the top-k for the
golden queries. The end-to-end test of embeddings plus search.

**Example:**
```python
# correct doc in the top-5 for 80% of queries
```

**Related concepts:** Regression gate

---

## Related Concepts

- **Model selection**: the choice is validated by these metrics (topic 01)
- **Batch processing**: the eval runs on batches (topic 02)
- **Retrieval evaluation**: the same metrics in ai-evaluation (ai-evaluation 03)

## Key Takeaways

1. Golden pairs cover similar and dissimilar texts.
2. Cosine similarity is compared to the expected value.
3. Retrieval accuracy is the end-to-end test.
4. Consistency is 100% — same text, same vector.
5. The metrics gate every embedding change.