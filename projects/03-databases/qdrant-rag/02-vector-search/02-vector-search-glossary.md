# Qdrant 02: Vector Search — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Query embedding | The query embedded with the collection's model | same model |
| Search | The top-k points by similarity | client.search |
| Score | The similarity measure | cosine |
| Limit | The cap on returned points | 10 |
| Score threshold | The similarity floor | 0.7 |
| Top-k | The k most similar points | top-10 |
| Embedding mismatch | A different model or size | silent failure |

---

## Alphabetical Glossary

### Embedding mismatch

**Definition:** The query embedded with a different model or size than the
collection. A silent failure — search returns garbage without error.

**Example:**
```python
# collection at 768 dims, query at 1536 dims -> meaningless
```

**Related concepts:** Query embedding

---

### Limit

**Definition:** The cap on how many points search returns. Controls the
context budget.

**Example:**
```python
results = client.search(..., limit=10)
```

**Related concepts:** Score threshold

---

### Query embedding

**Definition:** The query embedded with the same model that embedded the
collection. A mismatch produces meaningless similarity.

**Example:**
```python
query_vector = embed(query)
```

**Related concepts:** Embedding mismatch

---

### Score

**Definition:** The similarity measure between the query and each point.
Higher is more similar for cosine. The raw material for thresholds and
reranking.

**Example:**
```python
# result.score = 0.87
```

**Related concepts:** Score threshold

---

### Score threshold

**Definition:** The similarity floor that drops weak matches. Keeps weak
matches out of the context.

**Example:**
```python
results = client.search(..., score_threshold=0.7)
```

**Related concepts:** Score, Limit

---

### Search

**Definition:** The operation that returns the top-k points by similarity,
each with a score.

**Example:**
```python
client.search(collection_name="athar", query_vector=qv, limit=10)
```

**Related concepts:** Top-k, Score

---

### Top-k

**Definition:** The k most similar points returned by search.

**Example:**
```python
# top-10 points by cosine similarity
```

**Related concepts:** Search

---

## Related Concepts

- **Collections**: search runs on a collection (topic 01)
- **Hybrid search**: vector search combines with keyword (topic 03)
- **Metadata filtering**: filters narrow the search (topic 04)

## Key Takeaways

1. The query is embedded with the same model as the collection.
2. Search returns the top-k points with scores.
3. The score measures similarity.
4. The limit and threshold control the context budget.
5. An embedding mismatch fails silently.