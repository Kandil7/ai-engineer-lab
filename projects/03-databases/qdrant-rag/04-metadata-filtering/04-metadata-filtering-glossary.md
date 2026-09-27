# Qdrant 04: Metadata Filtering — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Filter | Selecting points by payload | book = b3 |
| must | All conditions must hold | book AND language |
| must_not | None of the conditions may hold | exclude a book |
| should | Any condition may hold | OR |
| Pre-filtering | Narrow candidates before scoring | fast on large sets |
| Post-filtering | Score all, drop after | strict filters |
| Tenant isolation | The correctness boundary filter | applied on every query |

---

## Alphabetical Glossary

### Filter

**Definition:** Selecting points by their payload: a book, a page range, a
language. Written against the payload schema.

**Example:**
```python
Filter(must=[FieldCondition(key="book", match=MatchValue(value="b3"))])
```

**Related concepts:** must, Tenant isolation

---

### must

**Definition:** The condition group where all conditions must hold. The
query's scope.

**Example:**
```python
# book = b3 AND language = ar
```

**Related concepts:** must_not, should

---

### must_not

**Definition:** The condition group where none of the conditions may hold.
Excludes points.

**Example:**
```python
# exclude book b9
```

**Related concepts:** must

---

### Post-filtering

**Definition:** Scoring every point, then dropping the filtered points
after. Can return fewer results when the filter is strict.

**Example:**
```python
# score all, then drop points outside the filter
```

**Related concepts:** Pre-filtering

---

### Pre-filtering

**Definition:** Narrowing the candidate set before scoring. Faster on large
collections.

**Example:**
```python
# filter first, then score the candidates
```

**Related concepts:** Post-filtering

---

### should

**Definition:** The condition group where any condition may hold. An OR
within the group.

**Example:**
```python
# book = b3 OR book = b5
```

**Related concepts:** must

---

### Tenant isolation

**Definition:** The correctness boundary: a user's results never include
another tenant's data. A filter applied on every query, always.

**Example:**
```python
# every query carries the tenant filter
```

**Related concepts:** Filter

---

## Related Concepts

- **Collections**: filters run on the payload schema (topic 01)
- **Vector search**: filters narrow the search (topic 02)
- **Hybrid search**: filters apply to both retrievers (topic 03)

## Key Takeaways

1. Filters select points by payload.
2. Must, must_not, and should combine the scope.
3. Pre-filtering is faster; post-filtering can drop results.
4. Tenant isolation is a filter, applied on every query.
5. Filters and the payload schema evolve together.