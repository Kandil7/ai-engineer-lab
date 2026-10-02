# Databases — PG03: JSONB Queries

## Topic Overview

Semi-structured payloads — chunk metadata, eval configs, provider responses —
don't deserve their own tables, but they do deserve querying. JSONB stores
parsed binary JSON with operators for extraction, containment, and existence,
plus GIN indexes that make path queries fast. This lecture is the full
operator set plus the indexing rule, anchored on DevMate's own `metadata`
column.

The design question underneath is always the same: which fields stay relational
and which move into the document? Columns you filter, join, or constrain belong
in the schema; payload you carry along and occasionally inspect belongs in
JSONB. Getting that split right keeps the relational core fast and the flexible
remainder queryable.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Extract values with `->`, `->>`, `#>` and state the type each returns
2. Test containment with `@>` and existence with `?`, `?|`, `?&`
3. Choose `jsonb` over `json` (parsed, indexed, нормативных) every time
4. Add a GIN index and verify with EXPLAIN that path queries use it
5. Model DevMate-style metadata (language, repo, chunk_type) as queryable JSONB

## Prerequisites

| Need | Where |
|---|---|
| Type mapping basics | [02](02-postgres-types-lecture.md) |
| Index reading (EXPLAIN) | [04](04-indexes-postgres-lecture.md) (read after, or alongside) |
| The runnable exercise | [03-jsonb-queries.py](03-jsonb-queries.py) |

## 1. Extraction: `->`, `->>`, `#>`

```sql
-- -> returns jsonb (chainable), ->> returns text (terminal), #> takes a path
SELECT meta -> 'repo'          AS repo_json,   -- jsonb "devmate"
       meta ->> 'language'     AS lang,        -- text python
       meta #> '{span,lines}'  AS lines        -- nested path
FROM chunks WHERE id = 1;
```

The `->` vs `->>` confusion is the #1 JSONB bug: comparing `->` output to
text always fails because one side is still JSON. Extract text at the
boundary, compare text to text.

Chain `->` to walk nesting, terminate with `->>` when you need a value for
comparison, ordering, or display. `#>`/`#>>` take a text-array path for deep
access in one step.

## 2. Containment and Existence

```sql
-- @>: does the document contain this structure? (GIN-indexable)
SELECT * FROM chunks WHERE meta @> '{"language": "python"}';
-- ?: does the key exist? ?|: any of these keys? ?&: all of these keys?
SELECT * FROM chunks WHERE meta ? 'repo' AND meta ?& array['repo', 'chunk_type'];
```

Design payloads so the hot queries are containment checks — `@>` with a GIN
index is the fast path; deep nested `#>` extractions in WHERE clauses are the
slow one.

Existence operators answer schema questions ("which chunks carry a repo key?")
without knowing the values, which makes them the right tool for evolving
payloads where keys come and go.

## 3. `json` vs `jsonb`, Settled

`json` stores exact text (whitespace, duplicate keys preserved) and parses
on every read. `jsonb` stores parsed binary (normalized, indexed). Unless
you need byte-exact round-trips of malformed input, `jsonb` wins on every
axis that matters. New columns are `jsonb`; the exercise asserts this.

The normalization has one visible consequence: key order and duplicate keys
are not preserved. If byte fidelity matters (signed payloads, audit logs),
store the raw text alongside — but query the `jsonb` copy.

## 4. GIN Indexing and Verification

```sql
CREATE INDEX ON chunks USING GIN (meta);
-- then prove it:
EXPLAIN SELECT * FROM chunks WHERE meta @> '{"language": "python"}';
-- Bitmap Heap Scan + Bitmap Index Scan on the GIN index: indexed.
-- Seq Scan: the index is missing, wrong type, or the planner chose otherwise.
```

Week 4's rule — indexes justified in comments — starts here: the comment
names the query shape the index serves, so the next engineer knows what
breaks if it is dropped.

GIN indexes are heavier on writes than B-trees, especially on churning
documents. Budget the write cost, and consider `jsonb_path_ops` when your
queries are pure containment — a smaller, faster GIN variant.

## 5. Real-World Application

DevMate's `metadata` column carries language, repo, and chunk type for every
ingested chunk. The retrieval path filters `meta @> '{"language": "arabic"}'`
before vector search, so the GIN index on `meta` is on the hot path of every
query. When a new metadata key is added, the migration adds the key to
payloads and the justification comment names the queries it will serve —
exactly the discipline this lecture teaches.

## Common Mistakes

- Comparing `->` (jsonb) output to text literals — always fails silently.
- `json` columns for queryable payloads (parse on every read, no GIN).
- Deep `#>` extractions in WHERE without a GIN index (full scan in disguise).
- Storing relational data as JSONB because "flexible" — joins still beat documents.
- GIN on high-churn documents without budgeting write amplification.

## DevMate Connection

This is the `metadata` column's lecture: `mapped_column(JSONB,
name="metadata")`, queried by language/repo/chunk_type to feed the
metadata-filtering fold-in. The model-layer `meta` rename already proved the
mapping works both directions; these operators are how week 4 filters on it.

## Key Takeaways

1. `->` chains, `->>` terminates as text, `@>` is the indexed fast path.
2. `jsonb` always, unless byte-exactness is the requirement.
3. GIN + EXPLAIN proof, with the justification in a comment.
4. Payloads are designed for their hottest containment query.
5. Relational data stays relational; JSONB carries the flexible remainder.

## Self-Check Questions

1. Why does `meta -> 'language' = 'python'` never match?
2. Which operator answers "which chunks carry a repo key" without knowing values?
3. When is `json` the right choice over `jsonb`?
4. What EXPLAIN output proves the GIN index is used?
5. Why is storing join keys inside JSONB a design smell?

## Further Reading / Connections

- Next: PG04, Indexes in Postgres.
- `sql-fundamentals/10-indexes-and-plans/` for plan reading.
- Exercise: `03-jsonb-queries.py`.
