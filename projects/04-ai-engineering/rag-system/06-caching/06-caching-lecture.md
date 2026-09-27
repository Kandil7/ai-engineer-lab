# RAG System 06: Caching

## 🎯 Topic Overview

Caching is where RAG cost and latency are won or lost. Exact-match caching
is trivial; semantic caching — returning a cached answer for a similar
query — is where the real savings live. This lecture covers cache keys,
semantic caching, invalidation, and the discipline of never caching a bad
answer.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Cache exact-match queries by a normalized query key
2. Implement semantic caching with embedding similarity
3. Invalidate caches when the corpus or prompt version changes
4. Never cache malformed or abstained answers
5. Measure the cache hit rate as a cost lever

---

## 1. Exact-Match Caching

The simplest cache keys on the normalized query: the same question asked
twice returns the cached answer. The key is the normalized query plus the
prompt version and corpus version — a cache entry is only valid for the
exact configuration that produced it.

```python
cache_key = (normalize(query), prompt_version, corpus_version)
```

## 2. Semantic Caching

Semantic caching returns a cached answer when a new query is similar enough
to a cached one — same intent, different wording. The query is embedded and
compared to cached query embeddings; above a similarity threshold, the
cached answer is returned. The threshold is the precision-recall dial: too
low returns wrong answers, too high misses savings.

## 3. Invalidation

A cache entry is valid only while its inputs are unchanged. When the corpus
changes (new source version) or the prompt changes (new prompt version),
the cache must invalidate. The cache key carries both versions, so a change
naturally misses. Never serve a stale answer from a changed corpus.

## 4. Never Cache Bad Answers

Never cache an abstained answer or a malformed one. Caching a refusal
locks in a refusal; caching a malformed output amplifies the error. The
rule: validate the answer before caching it — schema-valid, grounded, not
abstained.

## 5. Measuring the Hit Rate

The hit rate is a cost lever: a 30% hit rate cuts a third of the LLM spend.
The dashboard tracks hit rate over time; a dropping rate means the cache is
rotting (queries diverging, threshold too strict, invalidation too
aggressive). The roadmap's stage budgets treat cache hit rate as a first-class
metric.

## Common Mistakes

- Caching without the prompt/corpus version in the key (stale answers).
- Semantic threshold too low (wrong answers served as cached).
- Caching abstained or malformed answers (amplified errors).
- No hit-rate measurement (the cost lever is invisible).

## Key Takeaways

1. Cache keys carry query + prompt version + corpus version.
2. Semantic caching needs a tuned similarity threshold.
3. Invalidate on corpus or prompt change.
4. Never cache bad answers; measure the hit rate.