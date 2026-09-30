# Qdrant 02: Vector Search

## Topic Overview

Vector search finds the points closest to a query vector. The query is embedded, the collection is
searched by similarity, and the top-k points are returned with scores. It is the dense arm of retrieval,
and its correctness depends on a single precondition: the query must be embedded with the same model,
and therefore the same dimensionality, as the collection.

This lecture covers the query embedding, the search call, the score, the limit and threshold, and the
silent failure that happens when the query embedding does not match the collection.

The most dangerous property of vector search is that an embedding mismatch fails silently: it returns
results, they are just wrong. That is why the model-and-size match is a contract that must be enforced,
not assumed.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Embed a query with the same model as the collection.
2. Search the collection for the top-k points.
3. Read the similarity score.
4. Use the limit and score threshold to control the result set.
5. Explain why an embedding mismatch fails silently.
6. Explain how the limit and threshold relate to the context budget.

## Prerequisites

- Qdrant 01 (collections and points) for the collection this searches.
- Applied ML 01 (vectors and similarity) for the score.

---

## 1. The Query Embedding

### The match

The query is embedded with the same model that embedded the collection:

```python
query_vector = embed(query)  # same model as the collection
```

### The contract

The model and its dimensionality are a contract between the embedder and the collection. A 768-
dimension query into a 768-dimension collection is valid; a different model's output is not.

### The exit test

The roadmap's exit test is that the query is embedded with the same model, which is the precondition
for the scores to mean anything.

## 2. The Search

### The call

Search returns the top-k points by similarity, each with a score:

```python
results = client.search(
    collection_name="athar",
    query_vector=query_vector,
    limit=10,
)
```

### What it does

The store compares the query vector to the stored vectors and returns the nearest ones. For a cosine
collection (Qdrant pre-normalizes), this is a dot-product comparison and the index prunes the search
space (Arabic NLP 06).

### The exit test

The roadmap's exit test is that the top-k points are returned with scores, which is the basic retrieval
operation.

## 3. The Score

### What it measures

The score measures similarity between the query and each point. For cosine, higher is more similar:

```python
assert results[0][0] == "b3:p12:0", "most similar first"
```

### What it means

A high score means strong similarity; a low score means weak similarity, which is not the same as a
wrong answer. The score is the raw material for the threshold and for reranking (RAG System 03).

### The normalization

Cosine scores are bounded, which makes a threshold meaningful. An unbounded metric makes absolute
thresholds harder to set, which is another reason cosine is the default.

## 4. The Limit and Threshold

### The limit

The limit caps how many points are returned:

```python
assert len(results) == 2, "limit caps the results"
```

The limit should match the number of passages that will reach the generator (RAG System 04), so it
reflects what the model can use.

### The threshold

The score threshold drops points below a similarity floor:

```python
results = search(points, query, limit=10, threshold=0.995)
assert len(results) == 1, "only the near-identical point passes"
```

A threshold controls precision: it drops weak matches that would otherwise fill the context budget.

### The budget link

The limit and threshold together control the context budget (RAG System 09). A generous limit with no
threshold fills the window with weak matches; a tight limit with a high threshold risks missing
relevant passages.

### The exit test

The roadmap's exit test is that the limit and threshold are set deliberately, which is what controls the
context the pipeline receives.

## 5. The Silent Failure

### The mismatch

The query embedding must match the collection's model and size. A mismatch is a silent failure: search
returns results without error, but the results are meaningless:

```python
try:
    cosine(query, [1.0, 0.0])  # size mismatch
    assert False, "size mismatch must be rejected"
except AssertionError:
    pass
```

### Why silent

The store does not know which model produced the query; it only knows the size, and even a size match
with a different model produces wrong similarities. The mismatch is invisible unless the pipeline
enforces the model identity.

### The prevention

Record the embedding model version with the collection (Qdrant 01) and check it at query time. The check
is the only thing standing between a mismatch and a silently broken retrieval.

### The exit test

The roadmap's exit test is that the embedding match is enforced, which is what prevents the silent
failure.

## 6. The Exercise

### What it models

The exercise models search with a limit and threshold, the most-similar-first ordering, and the rejected
size mismatch.

### The assertions

```python
results = search(points, query, limit=2, threshold=0.5)
assert results[0][0] == "b3:p12:0", "most similar first"
results = search(points, query, limit=10, threshold=0.995)
assert len(results) == 1, "only the near-identical point passes"
```

The threshold assertion shows precision control; the size-mismatch assertion shows the contract.

## Real-World Application

- Embedding an Athar query with the collection's model and searching the top-10.
- Setting a score threshold so weak matches do not fill the context.
- Recording the embedding model version so a mismatch is caught, not silent.
- Setting the limit to the number of passages the generator can use.

## Common Mistakes

1. **Query embedded with a different model.** Silent wrong results.
2. **No limit.** The whole collection returns.
3. **Ignoring the score.** The threshold has nothing to act on.
4. **No score threshold.** Weak matches flood the context.
5. **Forgetting the model-and-size match.** The silent failure.
6. **A limit unrelated to the context window.** Recall@k becomes academic.

## Key Takeaways

1. The query is embedded with the same model as the collection; the match is a contract.
2. Search returns the top-k points with scores; the store prunes the space via its index.
3. The score measures similarity; for cosine, higher is more similar and bounded.
4. The limit and threshold control the context budget and precision.
5. An embedding mismatch fails silently, so the model identity is enforced, not assumed.

## Self-Check Questions

1. Why must the query use the same model as the collection?
2. What does the score measure, and why does a bounded score help set a threshold?
3. How do the limit and threshold relate to the context budget?
4. Why does an embedding mismatch fail silently, and how is it prevented?
5. Why should the limit match the context window?

## Further Reading / Connections

- Qdrant 01 (collections and points), 03 (hybrid search), and 04 (metadata filtering).
- Arabic NLP 06 (ANN search) — the index that prunes the search.
- RAG System 03 (reranking) and 04 (context construction) — the consumers of the search result.
- `docs/cheat-sheets/qdrant.md` — the command reference.
