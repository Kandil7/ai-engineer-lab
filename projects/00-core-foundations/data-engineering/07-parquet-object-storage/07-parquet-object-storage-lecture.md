# Data Engineering 07: Parquet and Object Storage

## Topic Overview

Passages scale beyond JSONL files. Parquet gives columnar, compressed, schema-enforced storage; object
storage (S3, GCS, MinIO) gives durable, cheap, versioned files. Together they are the production home
for a corpus like Athar's, where analytics and storage efficiency matter as much as the retrieval
path.

This lecture covers Parquet's columnar design and why it beats JSONL at scale, the choice between
Parquet and JSONL by workload, object-storage principles, the partition layout that makes scans
efficient, and keeping provenance in the schema when the storage format changes.

The unifying idea is that the storage format changes but the contract does not: a Parquet row is as
traceable as a JSONL row, and the partition layout is the storage-level expression of the provenance
fields.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain Parquet's columnar design and why it beats JSONL at scale.
2. Choose Parquet versus JSONL by workload.
3. Apply object-storage principles: immutability, versioning, cheap reads.
4. Design a partition layout for efficient scans.
5. Keep provenance fields in the Parquet schema.
6. Explain why the storage-level layout mirrors provenance.

## Prerequisites

- Data Engineering 01 (ETL) for the output format and 06 (provenance) for the fields.
- Basic familiarity with files and directories.

---

## 1. Why Parquet

### Columnar storage

JSONL stores rows as text; Parquet stores columns as compressed binary. Reading one column of a
million-row Parquet file reads only that column's bytes, not the whole file.

### The consequences

- **Compression:** column values repeat, so they compress well; a Parquet corpus is a fraction of the
  JSONL size.
- **Speed:** an analytics query that touches one column reads one column, so it is an order of
  magnitude faster.
- **Schema enforcement:** the schema is written into the file, so a malformed row cannot be stored.

### The runner's check

The exercise demonstrates the principle even in the stdlib fallback: a query for the `page` column
reads the page values, not the whole row set. The columnar advantage is conceptual until you use a
real Parquet library, but the principle is the same.

## 2. Parquet Versus JSONL

### Where JSONL wins

JSONL wins for streaming append and human inspection: it is text, one row per line, trivially appended
and read. It is the pipeline's raw output and debugging format.

### Where Parquet wins

Parquet wins for analytics, storage, and schema enforcement: the queryable corpus, the analytics
tables, and the long-term store.

### The pragmatic pattern

Emit both: JSONL for inspection and debugging, Parquet for the queryable corpus and the indexer. Each
format is used where it is strong, rather than forcing one to do both jobs.

### The pipeline position

The pipeline's load stage can write JSONL (the pipeline output) and a Parquet snapshot (the corpus).
The two are consistent because they come from the same transformed rows.

## 3. Object Storage Principles

### Immutability

Object storage treats files as immutable objects addressed by key. Write once; to change, write a new
object. Immutability is what makes an old citation still resolvable (Data Engineering 06): the old
snapshot object is still there.

### Versioning

The store keeps object history, so a key's previous versions are recoverable. This is the storage-level
versioning that backs the source-version provenance.

### Cheap reads

Objects are read whole, so partition the data so a query reads only what it needs. Reading one
partition is cheap; reading the whole bucket is not.

### The cost model

Object storage is cheap to store and cheap to read occasionally, but expensive to read constantly and
to list at scale. The partition layout is how a query avoids reading everything.

## 4. Partition Layout

### The keys

```text
corpus/
  book_id=b1/
    source_version=v1/
      passages.parquet
    source_version=v2/
      passages.parquet
```

### Why these keys

Partitioning by `book_id` then `source_version` means a query for one book's current version reads
exactly one file. The partition keys mirror the provenance fields, so the layout is the storage-level
expression of traceability.

### The exercises

The exercise writes one JSONL file per `(book_id, source_version)` partition and asserts that a query
for one book's v1 reads exactly one file with two rows, all provenance intact.

### The anti-pattern

Partitioning by a high-cardinality key (per-passage) produces millions of tiny files, which is slow to
list and wasteful. Partition by the keys you filter by, not by every field.

## 5. Provenance in the Schema

### The rule

The Parquet schema carries the same provenance fields as the JSONL rows: `book_id`, `page`,
`source_version`, `path`, `original`, `searchable`. A Parquet row is as traceable as a JSONL row.

### Why it matters

When the storage format changes, the contract must not. Dropping provenance to save a few bytes
breaks the citation chain and the audit trail. The format is an implementation detail; provenance is
the contract.

### The link to the schema lecture

This is the same schema discipline as Data Engineering 02 applied to Parquet: the schema is the
contract, and it includes the provenance fields.

## 6. Scaling the Corpus

### The growth path

A small corpus lives comfortably in JSONL. As it grows, Parquet and object storage become necessary:
the JSONL files become too large to load, and the analytics queries too slow. The migration is a load
stage change, not a retrieval change.

### The reader's job

The retrieval path reads the corpus through an abstraction (a reader that lists partitions and filters
by key) rather than directly. The abstraction lets the storage backend change without touching the
retrieval code, which is the same provider-agnostic discipline used for models and stores.

### The consistency check

The Parquet snapshot and the JSONL output must agree because they come from the same transformed rows.
A consistency check (row counts, checksums) catches a load stage that writes one but not the other.

## Real-World Application

- Storing the Athar corpus as Parquet partitioned by `book_id`/`source_version` so a query for one
  book's version reads one file.
- Keeping JSONL as the pipeline's inspectable output alongside the Parquet snapshot.
- Retaining source snapshots immutably so old citations still resolve.
- Carrying the provenance fields in the Parquet schema so a Parquet row is as traceable as a JSONL
  row.

## Common Mistakes

1. **Using JSONL for analytics at scale.** Slow, uncompressed, schema-implicit.
2. **Editing objects in place.** Violates immutability; version instead.
3. **Partitioning by high-cardinality keys.** Too many tiny, slow files.
4. **Dropping provenance in the Parquet schema.** The citation chain breaks.
5. **No consistency check.** The Parquet snapshot and JSONL output drift.

## Key Takeaways

1. Parquet is columnar, compressed, and schema-enforced; JSONL is textual and append-friendly.
2. Emit JSONL for inspection and Parquet for the queryable corpus.
3. Object storage is immutable, versioned, and cheap to read partition by partition.
4. Partition by the keys you filter on (`book_id`, `source_version`), mirroring provenance.
5. The format changes, the contract does not; provenance stays in the schema.

## Self-Check Questions

1. Why is reading one column of a Parquet file cheaper than reading one column of JSONL?
2. When is JSONL the right choice over Parquet?
3. Why does immutability matter for old citations?
4. Why partition by `book_id` and `source_version` rather than by `passage_id`?
5. Why must the Parquet schema keep the provenance fields?

## Further Reading / Connections

- Data Engineering 01 (ETL) and 06 (provenance) — the output and the fields.
- Data Engineering 02 (schemas) — the contract the Parquet schema preserves.
- `projects/04-ai-engineering/athar-lab/` — the pipeline whose output this format scales.
- `docs/reference/llm-production-architecture.md` — storage and data-layer context.
