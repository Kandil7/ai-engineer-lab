# Qdrant 01: Collections and Points

## Topic Overview

Qdrant stores vectors in collections of points. A point is a vector plus its payload, and the payload is
the metadata that makes retrieval filterable. The collection fixes the vector size and distance metric;
the point carries the identity and the metadata. Getting these right at the start is what makes
retrieval correct and re-ingestion safe.

This lecture covers the collection, the point, the payload schema, the deterministic point id, and
updates and deletes.

The core idea is that the payload schema is designed before ingestion, not after. A filterable field
that was never stored cannot be filtered, and adding it later means re-ingesting the whole collection.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create a collection with the right vector size and distance metric.
2. Insert points with vectors and payloads.
3. Design the payload schema before ingestion.
4. Explain the deterministic point id.
5. Update and delete points idempotently.
6. Explain why the point id is the citation target.

## Prerequisites

- Arabic NLP 04 (Arabic embeddings) for the vector size the model produces.
- Applied ML 01 (vectors and similarity) for the distance metric.

---

## 1. The Collection

### What it fixes

A collection is a named set of points sharing a vector size and a distance metric. Both are fixed at
creation; every point in the collection has the same dimensionality:

```python
client.create_collection(
    collection_name="athar",
    vectors_config={"size": 768, "distance": "Cosine"},
)
```

### Why the size is fixed

The vector size must match the embedding model's output. A 768-dimension model produces 768-dimension
vectors; a collection created with a different size rejects them. The size is a contract between the
embedder and the store.

### The distance metric

The metric (cosine, dot, euclidean) decides how similarity is measured, and it must match the
retrieval design (Applied ML 01). Changing it after ingestion means re-indexing.

### The exit test

The roadmap's exit test is that the collection is created with the right vector size, which is the
precondition for every later operation.

## 2. The Point

### What it is

A point is a vector plus a payload. The vector is the embedding; the payload is the metadata: source,
page, book, language, version:

```python
col.upsert("b3:p12:0", [0.1, 0.2, 0.3], {"book": "b3", "page": 12, "language": "ar"})
```

### The vector

The vector is what makes the point retrievable by similarity. It is the embedding of the passage's
searchable text (Arabic NLP 01).

### The payload

The payload is the filterable and displayable metadata. It is what makes filtering, citation, and
provenance possible.

### The exit test

The roadmap's exit test is that points carry the payload, which is what makes the retrieval filterable
and citable.

## 3. The Payload Schema

### Design before ingestion

The payload is designed before ingestion: which fields are filters (book, page, language), which are
display (source text), which are provenance (version, path). The schema is a decision, not an
afterthought.

### The filterable fields

A field that will be filtered must be in the payload and, for pre-filtering, indexed. A filter on a
missing field either errors or silently matches nothing.

### The exit test

The roadmap's exit test is that the payload schema is designed before ingestion, because the
alternative is a re-ingest.

## 4. The Point Id

### The deterministic id

The point id is the stable identity of the chunk, and it is deterministic, derived from the source:

```python
def point_id(book: str, page: int, chunk: int) -> str:
    return f"{book}:p{page}:{chunk}"
```

### Why deterministic

A deterministic id means re-ingestion updates the same point instead of duplicating it:

```python
col.upsert(pid, vec, payload)
col.upsert(pid, vec, payload)
assert len(col.points) == 1, "same id updates, never duplicates"
```

This is the idempotency discipline (Data Engineering 03) applied to the vector store.

### The citation link

The point id is the evidence id the answer cites (RAG System 05). A stable id makes the citation
resolvable across re-ingests.

### The exit test

The roadmap's exit test is that the point id is deterministic, which is what makes re-ingestion safe
and citations stable.

## 5. Updates and Deletes

### Idempotent by id

Points are updated and deleted by id, and the operations are idempotent: the same id, the same result.
Re-ingesting a corrected source updates the existing points; deleting a source deletes its points.

### The link to provenance

Because the id is derived from the source, a re-ingest of a new source version produces the same ids
and updates in place, and the payload's `source_version` records which version the point reflects.

### The exit test

The roadmap's exit test is that updates and deletes are idempotent, which is what makes the vector
store safe to re-run against.

## 6. The Exercise

### What it models

The exercise models a collection with a fixed size, upsert by deterministic id, a rejected size
mismatch, and payload retrieval.

### The assertions

```python
col.upsert(pid, [0.1, 0.2, 0.3], {...})
col.upsert(pid, [0.1, 0.2, 0.3], {...})
assert len(col.points) == 1, "same id updates, never duplicates"
assert point["payload"]["book"] == "b3"
```

The duplicate assertion is the lesson: the deterministic id makes the re-upsert an update.

## Real-World Application

- The Athar collection with size 768 and cosine distance, matching the embedding model.
- Point ids `b3:p12:0` so a re-ingest of a corrected book updates the same points.
- A payload carrying `book`, `page`, `language`, `source_version`, and the original text for citation.
- Deleting a retracted source's points by id.

## Common Mistakes

1. **Wrong vector size at creation.** Must match the embedding model.
2. **Random point ids.** Re-ingestion duplicates.
3. **Payload designed after ingestion.** Filter fields are missing.
4. **No provenance in the payload.** Staleness is undetectable.
5. **Ignoring the distance metric.** Retrieval ranks wrongly.
6. **Upserting without the stable id.** Duplicates accumulate.

## Key Takeaways

1. A collection fixes the vector size and distance metric, which must match the design.
2. A point is a vector plus a payload; the payload carries the filterable and displayable metadata.
3. The payload schema is designed before ingestion.
4. The point id is deterministic and is the citation target, making re-ingestion safe.
5. Updates and deletes are idempotent by id.

## Self-Check Questions

1. Why must the collection's vector size match the embedding model?
2. What does the payload carry, and why is it designed before ingestion?
3. Why is a deterministic point id necessary for safe re-ingestion?
4. How does the point id relate to the citation?
5. Why are updates and deletes idempotent by id?

## Further Reading / Connections

- Qdrant 02 (vector search), 03 (hybrid search), and 04 (metadata filtering).
- Arabic NLP 04 (Arabic embeddings) — the vector size and model.
- Data Engineering 03 (idempotency) — the re-ingest discipline.
- `docs/cheat-sheets/qdrant.md` — the command reference.
