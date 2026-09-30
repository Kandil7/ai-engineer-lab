# Qdrant 04: Metadata Filtering

## Topic Overview

Payload filters narrow a search before or after scoring, keeping the results inside the right scope. They
are correctness tools as much as performance tools: tenant isolation, language restriction, and source
version are all filters, and a missing one is a data leak rather than a slightly worse answer.

This lecture covers filter types and conditions, pre-filtering versus post-filtering, tenant isolation,
and keeping filters aligned with the payload schema.

The most important rule is that tenant isolation is a filter applied on every query, always. A missing
tenant filter lets one user's data into another's results, which is a security incident, not a retrieval
miss (RAG System 02, 08).

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write payload filters on the collection's fields.
2. Combine conditions with must, must_not, and should.
3. Explain pre-filtering versus post-filtering.
4. Enforce tenant isolation with filters.
5. Keep filters aligned with the payload schema.
6. Explain why a missing tenant filter is a leak.

## Prerequisites

- Qdrant 01 (collections and points) for the payload schema.
- RAG System 02 (hard filters) and 08 (context security) for the broader treatment.

---

## 1. The Filter

### What it does

A filter selects points by their payload: a book, a page range, a language:

```python
filter_ = Filter(must=[FieldCondition(key="book", match=MatchValue(value="b3"))])
```

### The schema dependency

The filter is written against the payload schema; a field that was not stored and indexed cannot be
filtered (Qdrant 01). The schema and the filters evolve together.

### The exit test

The roadmap's exit test is that filters match the payload schema, which is the precondition for the
filter to work.

## 2. Combining Conditions

### The operators

Conditions combine with:

- **must:** all conditions hold.
- **must_not:** no condition holds.
- **should:** at least one condition holds.

```python
apply_filter(points, {"tenant": "t1", "book": "b3"})  # both must hold
```

### The scope

The combination is the query's scope. A query for a book in Arabic uses `must` on both; a query for a
book in either of two editions uses `should` on the editions.

### The exit test

The roadmap's exit test is that filters combine correctly, which is what defines the query's scope
precisely.

## 3. Pre-filtering Versus Post-filtering

### The two plans

- **Pre-filtering** narrows the candidate set before scoring, so only eligible points are compared.
- **Post-filtering** scores everything and drops the filtered points after.

### The choice

Pre-filtering is faster on large collections because it scores fewer points, but it needs index support.
Post-filtering is simpler but can return fewer than k results, because it removes candidates after they
consumed slots:

```python
leak = apply_filter(
    points, {"book": "b3"}
)  # t2 data included without the tenant filter
```

### The exit test

The roadmap's exit test is that the filtering plan matches the selectivity, which is a performance
decision with a correctness edge for tenant isolation.

## 4. Tenant Isolation

### The rule

The tenant filter is applied on every query, always. A query without it leaks another tenant's data:

```python
results = tenant_query(points, "t1", ["الصلاة"])
assert {p["id"] for p in results} == {"a1"}, "t2 data excluded"
```

### Why it is a leak

A missing tenant filter does not produce a slightly worse answer; it produces another user's data. This
is the same failure mode as a missing tenant filter in the retrieval layer (RAG System 02), and the
enforcement point is the retrieval boundary.

### The enforcement

Enforce the filter in the query function, not in each caller, so it cannot be forgotten. The filter is
part of the retrieval contract, and the collection's payload carries the tenant field for it.

### The exit test

The roadmap's exit test is that tenant isolation is enforced by filters, which is what makes it a
correctness property rather than a convention.

## 5. Alignment with the Schema

### The rule

A filter only works on fields the payload schema defines. Adding a filter field means adding it to the
schema and re-ingesting (Qdrant 01):

```text
new filter field -> payload schema change -> re-ingest
```

### Why it matters

Filters and schema drifting apart is how a filter silently matches nothing. The two are designed
together, and a new filter is a schema change, not a query change.

### The exit test

The roadmap's exit test is that filters and the schema evolve together, which is what keeps the filters
working.

## 6. The Exercise

### What it models

The exercise models payload filters, tenant isolation, and the leak from a missing tenant filter.

### The assertions

```python
filtered = apply_filter(points, {"book": "b3"})
assert {p["id"] for p in filtered} == {"a1", "b1"}
results = tenant_query(points, "t1", ["الصلاة"])
assert {p["id"] for p in results} == {"a1"}, "t2 data excluded"
leak = apply_filter(points, {"book": "b3"})
assert any(p["payload"]["tenant"] == "t2" for p in leak), "leak without tenant filter"
```

The leak assertion makes the consequence concrete: without the tenant filter, another tenant's data
appears.

## Real-World Application

- Filtering Athar retrieval by `book_id` and `language` so the results stay in scope.
- Enforcing a tenant filter on every query so no customer sees another's data.
- Filtering by `source_version` so a stale or superseded passage never surfaces.
- Adding a filter field to the payload schema before ingesting, not after.

## Common Mistakes

1. **Filtering on a field not in the payload schema.** The filter matches nothing.
2. **A missing tenant filter.** A data leak.
3. **Post-filtering on a huge collection.** Slow and can drop results.
4. **Filter conditions that contradict.** An empty result, silently.
5. **Filters and schema drifting apart.** A filter that silently stops working.
6. **Enforcing the tenant filter in each caller.** A caller will forget.

## Key Takeaways

1. Filters select points by payload and depend on the payload schema.
2. Must, must_not, and should combine the query's scope.
3. Pre-filtering is faster; post-filtering can drop results.
4. Tenant isolation is a filter applied on every query, enforced at the retrieval boundary.
5. Filters and the payload schema evolve together.

## Self-Check Questions

1. Why can a filter only work on a field in the payload schema?
2. What do must, must_not, and should express?
3. When is pre-filtering the right plan, and what is the risk of post-filtering?
4. Why is a missing tenant filter a data leak rather than a retrieval miss?
5. Why does adding a filter field require a re-ingest?

## Further Reading / Connections

- Qdrant 01 (collections and points) and 02 (vector search) and 03 (hybrid search).
- RAG System 02 (hard filters) and 08 (context security) — the broader treatment.
- PostgreSQL 02 (indexes and queries) — the analogous filter-and-index idea in a relational store.
- `docs/cheat-sheets/qdrant.md` — the command reference.
