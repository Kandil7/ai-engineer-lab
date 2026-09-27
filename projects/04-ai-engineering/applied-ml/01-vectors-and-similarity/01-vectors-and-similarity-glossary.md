# Applied ML 01: Vectors and Similarity — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Vector | Ordered list of numbers representing data | term counts, embeddings |
| Dot product | Sum of element-wise products; mixes direction and magnitude | cheap similarity |
| Cosine similarity | Angle-based similarity, magnitude-free | text/embedding default |
| Euclidean distance | Straight-line distance; smaller means closer | magnitude-sensitive |
| Unit vector | Length-1 vector; direction only | normalized embedding |
| Normalization | Scaling to unit length | enables dot-as-cosine |
| Similarity | Geometric nearness under a chosen metric | ranking basis |

---

## Alphabetical Glossary

### Cosine similarity

**Definition:** Dot product divided by both norms; measures angle, ignoring
magnitude. The default metric for text and embeddings.

**Example:**
```python
cosine(a, b)  # 0.93 = near-duplicate, 0.11 = unrelated
```

**Related concepts:** Dot product, Unit vector

---

### Dot product

**Definition:** Sum of element-wise products. Mixes direction and magnitude;
equals cosine only on unit-normalized vectors.

**Example:**
```python
dot(a, b)  # valid cosine stand-in after normalization
```

**Related concepts:** Cosine similarity, Normalization

---

### Euclidean distance

**Definition:** Straight-line distance between vectors. A distance, not a
similarity: smaller wins. Magnitude-sensitive.

**Example:**
```python
euclidean(a, b)  # 0.2 = near, 1.7 = far
```

**Related concepts:** Cosine similarity, Normalization

---

### Normalization

**Definition:** Scaling vectors to unit length so dot product equals cosine
and magnitude stops leaking into rankings.

**Example:**
```python
an = [x / norm(a) for x in a]  # unit vector
```

**Related concepts:** Unit vector, Dot product

---

### Similarity

**Definition:** Geometric nearness under a chosen metric. The basis of
retrieval ranking, classification, and clustering.

**Example:**
```python
# rank candidates by cosine to the query
```

**Related concepts:** Cosine similarity, Euclidean distance

---

### Unit vector

**Definition:** A vector with norm exactly 1. Carries direction only, which
is why dot products between unit vectors are pure angle measurements.

**Example:**
```python
# all corpus vectors unit length -> rankings are angles
```

**Related concepts:** Normalization, Cosine similarity

---

### Vector

**Definition:** An ordered list of numbers representing data. Documents,
embeddings, and queries are all vectors.

**Example:**
```python
a = [3.0, 4.0, 0.0]  # term counts for a document
```

**Related concepts:** Similarity, Dot product

---

## Related Concepts

- **Embeddings**: dense vectors where distance means similarity
- **Retrieval**: ranking by vector similarity
- **Classification**: decision boundaries in vector space

## Key Takeaways

1. Similarity is geometry.
2. Cosine for direction, dot/Euclidean for magnitude.
3. Normalize on write; metric choice changes rankings.