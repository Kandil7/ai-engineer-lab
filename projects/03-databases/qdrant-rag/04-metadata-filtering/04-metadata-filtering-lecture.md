# Qdrant 04: Metadata Filtering

## 🎯 Topic Overview

Payload filters narrow a search before or after scoring. Filtering by
book, page, or language keeps the results inside the right scope. This
lecture covers filter types, pre- vs post-filtering, and the correctness
of tenant isolation.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write payload filters on the collection's fields
2. Combine filters with must, must_not, and should
3. Explain pre-filtering vs post-filtering
4. Use filters for tenant isolation
5. Keep filters aligned with the payload schema

---

## 1. The Filter

A filter selects points by their payload: a book, a page range, a
language. The filter is written against the payload schema — a field that
was not indexed cannot be filtered. The roadmap's exit test: "filters
match the payload schema."

```python
filter_ = Filter(
    must=[
        FieldCondition(key="book", match=MatchValue(value="b3")),
        FieldCondition(key="language", match=MatchValue(value="ar")),
    ]
)
```

## 2. Combining Conditions

Conditions combine with must (all), must_not (none), and should (any).
A query for a book in Arabic uses must on both. The combination is the
query's scope. The roadmap's exit test: "filters combine correctly."

## 3. Pre- vs Post-Filtering

Pre-filtering narrows the candidate set before scoring; post-filtering
scores everything and drops the filtered points after. Pre-filtering is
faster on large collections; post-filtering can return fewer results when
the filter is strict. The choice is a performance decision.

## 4. Tenant Isolation

Filters are the correctness boundary: a user's results must never include
another tenant's data. The tenant filter is applied on every query, always.
A missing tenant filter is a data leak. The roadmap's exit test: "tenant
isolation is enforced by filters."

## 5. Alignment with the Schema

A filter only works on fields the payload schema defines. Adding a filter
field means adding it to the schema and re-ingesting. The filter and the
schema evolve together.

## Common Mistakes

- Filtering on a field not in the payload schema.
- A missing tenant filter (data leak).
- Post-filtering on a huge collection (slow).
- Filter conditions that contradict each other.
- Filters and schema drifting apart.

## Key Takeaways

1. Filters select points by payload.
2. Must, must_not, and should combine the scope.
3. Pre-filtering is faster; post-filtering can drop results.
4. Tenant isolation is a filter, applied on every query.
5. Filters and the payload schema evolve together.