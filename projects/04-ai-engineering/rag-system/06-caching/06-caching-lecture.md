# RAG System 06: Caching

## Topic Overview

Caching is where RAG cost and latency are won or lost. Exact-match caching is trivial and
saves little; semantic caching, which returns a cached answer for a semantically similar
query, is where the real savings live but also where the real risk lives, because a
too-aggressive threshold serves wrong answers. Caching is a cost lever and a correctness hazard
at the same time.

This lecture covers the cache key (query plus prompt version plus corpus version), semantic
caching with a similarity threshold, invalidation when the corpus or prompt changes, the rule
that a bad answer is never cached, and the hit rate as a first-class metric. The discipline
throughout is that a cache is only valid while its inputs are unchanged, which is why the key
carries the versions.

The failure mode to internalize is the stale answer: a correct answer from yesterday's corpus
served today, faithful to evidence that no longer exists. The version in the key is what
prevents it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Cache exact-match queries under a normalized query key plus versions.
2. Implement semantic caching with an embedding-similarity threshold.
3. Invalidate the cache when the corpus or prompt version changes.
4. Never cache abstained or malformed answers.
5. Measure the hit rate as a cost lever.
6. Explain why the version is part of the key.

## Prerequisites

- RAG System 04 and 05 for the answer shape (grounded, with citations, or abstained).
- Arabic NLP 04 (embeddings) for the similarity used in semantic caching.

---

## 1. Exact-Match Caching

### The key

The simplest cache keys on the normalized query. The same question asked twice returns the
cached answer. The key is the normalized query plus the prompt version and the corpus version:

```python
cache_key = (normalize(query), prompt_version, corpus_version)
```

### Why versions in the key

A cached answer is only valid for the exact configuration that produced it. If the prompt
changed, the answer would differ; if the corpus changed, the evidence would differ. Putting the
versions in the key makes a change naturally miss, so a stale answer cannot be served.

### The limitation

Exact-match caching only helps when queries repeat verbatim, which real users rarely do. Its
savings are modest; the real lever is semantic caching.

## 2. Semantic Caching

### The mechanism

Semantic caching returns a cached answer when a new query is similar enough to a cached one:
same intent, different wording. The query is embedded and compared to cached query embeddings;
above a similarity threshold, the cached answer is returned.

### The threshold is the dial

The similarity threshold is a precision-recall trade. Too low, and a different question gets a
cached answer for a question that merely resembles it, serving a wrong answer confidently. Too
high, and almost nothing hits, and the cache saves little. The threshold is tuned on the golden
set: measure how often similar-but-different queries collide.

### The risk

Semantic caching is the one place in the pipeline where a wrong answer can be served with high
confidence and no retrieval. That is why the threshold must be conservative and measured, and
why semantic caching is usually paired with a check that the cached answer still passes the
citation and grounding guards.

## 3. Invalidation

### Version-based invalidation

A cache entry is valid only while its inputs are unchanged. Because the key carries the prompt
and corpus versions, a change to either makes the old entries unreachable without an explicit
purge:

```python
assert cache.get(query, "prompt_v1", "corpus_v2") is None  # corpus change invalidates
```

### Why this is the safe design

An explicit purge can be forgotten; a version in the key cannot. Version-based invalidation
makes correctness the default and staleness the exception, which is the right bias for a
knowledge system.

### The embedding-model version

The embedding model that produced the cached query vector is another version that must be in
the key or the invalidation logic, because a model change alters the similarity space and makes
old comparisons invalid.

## 4. Never Cache Bad Answers

### The rule

Never cache an abstained answer or a malformed one:

```python
def put(self, query, prompt_version, corpus_version, answer):
    # Never cache abstained or malformed answers.
    if answer.get("abstained") or not answer.get("answer"):
        return
    ...
```

### Why

Caching a refusal locks in the refusal, so a fix to the retrieval that would now answer the
question never takes effect for that query. Caching a malformed output amplifies the error
across every similar query. The cache must hold only validated, grounded answers.

### Validate before caching

The validation is the same as everywhere else: schema-valid, grounded, citations resolve, not
abstained. Only then is the answer a candidate for caching.

## 5. Measuring the Hit Rate

### The cost lever

The hit rate is a direct cost lever: a 30% hit rate cuts roughly a third of the LLM spend and a
large fraction of the latency. It is a first-class metric, tracked over time.

### What a dropping rate means

A falling hit rate means the cache is rotting: queries are diverging from the cached set, the
threshold is too strict, or invalidation is too aggressive. Each has a different fix, and the
trend is what surfaces it.

### The interaction with cost tracking

The hit rate feeds the cost model: cost per useful answer (Model Serving 01) depends on how
often the cache serves the answer for free. The two metrics are read together.

## 6. Where Caching Sits

### The layers

Caching can sit at several layers: the exact query, the semantic query, the retrieval result,
and the LLM response. Each has a different invalidation story and hit rate. Start with the
answer cache (the biggest cost) and the retrieval cache, and measure each.

### The correctness first rule

Every layer follows the same rule: the key carries the versions that could change the result,
and a bad result is never cached. A cache is an optimization only if it cannot serve a stale or
wrong answer.

### The budget interaction

Caching is also a latency lever, which matters for the stage budgets. A semantic cache hit can
turn a multi-second RAG pipeline into a sub-second response, which changes the deployment's
capacity profile (Model Serving 03).

## Real-World Application

- Caching Athar answers under (normalized query, prompt version, corpus version) so a
  re-ingested book invalidates the affected entries.
- Tuning the semantic threshold against the golden set so similar-but-different fiqh questions
  do not collide.
- Refusing to cache an abstention so a later retrieval fix can answer the query.
- Tracking the hit rate on a dashboard as a cost and latency lever.

## Common Mistakes

1. **Caching without the prompt or corpus version in the key.** Stale answers served.
2. **A semantic threshold that is too low.** Wrong answers served confidently.
3. **Caching abstained or malformed answers.** Errors locked in and amplified.
4. **No hit-rate measurement.** The cost lever is invisible.
5. **A manual purge instead of version keys.** A forgotten purge serves stale answers.
6. **Forgetting the embedding-model version.** The similarity space changed but the key did
   not.

## Key Takeaways

1. Cache keys carry the normalized query plus the prompt and corpus versions.
2. Semantic caching needs a conservatively tuned similarity threshold; the threshold is a
   correctness dial, not just a cost dial.
3. Version-based invalidation makes staleness the exception rather than the default.
4. Never cache abstained or malformed answers; validate before caching.
5. Measure the hit rate as a first-class cost and latency metric.

## Self-Check Questions

1. Why are the prompt and corpus versions part of the cache key?
2. What does the semantic similarity threshold trade, and how is it tuned?
3. Why must an abstained answer never be cached?
4. What does a falling hit rate indicate, and what are the possible fixes?
5. Why is version-based invalidation safer than an explicit purge?

## Further Reading / Connections

- RAG System 04 and 05 — the answer shape that determines cache eligibility.
- RAG System 07 (context failure modes) — staleness as a failure mode.
- Model Serving 01 and 03 — cost per useful answer and latency budgets.
- `projects/04-ai-engineering/devmate/src/devmate/cache/semantic_cache.py` — a working semantic
  cache.
