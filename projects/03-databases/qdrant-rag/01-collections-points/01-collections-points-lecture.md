# Qdrant 01: Collections and Points

## 🎯 Topic Overview

Qdrant stores vectors in collections of points. A point is a vector plus
its payload — the metadata that makes retrieval filterable. This lecture
covers the collection, the point, and the payload schema.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Create a collection with the right vector size
2. Insert points with vectors and payloads
3. Design the payload schema
4. Understand the point id
5. Update and delete points

---

## 1. The Collection

A collection is a named set of points sharing a vector size and distance
metric. The vector size is fixed at creation — every point in the
collection has the same dimensionality. The distance metric (cosine,
dot, euclidean) decides how similarity is measured. The roadmap's exit
test: "the collection is created with the right vector size."

```python
client.create_collection(
    collection_name="athar",
    vectors_config={"size": 768, "distance": "Cosine"},
)
```

## 2. The Point

A point is a vector plus a payload. The vector is the embedding; the
payload is the metadata: source, page, book, language. The point id is
the stable identity — it is what citations reference. The roadmap's exit
test: "points carry the payload."

## 3. The Payload Schema

The payload is the filterable metadata. It is designed before ingestion:
which fields are filters (book, page, language), which are display
(source text), which are provenance (version). A well-designed payload
makes filtering cheap and correct. The roadmap's exit test: "the payload
schema is designed before ingestion."

## 4. The Point Id

The point id is the stable identity of the chunk. It is the evidence id
the answer cites. The id is deterministic — derived from the source, not
random — so re-ingestion updates the same point instead of duplicating it.

## 5. Updates and Deletes

Points are updated and deleted by id. Re-ingesting a corrected source
updates the existing points. Deleting a source deletes its points. The
operations are idempotent: the same id, the same result.

## Common Mistakes

- Wrong vector size at creation (must match the embedding model).
- Random point ids (re-ingestion duplicates).
- Payload designed after ingestion.
- No provenance in the payload.
- Ignoring the distance metric.

## Key Takeaways

1. A collection fixes the vector size and distance metric.
2. A point is a vector plus a payload.
3. The payload schema is designed before ingestion.
4. The point id is deterministic and is the citation target.
5. Updates and deletes are idempotent by id.