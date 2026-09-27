# PostgreSQL 02: Indexes and Queries

## 🎯 Topic Overview

An index is the database's shortcut to the rows a query needs. Without it,
the database scans every row; with it, the lookup is logarithmic. This
lecture covers B-tree, composite, and GIN indexes, and how to read a query
plan.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what an index does
2. Choose B-tree, composite, or GIN
3. Write composite indexes for query patterns
4. Read an EXPLAIN plan
5. Avoid index mistakes

---

## 1. What an Index Does

An index is a sorted structure that maps a column's values to the rows
that hold them. A lookup uses the index instead of scanning every row. The
tradeoff: indexes speed reads and slow writes. The roadmap's exit test:
"queries use indexes."

```sql
CREATE INDEX idx_users_email ON users (email);
```

## 2. B-tree

The B-tree is the default index: sorted, balanced, good for equality and
range queries. Most indexes are B-trees. A unique index enforces
uniqueness and speeds lookups on the same column.

## 3. Composite Indexes

A composite index covers multiple columns in order. The order matters:
a query filtering on (session_id, created_at) uses an index on those two
columns in that order. The roadmap's exit test: "composite indexes match
the query patterns."

```sql
CREATE INDEX idx_messages_session_time ON messages (session_id, created_at);
```

## 4. GIN for JSONB and Text

GIN indexes serve JSONB containment and full-text search. A GIN index on
a tsvector column makes text search fast. For Arabic text, the search
config matters — the index must use the same config as the query.

## 5. Reading the Plan

EXPLAIN shows how the database will run a query: sequential scan or index
scan, estimated rows, and cost. A sequential scan on a large table is the
signal for a missing index. The roadmap's exit test: "queries are
verified with EXPLAIN."

## Common Mistakes

- Indexing every column (write slowdown).
- Composite index columns in the wrong order.
- No index on the columns queries filter on.
- GIN config mismatch between index and query.
- Never reading the query plan.

## Key Takeaways

1. An index maps values to rows; reads speed up, writes slow down.
2. B-tree is the default for equality and range.
3. Composite indexes must match the query pattern.
4. GIN serves JSONB and full-text search.
5. EXPLAIN shows whether the index is used.