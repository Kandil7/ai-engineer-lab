# PostgreSQL 02: Indexes and Queries

## Topic Overview

An index is the database's shortcut to the rows a query needs. Without it, the database reads every
row (a sequential scan); with it, the lookup is logarithmic. Indexes are the single most effective
performance lever in a relational database, and the single most overused one: every index speeds reads
and slows writes, so the skill is choosing the indexes that match the actual query patterns.

This lecture covers what an index does, B-tree, composite, and GIN indexes, how to read a query plan,
and the mistakes that make an index useless.

The core discipline is evidence: read `EXPLAIN` to see whether the index is used, rather than assuming
it. A query plan shows a sequential scan on a large table, which is the signal for a missing index.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what an index does and its write cost.
2. Choose B-tree, composite, or GIN for a query pattern.
3. Order composite index columns to match the query.
4. Read an `EXPLAIN` plan and spot a sequential scan.
5. Avoid the mistakes that silently disable an index.
6. Explain why indexes follow query patterns, not intuition.

## Prerequisites

- PostgreSQL 01 (schema design) for tables and keys.
- Basic SQL queries with WHERE, ORDER BY, and joins.

---

## 1. What an Index Does

### The structure

An index is a sorted structure that maps a column's values to the rows that hold them. A lookup uses
the index instead of scanning every row:

```sql
CREATE INDEX idx_users_email ON users (email);
```

### The tradeoff

Indexes speed reads and slow writes, because every insert, update, and delete must also update the
indexes. They also consume storage. The tradeoff means indexes are chosen for the queries that matter,
not for every column.

### The exit test

The roadmap's exit test is that queries use indexes. The proof is the query plan: an index scan instead
of a sequential scan on the columns the query filters by.

## 2. B-tree

### The default

The B-tree is the default index: sorted, balanced, and good for equality and range queries:

```sql
CREATE INDEX idx_orders_created ON orders (created_at);
```

### What it serves

Equality (`WHERE email = ...`), range (`WHERE created_at > ...`), and ordering (`ORDER BY`). It is the
right index for the vast majority of cases.

### Unique indexes

A unique index enforces uniqueness and speeds lookups on the same column. A primary key is a unique
index; adding `UNIQUE` to another column creates one there too.

## 3. Composite Indexes

### The idea

A composite index covers multiple columns in a specified order:

```sql
CREATE INDEX idx_messages_session_time ON messages (session_id, created_at);
```

### The order rule

The order matters: a query filtering on `(session_id, created_at)` uses an index on those columns in
that order. A query on `session_id` alone can use the index (it is the leading column); a query on
`created_at` alone cannot:

```python
assert composite_matches(("session_id", "created_at"), ("session_id",))
assert not composite_matches(("session_id", "created_at"), ("created_at",))
```

### The exit test

The roadmap's exit test is that composite indexes match the query patterns. The leading-column rule is
the reason: the index is usable only from its leftmost column onward.

## 4. GIN for JSONB and Text

### What GIN serves

GIN (Generalized Inverted Index) serves JSONB containment and full-text search, where the indexed
values are composite:

```sql
CREATE INDEX idx_docs_tsv ON documents USING GIN (tsv);
```

### The config rule

For text search, the index and the query must use the same text-search configuration. For Arabic, the
config matters: an index built with one config and a query using another will not match. The config is
part of the contract.

### When GIN

GIN is for containment and search, not for equality and range. Choosing it for the wrong pattern
produces a slow index that is never used.

## 5. Reading the Plan

### EXPLAIN

`EXPLAIN` shows how the database will run a query: sequential scan or index scan, estimated rows, and
cost:

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE created_at > '2026-01-01';
```

### What to look for

- **Sequential scan on a large table:** the signal for a missing index.
- **Index scan:** the index is used.
- **Estimated vs actual rows:** a large mismatch means stale statistics (`ANALYZE`).

### The exit test

The roadmap's exit test is that queries are verified with `EXPLAIN`. The plan is the evidence that the
index exists and the query uses it, which is the only way to know without guessing.

## 6. The Exercise

### What it models

The exercise models an index lookup and the composite-index leading-column rule.

### The assertions

```python
idx = Index([("s1", 1), ("s1", 2), ("s2", 3)])
assert idx.lookup("s1") == [1, 2], "index lookup returns the rows"
assert composite_matches(("session_id", "created_at"), ("session_id",))
assert not composite_matches(("session_id", "created_at"), ("created_at",))
```

The last assertion is the lesson: a query on the second column alone cannot use the composite index.

## Real-World Application

- An index on `messages(session_id, created_at)` so a session's messages load in order without a scan.
- A GIN index on a `tsvector` column for Arabic full-text search with the matching config.
- Running `EXPLAIN ANALYZE` on a slow query to confirm the index is used and the estimates are close.
- Adding an index only after a plan shows a sequential scan, not preemptively.

## Common Mistakes

1. **Indexing every column.** Writes slow down for indexes never used.
2. **Composite index columns in the wrong order.** The query cannot use it.
3. **No index on the columns queries filter by.** Sequential scans on large tables.
4. **GIN config mismatch between index and query.** Text search does not match.
5. **Never reading the query plan.** The index's use is assumed.
6. **Assuming an index is used because it exists.** The planner may choose a scan.

## Key Takeaways

1. An index maps values to rows; reads speed up and writes slow down.
2. B-tree is the default for equality and range; unique indexes enforce and speed.
3. Composite indexes must match the query pattern from the leading column.
4. GIN serves JSONB and full-text search; the config must match the query.
5. `EXPLAIN` shows whether the index is used; verify, do not assume.

## Self-Check Questions

1. Why do indexes slow writes, and what does that imply about indexing every column?
2. Why can a query on a composite index's second column alone not use it?
3. When is a GIN index the right choice, and what must match between index and query?
4. What does a sequential scan on a large table tell you, and what is the fix?
5. Why verify with `EXPLAIN` rather than assume the index is used?

## Further Reading / Connections

- PostgreSQL 01 (schema design), 03 (migrations), and 04 (connection pooling).
- DS-Algo 04 (sorting and searching) — the binary-search idea behind B-tree lookup.
- `docs/cheat-sheets/postgres.md` — the command reference.
