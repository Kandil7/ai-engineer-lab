# Databases — PG04: Indexes in Postgres

## Topic Overview

Every week-4 SQL sprint starts here: joins are only as fast as their lookup
paths, and lookup paths are indexes. This lecture covers B-tree defaults,
GIN/GiST specialties, BRIN for append-only data, reading EXPLAIN output, and
the discipline week 4 demands — every index justified in a comment naming
the query shape it serves.

An index is a bet: you pay write cost and RAM on every write for faster reads
on a specific query shape. Bets without a named query behind them lose money.
The sprint loop in this lecture — slow query, plan, hypothesis, index,
re-measure — is how that bet is placed deliberately and verified honestly.

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

Composite B-trees follow the leftmost-prefix rule: an index on `(a, b)` serves
predicates on `a` and on `(a, b)`, but not on `b` alone. Order the columns by
the queries, most selective and most filtered first.

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

`EXPLAIN (ANALYZE, BUFFERS)` runs the query and reports actual rows and buffer
hits — the difference between the planner's estimate and reality is where the
real diagnosis lives. Beware cache warmth lying about wall time; confirm the
plan changed, not just the milliseconds.

## 3. The Sprint Loop (Week 4 Protocol)

Slow query from the "most expensive queries" view → `EXPLAIN (ANALYZE,
BUFFERS)` → hypothesis (which access path is missing) → create index →
re-run EXPLAIN → confirm the plan changed AND wall time dropped. Both
confirmations: plans can improve while time doesn't (tiny tables), and time
can improve while the plan is still wrong (cache warmth lying to you).

Write the hypothesis down before creating the index. If the plan does not
change, the hypothesis was wrong — drop the index and form a new one. Indexes
created "just in case" accumulate into write amplification that shows up
months later as slow ingestion.

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

Partial indexes (`WHERE revoked = false`) shrink the structure to the rows
queries actually touch — smaller, faster, cheaper to maintain. Expression
indexes serve computed predicates, but the query must match the expression
exactly.

## 5. Real-World Application

The week-4 SQL sprint is this protocol applied to DevMate's own queries: the
cost-per-query view identifies victims, EXPLAIN diagnoses, indexes with
justification comments fix. The `(conversation_id, created_at DESC)` composite
serves the conversation view's ordered lookup in one index-only path; the GIN
index on chunk metadata serves the retrieval filter. Both carry comments
naming their queries, so the quarterly audit can verify each still earns its
write cost.

## Common Mistakes

- Indexing every column "just in case" (write amplification, RAM).
- Reading EXPLAIN cost numbers as milliseconds (they're planner units).
- Creating the index but never re-running EXPLAIN to confirm the plan changed.
- GIN on high-churn columns without budgeting the write cost.
- Forgetting that `OR` across columns defeats single-column indexes.
- Trusting wall time without checking the plan (cache warmth lies).

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
4. Composite order follows the queries; partial indexes shrink the structure.
5. Confirm the plan changed AND the wall time dropped.

## Self-Check Questions

1. Which index family serves `meta @> '{"language": "python"}'`, and why?
2. What does a Nested Loop with 10k iterations usually indicate?
3. Why must both the plan and the wall time improve?
4. How do you find an index that earns nothing?
5. Why can `OR` defeat a single-column index?

## Further Reading / Connections

- Next: PG05, Transactions and MVCC.
- `sql-fundamentals/10-indexes-and-plans/` and `14-query-optimization/`.
- Exercise: `04-indexes-postgres.py`.
