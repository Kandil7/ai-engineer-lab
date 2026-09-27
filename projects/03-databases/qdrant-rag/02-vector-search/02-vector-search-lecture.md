# Qdrant 02: Vector Search

## 🎯 Topic Overview

Vector search finds the points closest to a query vector. The query is
embedded, the collection is searched by similarity, and the top-k points
are returned with scores. This lecture covers the search call, the score,
and the limit.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Embed the query with the same model as the collection
2. Search the collection for the top-k points
3. Read the similarity score
4. Use the limit and score threshold
5. Match the query embedding to the collection

---

## 1. The Query Embedding

The query is embedded with the same model that embedded the collection. A
mismatch — a different model, a different size — produces meaningless
similarity. The roadmap's exit test: "the query is embedded with the same
model."

```python
query_vector = embed(query)  # same model as the collection
```

## 2. The Search

Search returns the top-k points by similarity, each with a score. The
score is the distance metric's output: cosine similarity for cosine
collections. The roadmap's exit test: "the top-k points are returned with
scores."

```python
results = client.search(
    collection_name="athar",
    query_vector=query_vector,
    limit=10,
)
```

## 3. The Score

The score measures similarity between the query and each point. Higher is
more similar for cosine. The score is the raw material for the threshold
and for reranking. A low score means weak similarity, not a wrong answer.

## 4. The Limit and Threshold

The limit caps how many points are returned. The score threshold drops
points below a similarity floor. The limit and threshold together control
the context budget. The roadmap's exit test: "the limit and threshold are
set deliberately."

## 5. Matching the Embedding

The query embedding must match the collection's model and size. A
collection built with a 768-dimension model is searched with 768-dimension
query vectors. The mismatch is a silent failure — search returns garbage
without error.

## Common Mistakes

- Query embedded with a different model.
- No limit (the whole collection returns).
- Ignoring the score.
- No score threshold (weak matches flood the context).
- Forgetting the query embedding must match the collection.

## Key Takeaways

1. The query is embedded with the same model as the collection.
2. Search returns the top-k points with scores.
3. The score measures similarity.
4. The limit and threshold control the context budget.
5. An embedding mismatch fails silently.