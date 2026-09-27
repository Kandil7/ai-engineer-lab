# Qdrant 01: Collections and Points — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Collection | A named set of points with a fixed vector size | athar |
| Point | A vector plus its payload | embedding + metadata |
| Payload | The filterable metadata | book, page, language |
| Vector size | The fixed dimensionality | 768 |
| Distance metric | How similarity is measured | Cosine |
| Point id | The stable identity, the citation target | b3:p12:0 |
| Payload schema | The designed metadata fields | designed before ingestion |

---

## Alphabetical Glossary

### Collection

**Definition:** A named set of points sharing a vector size and distance
metric. The vector size is fixed at creation.

**Example:**
```python
client.create_collection("athar", vectors_config={"size": 768, "distance": "Cosine"})
```

**Related concepts:** Point, Vector size

---

### Distance metric

**Definition:** How similarity is measured between vectors: cosine, dot, or
euclidean. Chosen at collection creation.

**Example:**
```python
# Cosine for normalized embeddings
```

**Related concepts:** Collection

---

### Payload

**Definition:** The filterable metadata attached to a point: source, page,
book, language. What makes retrieval filterable.

**Example:**
```python
{"book": "b3", "page": 12, "language": "ar"}
```

**Related concepts:** Point, Payload schema

---

### Payload schema

**Definition:** The designed metadata fields, decided before ingestion:
which are filters, which are display, which are provenance.

**Example:**
```python
# filters: book, page, language; display: source_text; provenance: version
```

**Related concepts:** Payload

---

### Point

**Definition:** A vector plus its payload. The vector is the embedding; the
payload is the metadata.

**Example:**
```python
client.upsert("athar", points=[{"id": "b3:p12:0", "vector": [...], "payload": {...}}])
```

**Related concepts:** Collection, Payload

---

### Point id

**Definition:** The stable identity of the chunk, deterministic from the
source. The evidence id the answer cites.

**Example:**
```python
# "b3:p12:0" = book b3, page 12, chunk 0
```

**Related concepts:** Point

---

### Vector size

**Definition:** The fixed dimensionality of every vector in the collection.
Must match the embedding model.

**Example:**
```python
# 768 for a multilingual embedding model
```

**Related concepts:** Collection

---

## Related Concepts

- **Vector search**: the collection is searched (topic 02)
- **Hybrid search**: payload filters combine with vectors (topic 03)
- **Metadata filtering**: the payload schema drives filters (topic 04)

## Key Takeaways

1. A collection fixes the vector size and distance metric.
2. A point is a vector plus a payload.
3. The payload schema is designed before ingestion.
4. The point id is deterministic and is the citation target.
5. Updates and deletes are idempotent by id.