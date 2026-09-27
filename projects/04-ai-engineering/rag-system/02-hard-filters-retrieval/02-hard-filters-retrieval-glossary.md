# RAG System 02: Hard Filters and Retrieval — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hard filter | Predicate constraining retrieval before ranking | language == ar |
| Selectivity | Fraction of collection a filter admits | 0.001 = one tenant |
| Pre-filtering | Predicates first, then similarity search | low-selectivity correct |
| Post-filtering | Similarity first, then discard | simple, k not guaranteed |
| Tenant isolation | Mandatory per-tenant filter, never optional | correctness |
| Payload | Per-chunk attribute dict | designed at ingest |
| Hybrid leak | One arm ignoring the filter | fused result leaks |

---

## Alphabetical Glossary

### Hard filter

**Definition:** A predicate over chunk payloads constraining retrieval
before ranking. A correctness tool first, performance second.

**Example:**
```python
{"language": "ar", "book_id": "b1"}
```

**Related concepts:** Selectivity, Pre-filtering

---

### Hybrid leak

**Definition:** One retrieval arm ignoring the filter while the other honors
it, so the fused result leaks. Both arms must inherit the same filter.

**Example:**
```python
# dense filters, lexical does not -> fused result crosses the boundary
```

**Related concepts:** Hard filter, Tenant isolation

---

### Payload

**Definition:** The per-chunk attribute dictionary (language, book, version,
date). Designed at ingest; a missing attribute is a re-ingest.

**Example:**
```python
{"language": "ar", "book_id": "b1", "source_version": "v2"}
```

**Related concepts:** Hard filter

---

### Post-filtering

**Definition:** Running similarity search first, then discarding
non-matching results. Simple, but wastes vector work and can return fewer
than k results.

**Example:**
```python
# k=10 requested, 3 survive the filter -> user sees 3
```

**Related concepts:** Pre-filtering, Selectivity

---

### Pre-filtering

**Definition:** Applying predicates before similarity search; rank only
eligible vectors. Correct at low selectivity, given index support.

**Example:**
```python
# one tenant of a thousand: search 0.1%, exactly
```

**Related concepts:** Post-filtering, Selectivity

---

### Selectivity

**Definition:** The fraction of the collection a filter admits. The number
that decides pre- vs post-filtering.

**Example:**
```python
# 0.8: plan barely changes — 0.001: pre-filter or die
```

**Related concepts:** Pre-filtering, Post-filtering

---

### Tenant isolation

**Definition:** The guarantee that queries never return another tenant's
data. A mandatory pre-filter enforced below the API layer.

**Example:**
```python
# every query carries tenant == caller, enforced, never optional
```

**Related concepts:** Hard filter, Pre-filtering

---

## Related Concepts

- **Hybrid search**: both arms must honor filters (arabic-nlp 05)
- **OWASP RAG security**: isolation as an ingestion/retrieval control
- **Payload indexes**: making filters cheap (vector-stores 06)

## Key Takeaways

1. Filters are correctness tools first.
2. Selectivity picks the plan.
3. Tenant isolation is mandatory.
4. Both arms honor the same filters.