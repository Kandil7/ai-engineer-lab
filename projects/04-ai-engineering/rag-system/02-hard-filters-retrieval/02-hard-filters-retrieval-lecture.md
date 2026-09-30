# RAG System 02: Hard Filters and Retrieval

## Topic Overview

Hard filters constrain retrieval before ranking: tenant, language, source version, date
range, document type. They are correctness tools first and performance tools second,
because a filter that lets the wrong data through is a security bug, not a retrieval
inconvenience. In a multi-tenant or multi-source system, the filter is what keeps one user's
data out of another's answer.

This lecture covers the filter types, the choice between pre-filtering and post-filtering
and why selectivity decides it, why tenant isolation must be a mandatory pre-filter, and how
filters apply to both arms of hybrid retrieval. The through-line is that filters are a
retrieval contract, designed at ingest time and enforced once at the boundary, not a
query-time afterthought.

The most important claim here is that a filter's failure mode is silent leakage. A ranking
bug returns a slightly worse answer; a filter bug returns someone else's data, which is why
this is the security-adjacent topic in the retrieval module.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write equality, membership, range, and version filters over chunk payloads.
2. Choose pre-filtering versus post-filtering from selectivity.
3. Make tenant isolation a mandatory pre-filter, never optional.
4. Apply the same filters to both the lexical and dense arms.
5. Test that filters never leak across a boundary.
6. Explain why the payload schema is designed at ingest time.

## Prerequisites

- RAG System 01 (chunking) for the chunks and their metadata.
- A basic model of a vector store with payload filtering.

---

## 1. Filter Types

### Predicates over payloads

A filter is a predicate over a chunk's payload metadata. The common shapes:

- **Equality:** `language == "ar"`.
- **Membership:** `book_id in ["b1", "b2"]`.
- **Range:** `page >= 100`.
- **Version:** `source_version == "v2"`.
- **Date:** `published_after > "2020-01-01"`.

### The payload schema is an ingest decision

A filterable attribute must be present in the payload, set when the chunk is written. If you
need to filter by a field that was never stored, the fix is a re-ingest, not a query change.
This is why the payload schema is designed alongside chunking (RAG System 01).

```python
# The filter contract carried on every chunk
{"language": "ar", "book_id": "b1", "source_version": "v2", "page": 7}
```

### Filters carry provenance

Version and source fields are also what make staleness detectable (RAG System 07) and
provenance validation possible (RAG System 08). The payload is doing more than filtering.

## 2. Pre-filter Versus Post-filter

### The two plans

- **Pre-filtering** applies the predicates before the similarity search, so only eligible
  chunks are scored.
- **Post-filtering** applies them after ranking, over the returned candidates.

### Selectivity decides

Pre-filtering is correct when the filter is highly selective (a tenant with a tiny fraction
of the corpus), because scoring ineligible chunks wastes work. Post-filtering is simpler but
can return fewer than k results, because it removes candidates after they have consumed slots,
and it wastes vector work on data that will be discarded.

### The failure of post-filtering

If a tenant owns 0.1% of the data and you post-filter the top 50, you may keep almost
nothing. The k guarantee breaks: the user asked for five passages and got one. Pre-filtering
with index support avoids this, which is why vector stores expose payload filtering.

### The rule

Highly selective filter: pre-filter. Barely selective filter: either works, but pre-filtering
is still safer for the k guarantee. When in doubt, pre-filter.

## 3. Tenant Isolation Is Correctness

### The rule

For multi-tenant data, the tenant filter is a mandatory pre-filter, enforced below the API
layer, never optional and never a query-time afterthought. Every query carries the tenant,
and every candidate is filtered by it before ranking.

### Why it is not negotiable

A leak across tenants is a security incident, not a retrieval miss. The consequences are
legal and reputational, not a slightly worse answer. This is why the filter is enforced at
the retrieval boundary rather than trusted to caller discipline.

### The enforcement point

Enforce it in the retrieval function, not in each caller:

```python
def search(chunks, query, tenant, k=3):
    """Pre-filtered search: tenant filter applied before ranking."""
    eligible = [c for c in chunks if c["tenant"] == tenant]
    ...
```

A caller cannot forget the filter because the caller does not apply it.

## 4. Filters in Hybrid Search

### The same filter on both arms

Both retrieval arms must honor the same filters. The dense arm filters by payload before the
similarity search; the lexical arm filters by the same predicate before scoring. If one arm
ignores the filter, the fused result leaks, because the fusion (RAG System 03, Arabic NLP 05)
mixes both arms.

### Apply once, inherit twice

Apply the filter once, at the boundary, and pass the eligible set to both arms. Duplicating
the predicate in two places invites drift, where one arm's filter is updated and the other is
not.

### The fused result is only as safe as the weaker arm

A dense arm that filters and a lexical arm that does not still leaks, because the lexical
arm's unfiltered candidates reach the fusion. The safety of the pipeline is the minimum of
its parts.

## 5. Testing Filters

### The no-leak test

The test asserts that no result crosses the boundary:

```python
def test_tenant_isolation():
    results = search(chunks, "صلاة", tenant="t1")
    assert all(r["tenant"] == "t1" for r in results)  # no leak
```

### Assert the absence, not just the presence

A weak test checks that the right data is returned. A strong test checks that the wrong data
is not returned: `assert all(r["tenant"] == "t1" ...)` and, where a known secret exists in
another tenant, `assert all(secret not in r["text"] for r in results)`. The second assertion
is what catches a filter that is silently dropped.

### In CI

The no-leak test is a permanent gate (AI Evaluation 06). A change that removes or bypasses
the filter fails the build, because the failure mode is a security incident.

## 6. Designing the Payload

### At ingest, not at query

Every attribute you will ever filter by must be written at ingest. Plan the payload when you
plan the chunk: language, source, version, page, and tenant are the usual set. Adding one
later means re-ingesting the corpus.

### Cardinality and index support

High-cardinality fields (per-tenant, per-document) are the ones that most need index support
for pre-filtering. The vector store's payload-index configuration is part of the retrieval
design, alongside the distance metric (Applied ML 01).

### Filters are part of the retrieval ADR

The filter set, the pre/post choice, and the isolation enforcement point belong in the
retrieval ADR so a change is deliberate and reviewable.

## Real-World Application

- Filtering Athar retrieval by `book_id` so a query's answer cites the right work and pulls
  only vetted sources.
- Pre-filtering by `tenant` in a multi-tenant DevMate deployment so no customer sees another's
  code.
- Filtering by `language == "ar"` so a mixed corpus does not return English passages for an
  Arabic query.
- Filtering by `source_version` so a re-ingested book's old passages never surface.

## Common Mistakes

1. **Post-filtering at low selectivity.** Wasted work and a broken k guarantee.
2. **Optional tenant filters.** The failure mode is a data leak.
3. **Filters on one arm but not the other.** The hybrid result leaks.
4. **Designing payloads at query time.** Missing attributes mean a re-ingest.
5. **Enforcing the filter in each caller.** A caller will forget.
6. **Testing only presence, not absence.** A dropped filter passes the weak test.

## Key Takeaways

1. Filters are correctness tools first; the payload schema is an ingest-time design.
2. Selectivity decides pre- versus post-filtering; pre-filtering is safer for the k guarantee.
3. Tenant isolation is a mandatory pre-filter enforced below the API layer.
4. Both hybrid arms honor the same filters; safety is the weaker arm's safety.
5. Test the absence of forbidden data, not only the presence of expected data, and gate it in
   CI.

## Self-Check Questions

1. Why can post-filtering return fewer than k results, and when does that matter?
2. Why is tenant isolation enforced in the retrieval function rather than by callers?
3. Give the filter rule for a highly selective attribute.
4. Why does filtering only one hybrid arm still leak?
5. Why is a "wrong data absent" assertion stronger than a "right data present" assertion?

## Further Reading / Connections

- RAG System 01 (chunking) — the payload the filters operate on.
- RAG System 03 (reranking) and Arabic NLP 05 (hybrid search) — the arms that inherit the
  filters.
- RAG System 08 (context security) — tenant isolation and provenance validation.
- AI Evaluation 05 (adversarial evaluation) — the adversarial set that includes leak attempts.
