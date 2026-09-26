# Databases — 06: Metadata Filtering (Selective Retrieval)

## Topic Overview

Unfiltered similarity search scans the whole collection and returns
plausible-looking wrong answers: last year's docs, another tenant's data, a
different programming language. Metadata filtering constrains retrieval to
the eligible subset before or alongside ranking. This lecture covers filter
types, selectivity, pre- vs post-filtering, and payload indexes — the topic
the roadmap fold-in added to DevMate's retrieval step.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write equality, membership, range, and date filters on chunk payloads
2. Explain selectivity and why low-selectivity filters change the query plan
3. Choose pre-filtering vs post-filtering from the selectivity number
4. Explain payload indexes and when a filter needs one
5. Combine filters with hybrid search so both arms respect the same constraints

## Prerequisites

| Need | Where |
|---|---|
| Dense retrieval basics | [01](../01-vector-search-fundamentals/01-vector-search-fundamentals-lecture.md) |
| Hybrid arms | [05](../05-hybrid-search/05-hybrid-search-lecture.md) |
| The runnable exercise | [06-metadata-filtering.py](06-metadata-filtering.py) |

## 1. Filter Types on Payloads

Every chunk carries a payload: language, filename, chunk type, repo, date,
tenant. Filters are predicates over it — equality (`language == "python"`),
membership (`repo in [...]`), range (`date >= 2026-01-01`), and combinations.
Design payload schemas at ingest time; a filterable attribute missing from
the payload is a re-ingest, not a query fix.

```python
# The contract every vector store honors in some syntax:
eligible = [c for c in chunks if c["language"] == "python" and c["date"] >= "2026-01-01"]
candidates = vector_search(query, eligible, k=10)  # rank only the eligible
```

## 2. Selectivity Decides the Plan

Selectivity is the fraction of the collection a filter admits. High
selectivity (admits 80%) barely changes the plan; low selectivity (admits
0.1% — one tenant of a thousand) changes everything: pre-filter then search
the tiny subset, because ranking 0.1% exactly beats approximating 100%.
Post-filtering (search broadly, discard) wastes vector work and can return
fewer than k results when the filter bites after ranking.

## 3. Pre-filter vs Post-filter

Pre-filter: apply predicates first, run ANN on survivors. Correct and
efficient at low selectivity; needs index support for the filter or it
degenerates to a scan. Post-filter: ANN first, discard non-matching. Simple,
works anywhere, but k is no longer guaranteed and latency is paid on vectors
you throw away. The exercise measures both on the same workload — the
crossover point is the lesson.

## 4. Payload Indexes

A payload index makes a filter cheap the way a vector index makes similarity
cheap: the store prunes by predicate without scanning. Index the attributes
queries actually filter on (check logs, not guesses); every index costs write
throughput and RAM. Unindexed low-selectivity filters are the classic
"works in dev, dies in prod" retrieval story.

## Common Mistakes

- Filtering after ranking and wondering why k=10 returns 3 results.
- Designing payloads at query time instead of ingest time.
- Indexing every attribute instead of the filtered ones.

## DevMate Connection

The fold-in added metadata filtering to the weeks 2–3 hybrid step:
`language`, `filename`, `chunk_type`, `repo_name` payloads constrain both
retrieval arms before fusion. The chunking ADR cites which attributes proved
filter-worthy on this repo — filename and language first, everything else on
demand.

## Key Takeaways

1. Filter before ranking when selectivity is low.
2. Payloads are designed at ingest; filters are cheap only with indexes.
3. Post-filtering breaks the k guarantee — know when you accept that.
4. Both hybrid arms must respect the same constraints.
