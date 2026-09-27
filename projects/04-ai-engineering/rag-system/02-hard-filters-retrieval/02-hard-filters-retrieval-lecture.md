# RAG System 02: Hard Filters and Retrieval

## 🎯 Topic Overview

Hard filters constrain retrieval before ranking: tenant, language, source
version, date range. They are correctness tools first — a filter that lets
the wrong data through is a security bug, not a performance issue. This
lecture covers filter types, pre- vs post-filtering, and combining filters
with hybrid retrieval.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write equality, membership, range, and date filters
2. Choose pre-filtering vs post-filtering from selectivity
3. Make tenant isolation a mandatory pre-filter, never optional
4. Apply the same filters to both hybrid arms
5. Test that filters never leak across boundaries

---

## 1. Filter Types

Filters are predicates over chunk payloads: equality (`language == "ar"`),
membership (`book_id in [...]`), range (`page >= 100`), date. The payload
schema is designed at ingest time — a filterable attribute missing from the
payload is a re-ingest, not a query fix.

```python
# The filter contract
{"language": "ar", "book_id": "b1", "source_version": "v2"}
```

## 2. Pre-filter vs Post-filter

Pre-filtering applies predicates before similarity search; post-filtering
applies them after. Pre-filtering is correct at low selectivity (a tenant
with 0.1% of data) and needs index support. Post-filtering is simple but
wastes vector work and can return fewer than k results. Selectivity decides
the plan.

## 3. Tenant Isolation Is Correctness

For multi-tenant data, the tenant filter is a mandatory pre-filter enforced
below the API layer — never optional, never a query-time afterthought. A
leak across tenants is a security incident, not a retrieval miss. The OWASP
RAG guidance treats isolation as an ingestion-and-retrieval control, not an
audit finding.

## 4. Filters in Hybrid Search

Both retrieval arms must honor the same filters. The dense arm filters by
payload before similarity; the lexical arm filters by the same predicate
before scoring. If one arm ignores the filter, the fused result leaks. The
filter is applied once, at the boundary, and both arms inherit it.

## 5. Testing Filters

```python
def test_tenant_isolation():
    results = search("سؤال", tenant="t1")
    assert all(r["tenant"] == "t1" for r in results)  # no leak
```

The test asserts no result crosses the boundary. This is the roadmap's
"no leakage between different permissions" exit test, applied at the
retrieval layer.

## Common Mistakes

- Post-filtering at low selectivity (wasted work, broken k guarantee).
- Optional tenant filters (leaks).
- Filters applied to one arm but not the other (hybrid leak).
- Payloads designed at query time instead of ingest time.

## Key Takeaways

1. Filters are correctness tools first.
2. Selectivity decides pre- vs post-filtering.
3. Tenant isolation is a mandatory pre-filter.
4. Both hybrid arms honor the same filters.