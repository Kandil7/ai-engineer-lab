# Data Engineering 07: Parquet and Object Storage — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Parquet | Columnar, compressed, schema-enforced format | analytics corpus |
| Columnar | Column-oriented storage, reads only needed columns | fast scans |
| JSONL | Row-oriented text, schema implicit | pipeline output |
| Object storage | Immutable objects addressed by key | S3, GCS, MinIO |
| Immutability | Write once, never edit; new version = new object | versioned snapshots |
| Partitioning | Folder layout mirroring query keys | book_id/version |
| High cardinality | Many distinct partition values | too many tiny files |

---

## Alphabetical Glossary

### Columnar

**Definition:** Storing data by column rather than by row. Reading one
column reads only that column's bytes — the basis of Parquet's speed.

**Example:**
```python
# read only the 'page' column of a million-row file
```

**Related concepts:** Parquet

---

### High cardinality

**Definition:** A field with many distinct values. Partitioning by it
creates too many tiny files — a partition anti-pattern.

**Example:**
```python
# partition by passage_id (millions of values) -> thousands of tiny files
```

**Related concepts:** Partitioning

---

### Immutability

**Definition:** The object-storage principle that files are written once
and never edited; a change is a new object. Enables versioning and rollback.

**Example:**
```python
# v1 and v2 are separate objects; never overwrite v1
```

**Related concepts:** Object storage, Versioning

---

### JSONL

**Definition:** Row-oriented text storage with an implicit schema. Good for
streaming append and human inspection; slow and uncompressed for analytics.

**Example:**
```python
# pipeline raw output, debugging, small corpora
```

**Related concepts:** Parquet

---

### Object storage

**Definition:** Storage treating files as immutable objects addressed by
key. Durable, cheap, versioned — the production home for corpora.

**Example:**
```python
# s3://corpus/book_id=b1/source_version=v1/passages.parquet
```

**Related concepts:** Immutability, Partitioning

---

### Parquet

**Definition:** Columnar, compressed, schema-enforced binary format. The
analytics-grade replacement for JSONL at scale.

**Example:**
```python
# pyarrow.parquet.write_table(table, "passages.parquet")
```

**Related concepts:** Columnar, JSONL

---

### Partitioning

**Definition:** Folder layout mirroring query keys so reads touch only the
needed files. The storage-level expression of traceability.

**Example:**
```python
# book_id=b1/source_version=v1/passages.parquet
```

**Related concepts:** Object storage, High cardinality

---

## Related Concepts

- **Provenance**: partition keys mirror provenance fields (topic 06)
- **Schemas**: Parquet enforces the contract (topic 02)
- **pyarrow**: the Python Parquet library

## Key Takeaways

1. Parquet for analytics, JSONL for pipeline output.
2. Object storage is immutable and versioned.
3. Partition by low-cardinality provenance keys.
4. Provenance survives the format change.