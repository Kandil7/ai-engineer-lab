# Vector Stores 06: Metadata Filtering — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Metadata filter | Predicate over chunk payloads constraining retrieval | language == python |
| Payload | Per-chunk attribute dict (language, file, date, tenant) | indexed at ingest |
| Selectivity | Fraction of collection a filter admits | 0.001 = one tenant |
| Pre-filtering | Predicates first, ANN on survivors | low-selectivity tenant |
| Post-filtering | ANN first, discard non-matching after | simple, k not guaranteed |
| Payload index | Index making a predicate cheap without scanning | date range pruning |
| Tenant isolation | Per-customer filtering as a correctness property | never leak across tenants |

---

## Alphabetical Glossary

### Metadata filter

**Definition:** A predicate over stored chunk attributes that restricts which
vectors participate in a query. Correctness tool first, performance tool
second.

**Example:**
```python
{"language": "python", "date": {"$gte": "2026-01-01"}}
```

**Related concepts:** Payload, Selectivity

---

### Payload

**Definition:** The attribute dictionary stored alongside each vector:
language, filename, chunk type, repo, date, tenant. Designed at ingest.

**Example:**
```python
# missing tenant in payload -> re-ingest, not a query fix
```

**Related concepts:** Metadata filter, Payload index

---

### Payload index

**Definition:** A store-side index over a payload attribute so filters prune
without scanning. Built for attributes queries actually use.

**Example:**
```python
# indexed date range: 0.1% survivors without touching 99.9% of vectors
```

**Related concepts:** Payload, Selectivity

---

### Post-filtering

**Definition:** Run ANN, then discard non-matching results. Works without
index support but wastes vector work and can return fewer than k hits.

**Example:**
```python
# k=10 requested, 3 survive the filter -> user sees 3
```

**Related concepts:** Pre-filtering, Selectivity

---

### Pre-filtering

**Definition:** Apply predicates before similarity search; rank only eligible
vectors. The correct plan at low selectivity, given index support.

**Example:**
```python
# one tenant of a thousand: search 0.1%, exactly
```

**Related concepts:** Post-filtering, Payload index

---

### Selectivity

**Definition:** Fraction of the collection admitted by a filter. The number
that decides pre- vs post-filtering.

**Example:**
```python
# 0.8: plan barely changes — 0.001: pre-filter or die
```

**Related concepts:** Pre-filtering, Post-filtering

---

### Tenant isolation

**Definition:** Guarantee that queries never return another tenant's data.
Implemented as a mandatory pre-filter, tested adversarially, never optional.

**Example:**
```python
# every query carries tenant == caller, enforced below the API layer
```

**Related concepts:** Metadata filter, Pre-filtering

---

## Related Concepts

- **Hybrid search**: both arms must honor the same filters (topic 05)
- **k guarantee**: post-filtering breaks it; pre-filtering keeps it
- **Re-ingest**: the price of a payload designed too late

## Key Takeaways

1. Selectivity picks the plan.
2. Payloads at ingest, indexes on filtered attributes.
3. Tenant isolation is correctness, not optimization.
