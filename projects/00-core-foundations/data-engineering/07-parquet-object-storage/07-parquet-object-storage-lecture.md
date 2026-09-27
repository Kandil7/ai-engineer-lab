# Data Engineering 07: Parquet and Object Storage

## 🎯 Topic Overview

Passages scale beyond JSONL files. Parquet gives columnar, compressed,
schema-enforced storage; object storage (S3, GCS, MinIO) gives durable,
cheap, versioned files. Together they are the production home for a corpus
like Athar's. This lecture covers Parquet's design, object-storage
principles, and the partition layout that makes retrieval efficient.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain Parquet's columnar design and why it beats JSONL at scale
2. Choose Parquet vs JSONL by workload (analytics vs streaming append)
3. Apply object-storage principles: immutability, versioning, cheap reads
4. Design a partition layout (book_id/version) for efficient scans
5. Keep provenance fields in the schema so Parquet rows stay traceable

---

## 1. Why Parquet

JSONL stores rows as text; Parquet stores columns as compressed binary.
Reading one column of a million-row Parquet file reads only that column's
bytes. Compression is better (column values repeat), and the schema is
enforced at write time. For analytics over a large corpus — "how many
passages per book?", "which pages changed in v2?" — Parquet is an order of
magnitude faster and smaller than JSONL.

```python
# JSONL:  row-oriented text, schema implicit
# Parquet: column-oriented binary, schema enforced, compressed
```

## 2. Parquet vs JSONL

JSONL wins for streaming append and human inspection; Parquet wins for
analytics, storage, and schema enforcement. The pragmatic pattern: JSONL for
the pipeline's raw output and debugging, Parquet for the queryable corpus.
The roadmap's stage-5 pipeline can emit both — JSONL for inspection, Parquet
for the indexer.

## 3. Object Storage Principles

Object storage treats files as immutable objects addressed by key. Three
principles matter: **immutability** (write once, never edit — a new version
is a new object), **versioning** (the store keeps object history, enabling
rollback), and **cheap reads** (objects are read whole; partition so you
read only what you need). Object storage is the durable home for both the
raw corpus and the Parquet snapshots.

## 4. Partition Layout

```text
corpus/
  book_id=b1/
    source_version=v1/
      passages.parquet
    source_version=v2/
      passages.parquet
```

Partitioning by book_id then source_version means a query for one book's
current version reads exactly one file. The partition keys mirror the
provenance fields — the layout is the storage-level expression of
traceability.

## 5. Provenance in the Schema

The Parquet schema carries the same provenance fields as the JSONL rows:
book_id, page, source_version, path, original, searchable. A Parquet row is
as traceable as a JSONL row. Never drop provenance when moving to Parquet —
the storage format changes, the contract does not.

## Common Mistakes

- Using JSONL for analytics at scale (slow, uncompressed, schema-implicit).
- Editing objects in place (violates immutability; version instead).
- Partitioning by high-cardinality keys (too many tiny files).
- Dropping provenance fields in the Parquet schema.

## Key Takeaways

1. Parquet: columnar, compressed, schema-enforced.
2. JSONL for pipeline output, Parquet for the queryable corpus.
3. Object storage: immutable, versioned, partitioned.
4. Provenance survives the format change.