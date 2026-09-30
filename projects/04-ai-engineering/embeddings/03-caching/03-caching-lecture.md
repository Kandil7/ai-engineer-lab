# Embeddings 03: Caching

## Topic Overview

Embeddings are expensive to generate: they cost API calls or GPU time, and re-embedding a large
corpus is slow. Caching means the same text is never embedded twice. It is one of the highest-
leverage optimizations in the pipeline, because ingestion, re-indexing, and query embedding all
touch the same texts repeatedly.

This lecture covers the cache key (content hash plus model), the cache layers by speed and
persistence, the cache-aside flow, invalidation when the model or content changes, and the hit
rate as a metric. The key design decision is that the model belongs in the key, because a
different model produces a different vector and must not be served from another model's cache.

The failure mode is subtle: a cache without the model in the key serves vectors from the wrong
space, and the retrieval degrades silently. The key carries every version that could change the
result.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design a cache key from the content hash and the model.
2. Layer the cache by speed and persistence.
3. Implement the cache-aside flow.
4. Invalidate on model or content change.
5. Measure the hit rate.
6. Explain why the model belongs in the key.

## Prerequisites

- Embeddings 01 (model selection) for the model-consistency rule.
- Embeddings 02 (batch processing) for the pipeline that generates the embeddings.

---

## 1. The Cache Key

### The content hash plus the model

The key is the content hash plus the model identifier:

```python
def cache_key(model: str, text: str) -> str:
    """The key carries the model and a content hash."""
    return f"embedding:{model}:{hash(text)}"
```

The hash is of the normalized text (Arabic NLP 02), so the same logical text maps to the same
key. The model is in the key because a different model produces a different vector.

### Why the model is in the key

If the key omitted the model, a cache built with model A would serve vectors to queries from
model B, and the two live in different spaces. The retrieval would return arbitrary results
while looking functional. Putting the model in the key makes a model change naturally miss,
which is exactly the right behavior.

### Why the hash is of normalized text

Hashing unnormalized text means the same logical text with a diacritic difference produces two
keys and two embeddings, wasting storage and splitting the cache. Normalize before hashing.

## 2. The Layers

### L1: process memory

The fastest layer, lost on restart. Good for the hot set of recently used texts. Bounded in
size, evicted by recency.

### L2: Redis (or similar)

Fast and survives restarts, TTL-bounded. Shared across processes, so multiple workers share the
cache. This is where most of the savings live for a corpus-scale ingestion.

### L3: the vector store itself

The stored vector is the permanent cache: if a text's vector is already in the vector store, it
does not need to be embedded again. This layer is deduplicated by the chunk identity (RAG System
01).

### Why layers

Each layer trades speed for capacity and persistence. The query path checks the fastest layer
first; the ingestion path benefits from the persistent layers. Together they ensure a text is
embedded at most once across the system's life.

## 3. The Cache-Aside Flow

### The flow

Cache-aside: hash the text, check the cache, return on a hit, embed and store on a miss:

```python
vector = cache.get(key)
if vector is None:
    vector = embed(text)
    cache.put(key, vector)
```

### Why cache-aside

The application owns the logic: it decides when to embed and when to reuse. There is no hidden
coupling between the cache and the embedder, and a cache failure degrades to "embed anyway"
rather than to an error.

### The idempotency bonus

Because the key is deterministic, the flow is idempotent: running it twice yields the same
vector and no extra calls. This is what makes re-running ingestion safe (Data Engineering 03).

## 4. Invalidation

### Model change

A model change invalidates every entry, because the key carries the model. The old entries
naturally miss and are re-embedded, and the old entries can be expired by TTL.

### Content change

A content change changes the hash, so the entry misses. There is no stale vector for changed
text, because the changed text has a different key.

### Why version keys beat purges

An explicit purge can be forgotten; a version in the key cannot. Version-based invalidation
makes correctness the default, which is the right bias for a cache that feeds retrieval.

## 5. The Hit Rate

### The metric

The hit rate is the cost lever: a high hit rate means few embedding calls. Track it per model and
per corpus.

### What a dropping rate means

A falling hit rate signals a changing corpus (new texts not seen before), a broken key
(normalization changed so every key is new), or an over-aggressive invalidation. Each has a
different fix, and the trend is what surfaces it.

### The link to cost

The hit rate feeds the cost model: embedding cost per useful answer depends on how often the
cache serves the vector for free. It is read alongside the throughput (Embeddings 02).

## 6. Where Caching Sits

### Ingestion and query

Caching helps both paths: ingestion avoids re-embedding unchanged texts, and the query path
avoids re-embedding repeated queries. The same key design works for both.

### The interaction with the answer cache

The embedding cache caches vectors; the answer cache (RAG System 06) caches answers. They are
different layers with different keys, and both follow the same rule: every version that could
change the result is in the key.

## Real-World Application

- Caching Athar passage embeddings under (model, normalized-text hash) so re-running ingestion
  does not re-embed the corpus.
- Layering the cache in memory and Redis so multiple ingestion workers share the persistent
  layer.
- Invalidating on a model change so the new model's vectors replace the old ones without a
  purge.
- Tracking the hit rate to see the embedding cost drop after the first full ingestion.

## Common Mistakes

1. **A key without the model.** Wrong-space vectors served.
2. **No cache layers.** Every miss hits the API.
3. **Hashing unnormalized text.** The same text produces different keys.
4. **No hit-rate tracking.** The cost lever is invisible.
5. **Caching without invalidation.** Stale vectors after a model change.
6. **An explicit purge instead of version keys.** A forgotten purge serves stale vectors.

## Key Takeaways

1. The key carries the model and the content hash of the normalized text.
2. Layer the cache: process memory, Redis, and the vector store as the permanent layer.
3. Cache-aside: hit returns, miss embeds and stores; the flow is idempotent.
4. A model or content change naturally invalidates because the key carries the versions.
5. Measure the hit rate as the embedding-cost lever.

## Self-Check Questions

1. Why does the model belong in the cache key?
2. Why is the hash taken over normalized text?
3. Describe the three cache layers and what each trades.
4. How does a model change invalidate the cache without an explicit purge?
5. What does a dropping hit rate indicate, and what are the possible fixes?

## Further Reading / Connections

- Embeddings 01 (model selection) — the consistency rule the key enforces.
- Embeddings 04 (quality evaluation) — measuring the cached pipeline's quality.
- RAG System 06 (caching) — the answer cache, with the same version-key discipline.
- Data Engineering 03 (idempotency) — why the deterministic key makes re-runs safe.
