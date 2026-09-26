# Postgres 04: Indexes — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| B-tree | Default index: equality, range, ordering | conversation_id lookup |
| GIN | Inverted index for containment (jsonb, arrays) | meta @> queries |
| GiST | Balanced-tree framework for geometry/NN types | PostGIS (rare here) |
| BRIN | Block-range index for append-only ordered data | event time series |
| EXPLAIN | Planner output showing access paths + unit costs | Seq vs Index Scan |
| Seq Scan | Full-table read; fine small, fatal large | missing-index symptom |
| Index justification | Comment naming the query shape an index serves | drop-if-unused audit |

---

## Alphabetical Glossary

### B-tree

**Definition:** Balanced-tree default index: equality, ranges, ordering, and
prefix matching. The right answer until a specialty proves otherwise.

**Example:**
```sql
CREATE INDEX ON messages (conversation_id, created_at DESC);
```

**Related concepts:** GIN, EXPLAIN

---

### BRIN

**Definition:** Block Range Index: stores min/max per page block. Tiny and
fast for append-only, physically ordered data; useless on random updates.

**Example:**
```sql
CREATE INDEX ON events USING BRIN (created_at);  -- append-only logs
```

**Related concepts:** B-tree, GIN

---

### EXPLAIN

**Definition:** Planner readout of access paths and unit costs. Read before
indexing (diagnosis) and after (proof). Costs are planner units, not ms.

**Example:**
```python
# Index Scan using idx_conv: the plan you wanted to see
```

**Related concepts:** Seq Scan, B-tree

---

### GIN

**Definition:** Generalized Inverted Index over elements/keys. Serves
containment queries on jsonb, arrays, and trigram text search.

**Example:**
```sql
CREATE INDEX ON chunks USING GIN (meta);
```

**Related concepts:** B-tree, `@>`

---

### GiST

**Definition:** Generalized Search Tree framework for geometry, full-text,
and nearest-neighbor types. Know it exists; reach for it rarely.

**Example:**
```sql
-- PostGIS distance queries; not the DevMate retrieval path
```

**Related concepts:** GIN, B-tree

---

### Index justification

**Definition:** A comment on every index naming the query shape it serves.
Makes the unused-index audit decidable and drops safe.

**Example:**
```sql
-- Serves: GET /conversations/{id} message lookup. Drop iff endpoint dies.
```

**Related concepts:** EXPLAIN, B-tree

---

### Seq Scan

**Definition:** Reading the whole table. Correct on tiny tables; the
missing-index symptom on large ones. Context decides whether it's a bug.

**Example:**
```python
# 200-row table: fine — 20M-row table: the sprint's first victim
```

**Related concepts:** EXPLAIN, B-tree

---

## Related Concepts

- **pg_stat_user_indexes**: scan counts per index for the drop audit
- **N+1**: the query-shape bug indexes can't fix (SQLAlchemy 06)
- **Migrations**: where indexes live as versioned schema (Alembic, week 4)

## Key Takeaways

1. Four families, four workload shapes.
2. Plans are read twice: before and after.
3. Unjustified indexes are future write-amplification.
