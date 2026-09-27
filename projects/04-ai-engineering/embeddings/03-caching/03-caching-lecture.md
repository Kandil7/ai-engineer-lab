# Embeddings 03: Caching

## 🎯 Topic Overview

Embeddings are expensive to generate. Caching means the same text is never
embedded twice. This lecture covers the cache key, the layers, and the
cache-aside flow.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Design the cache key from the content hash
2. Layer the cache by speed and persistence
3. Run the cache-aside flow
4. Invalidate on model or content change
5. Measure the hit rate

---

## 1. The Cache Key

The cache key is the content hash plus the model: `embedding:{model}:{hash}`.
The model is in the key because a different model produces a different
vector. The hash is of the normalized text — the same text, the same key.
The roadmap's exit test: "the cache key carries the model and the hash."

```python
key = f"embedding:{model}:{sha256(normalize(text))}"
```

## 2. The Layers

Caching layers by speed and persistence. L1 is process memory — fastest,
lost on restart. L2 is Redis — fast, survives restarts, TTL-bounded. L3 is
the vector store itself — the stored vector is the permanent cache. The
roadmap's exit test: "caching is layered."

## 3. The Cache-Aside Flow

Cache-aside: hash the text, check the cache, return on a hit, embed and
store on a miss. The flow is the same as any cache-aside. The roadmap's
exit test: "the cache-aside flow is used."

## 4. Invalidation

A cache entry is valid only for its model and content. A model change
invalidates every entry — the key carries the model, so a change naturally
misses. A content change changes the hash, so the entry misses. The
roadmap's exit test: "the cache invalidates on change."

## 5. The Hit Rate

The hit rate is the cost lever: a high hit rate means few API calls. The
rate is tracked per model and per corpus. A dropping rate signals a
changing corpus or a broken key.

## Common Mistakes

- A key without the model (wrong vectors served).
- No cache layers (all hits hit the API).
- Hashing unnormalized text (same text, different keys).
- No hit-rate tracking.
- Caching without invalidation.

## Key Takeaways

1. The key carries the model and the content hash.
2. Layers: memory, Redis, the vector store.
3. Cache-aside: hit returns, miss embeds and stores.
4. The key invalidates on model or content change.
5. The hit rate is the cost lever.