# Databases — PG04: Indexes in Postgres

## Topic Overview

Every week-4 SQL sprint starts here: joins are only as fast as their lookup
paths, and lookup paths are indexes. This lecture covers B-tree defaults,
GIN/GiST specialties, BRIN for append-only data, reading EXPLAIN output, and
the discipline week 4 demands — every index justified in a comment naming
the query shape it serves.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose B-tree (default), GIN (jsonb/arrays/trigrams), GiST (geometry), BRIN (append-only) correctly
2. Read EXPLAIN: Seq Scan vs Index/Bitmap scans, and what each implies
3. Detect unused indexes (write cost with zero read benefit) and drop them
4. Write the justification comment for every index you create
5. Run the SQL-sprint loop: slow query → EXPLAIN → hypothesis → index → re-measure

## Prerequisites

| Need | Where |
|---|---|
| DDL, basic SELECT | `sql-fundamentals/02-ddl-schema/`, `04-select-basics/` |
| JSONB operators + GIN | [03](03-jsonb-queries-lecture.md) |
| The runnable exercise | [04-indexes-postgres.py](04-indexes-postgres.py) |

## 1. The Four Index Families

```sql
CREATE INDEX ON messages (conversation_id);            -- B-tree: default, equality + range + order
CREATE INDEX ON chunks USING GIN (meta);               -- GIN: jsonb containment, arrays, trigrams
CREATE INDEX ON events USING BRIN (created_at);        -- BRIN: append-only time series, tiny
-- GiST: geometry and nearest-neighbor types (know it exists; reach rarely)
```

B-tree answers "find and sort"; GIN answers "contains"; BRIN answers
"roughly where in an append-only pile". Choosing wrong costs twice: the
index doesn't help, and every write still pays for it.

## 2. Reading EXPLAIN

```python
# Seq Scan on messages            -> no usable index (or tiny table: fine)
# Index Scan using idx_conv       -> B-tree lookup: the good path
# Bitmap Heap Scan + Bitmap Index -> GIN/combined: the good composite path
# Nested Loop with 10k iterations -> the N+1 wearing a costume: fix the query
```

Read plans before creating indexes: the plan tells you which access path the
query needs, and half of "slow query" tickets are missing WHERE clauses or
accidental cross joins, not missing indexes.

## 3. The Sprint Loop (Week 4 Protocol)

Slow query from the "most expensive queries" view → `EXPLAIN (ANALYZE,
BUFFERS)` → hypothesis (which access path is missing) → create index →
re-run EXPLAIN → confirm the plan changed AND wall time dropped. Both
confirmations: plans can improve while time doesn't (tiny tables), and time
can improve while the plan is still wrong (cache warmth lying to you).

## 4. Indexes Cost Too

Every index taxes writes and eats RAM. Audit quarterly: `pg_stat_user_indexes`
shows scans per index — zero scans over a full workload cycle means drop it
(after checking it isn't the quarterly-report index). The justification
comment from section 5 is what makes this audit possible.

```sql
-- Serves: messages-by-conversation lookup in GET /conversations/{id} (week 4 API).
-- Drop iff that endpoint goes away.
CREATE INDEX ON messages (conversation_id, created_at DESC);
```

## Common Mistakes

- Indexing every column "just in case" (write amplification, RAM).
- Reading EXPLAIN cost numbers as milliseconds (they're planner units).
- Creating the index but never re-running EXPLAIN to confirm the plan changed.
- GIN on high-churn columns without budgeting the write cost.

## DevMate Connection

The SQL sprint deliverable is literally this protocol applied to DevMate's
own queries: the cost-per-query view identifies victims, EXPLAIN diagnoses,
indexes with justification comments fix. Migrations carry the indexes, and
the comments carry the reasoning — `migrations/` is where this lecture's
discipline becomes schema.

## Key Takeaways

1. B-tree default, GIN contains, BRIN append-only, GiST geometry.
2. EXPLAIN first, index second, EXPLAIN again third.
3. Every index carries its justification comment or gets dropped in audit.
