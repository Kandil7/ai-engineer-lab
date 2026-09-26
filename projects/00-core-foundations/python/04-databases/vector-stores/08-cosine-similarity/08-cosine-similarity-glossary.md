# Vector Stores 08: Cosine Similarity — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Unit vector | Length-1 vector; direction only | normalized embedding |
| Normalization | Dividing by norm to force unit length | ingest pipeline step |
| Unit-vector identity | cos(a,b) = a·b on normalized vectors | dot-product indexes |
| Metric probe | Known-vector queries verifying a store's metric | orthogonal/duplicate/scaled |
| Norm drift | Stored vectors losing unit length over updates | re-ingest trigger |
| Length bias | Long documents outranking on magnitude, not relevance | unnormalized symptom |

---

## Alphabetical Glossary

### Length bias

**Definition:** Ranking distortion where large-norm documents win on
magnitude under dot/L2 metrics. The signature symptom of unnormalized data.

**Example:**
```python
# longest file ranks top-1 for every query -> check stored norms
```

**Related concepts:** Normalization, Unit-vector identity

---

### Metric probe

**Definition:** Three insert-and-query tests (orthogonal → 0, duplicate → 1,
scaled copy → 1 iff magnitude-free) that verify a store's metric claim.

**Example:**
```python
# scaled copy ranks differently -> "cosine" index is really unnormalized dot
```

**Related concepts:** Unit-vector identity, Cosine similarity

---

### Normalization

**Definition:** Scaling vectors to unit length at write time so dot product
equals cosine similarity and magnitude stops leaking into rankings.

**Example:**
```python
v / np.linalg.norm(v)  # once at ingest, never per query
```

**Related concepts:** Unit vector, Unit-vector identity

---

### Norm drift

**Definition:** Stored vectors deviating from unit length after updates or
migration bugs. Detected by norm-variance checks; fixed by re-ingest.

**Example:**
```python
# norms std > 1e-6 on a "normalized" collection -> investigate writes
```

**Related concepts:** Normalization, Length bias

---

### Unit vector

**Definition:** A vector with norm exactly 1. Carries direction only, which
is why dot products between unit vectors are pure angle measurements.

**Example:**
```python
# all corpus vectors unit length -> rankings are angles, nothing else
```

**Related concepts:** Normalization, Cosine similarity

---

### Unit-vector identity

**Definition:** The equality cos(a,b) = a·b when both vectors are normalized.
The one-line justification for dot-product indexes in retrieval.

**Example:**
```python
# store normalized, query normalized, compare with a single dot product
```

**Related concepts:** Cosine similarity, Dot product

---

## Related Concepts

- **Dot product**: the cheap operation the identity unlocks
- **Re-ingest**: the fix for stored-geometry bugs (no query patch substitutes)
- **Qdrant metric config**: the one-line production consequence

## Key Takeaways

1. One identity underlies every production cosine index.
2. Writes normalize; queries dot-product.
3. Prove the metric with three probes.
