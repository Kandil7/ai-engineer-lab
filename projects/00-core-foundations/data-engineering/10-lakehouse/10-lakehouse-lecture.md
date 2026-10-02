# Data Engineering 10: Lakehouse — Iceberg and Delta Lake

## Topic Overview

A data lake holds raw files on cheap object storage; a data warehouse holds structured, ACID tables on
expensive, proprietary compute. The lakehouse is the synthesis: data stays on object storage in open
files, but a table format adds the warehouse's guarantees — ACID transactions, schema enforcement, and
time travel — on top of them. Iceberg and Delta Lake are the two leading table formats that make this
possible.

The problem they solve is the lake's chronic weakness. A lake with bare Parquet files has no
transactions, no safe concurrent writes, no schema enforcement, and no way to ask "what did this table
look like yesterday." The table format adds a metadata layer that turns a directory of files into a
versioned table: each write produces a new snapshot, and every snapshot is queryable forever.

For Athar this matters directly. The corpus is partitioned Parquet on object storage (Data Engineering
07), and the provenance fields carry a `source_version`. A lakehouse table format turns those
partitions into a versioned table where the re-ingest of a corrected book is a new snapshot, and an old
citation can still resolve by reading the snapshot that existed when it was written — the same
traceability promise as provenance, implemented at the table level.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the difference between a lake, a warehouse, and a lakehouse.
2. Describe what a table format adds to bare Parquet files.
3. Explain ACID transactions and time travel on object storage.
4. Compare Iceberg and Delta Lake along their core mechanisms.
5. Design the Athar corpus as a versioned table with time travel.
6. Explain schema evolution and partition evolution.
7. Connect snapshots to the provenance discipline of earlier lectures.

## Prerequisites

- Data Engineering 07 (Parquet and object storage) for the files the table format governs.
- Data Engineering 06 (provenance) for the versioning the snapshots mirror.

---

## 1. Lake, Warehouse, Lakehouse

### The lake

A lake is raw data on cheap object storage in open formats (Parquet, ORC). It is cheap and flexible but
has no transactions, no schema enforcement, and no versioning; a directory of files is not a table.

### The warehouse

A warehouse is structured data in a proprietary engine with ACID guarantees, but it is expensive, locks
data into one engine, and struggles with the scale and cost of holding everything raw.

### The lakehouse

The lakehouse keeps the lake's economics and openness but adds a table format that imposes the
warehouse's guarantees. Data remains on object storage in open files, and the table format supplies the
metadata, transactions, and versioning. It is the answer to "keep raw, transform late" from Data
Engineering 09, with the guarantees the transform needs.

## 2. What the Table Format Adds

### The metadata layer

A table format is a layer of metadata over data files. It tracks which files belong to which snapshot,
their schema, and their partition statistics. The data files are still plain Parquet; the metadata is
what turns them into a table.

### The guarantees

With that metadata, the format provides three things bare files lack:

- **ACID transactions** — a write is atomic: readers see either the old snapshot or the new one, never a
  partial write.
- **Schema enforcement and evolution** — the schema is in the metadata and can be evolved additively
  without rewriting data.
- **Time travel** — every write is a named snapshot, and any snapshot is queryable later.

### The analogue

This is the same idea as the append-only event log in Data Engineering 08, applied to tables: never
mutate in place, always append a new snapshot, keep the old one readable. Immutability is the property
that makes history available.

## 3. Iceberg

### The model

Iceberg is the open-source table format built for portability across engines. It organizes a table as a
tree of metadata files: a manifest list points to manifests, which point to data files, and a metadata
file points to the current snapshot.

```text
metadata.json ──> snapshot (manifest list) ──> manifests ──> data files
```

### The strengths

Iceberg's defining features are **hidden partitioning** (the physical layout is decoupled from the
logical partition column, so queries do not need to know the layout) and **partition evolution** (the
partition scheme can change without rewriting the table). Time travel and schema evolution are
first-class. Because it is engine-neutral, Iceberg is the format for a multi-engine world — Spark,
Trino, Flink, Dremio — all read the same table.

### The map to provenance

Iceberg's snapshot plus the `source_version` column is exactly the two-level versioning of Data
Engineering 06: the table version (snapshot) and the data version (source_version) are independent and
both must resolve for a trace.

## 4. Delta Lake

### The model

Delta Lake, from Databricks, uses a transaction log of JSON files (the `_delta_log`) and Parquet data
files. Each write appends a commit to the log, and the log is the ordered source of truth for what
changed.

```text
_delta_log/
  000000.json    # commit: which files, which schema, which snapshot
  000001.json
data/
  part-0000.parquet
```

### The strengths

Delta Lake is deeply integrated with Spark, has ACID guarantees, time travel, and schema evolution, and
adds performance features like Z-ordering (multi-dimensional clustering) and delta versioning. Its
commit log is an ordered, replayable history — the same log concept that runs through this curriculum.

### Iceberg versus Delta

Both deliver ACID and time travel; the difference is emphasis and ecosystem. Iceberg is engine-neutral
and excels at partition evolution and multi-engine reads; Delta Lake is Spark-centric and excels at
single-vendor integration and query optimization. The choice is usually a platform decision, not a
correctness one.

## 5. Time Travel and Snapshots

### What time travel is

Time travel is querying a table as it existed at a past snapshot or timestamp. The table format keeps
every snapshot, so an old state is not overwritten but still addressable:

```python
# read the corpus as it existed at source_version v1 (a past snapshot)
rows = table.time_travel(snapshot_id="snap_v1").read()
```

### Why it matters for citations

A RAG answer cites a passage. If the corpus is a versioned table, the citation can resolve against the
snapshot that existed when the passage was written, even after later re-ingests. This is the storage
level of "old citations still resolve" from Data Engineering 07, made systematic.

### The retention trade

Keeping every snapshot forever costs storage. Object-storage lifecycle tiers and snapshot-expiration
policies bound that cost, but the rule is the same as provenance retention: keep snapshots long enough
for the trace to resolve, no longer.

## 6. Schema and Partition Evolution

### Schema evolution

Adding a column is backward-compatible: old data files lack the column and read as null. The table
format records the new schema without rewriting existing files, which is the additive-evolution rule
from Data Engineering 02, applied to files.

### Partition evolution

Iceberg's hidden partitioning lets the partition scheme change without a rewrite. A table partitioned by
`book_id` can evolve to partition by `book_id` and `source_version`; the metadata, not the file layout,
carries the mapping, and existing queries keep working.

### The link to the partition lecture

This is the guardrail for the partition layout of Data Engineering 07: choose partition keys by how you
filter, and know that a table format lets you evolve the scheme if that choice was wrong, without
paying a full rewrite.

## 7. The Athar Corpus as a Lakehouse

### The design

The Athar corpus is Parquet partitioned by `book_id` and `source_version`, governed by an Iceberg (or
Delta) table. Each re-ingest is a transaction that adds a snapshot. The provenance columns remain in the
schema, so a table row is as traceable as a JSONL row.

### The operations it enables

- A corrected book re-ingest is a new snapshot, and the old one stays queryable for old citations.
- A reader that lists partitions by key (Data Engineering 07) becomes a reader that time-travels by
  snapshot, without touching the retrieval code.
- Schema evolution lets a new provenance field (for example, a content hash) be added without rewriting
  the corpus.

### The exit-test connection

The roadmap bar is traceability and safe re-runs. A lakehouse table makes re-runs transactions (a
failed re-ingest never leaves a partial snapshot) and makes traceability a query (time travel to the
snapshot). Both properties are the data-engineering exit test, implemented in the storage layer.

## Real-World Application

- Storing the Athar corpus as an Iceberg table over Parquet, partitioned by book and source version.
- Re-ingesting a corrected book as a new snapshot so old citations resolve via time travel.
- Evolving the schema to add a content-hash column without rewriting existing files.
- Choosing Iceberg for multi-engine reads (Spark for recompute, Trino for analytics) over the same
  table.

## Common Mistakes

1. **Treating a directory of Parquet as a table.** No transactions, no versioning, no evolution.
2. **Editing data files in place.** Breaks every snapshot that referenced them.
3. **Dropping provenance in the table schema.** Time travel works but the trace breaks.
4. **Keeping every snapshot forever.** Storage cost with no resolution benefit.
5. **Rewriting the table for a schema add.** Schema evolution exists precisely to avoid that.
6. **Partitioning by a high-cardinality key and then needing a rewrite.** Choose filter keys first.

## Key Takeaways

1. A lakehouse is cheap open storage plus a table format's ACID and time travel.
2. The table format adds a metadata layer over plain Parquet files.
3. Iceberg is engine-neutral with partition evolution; Delta Lake is Spark-centric with a commit log.
4. Time travel makes an old citation resolvable against the snapshot that existed then.
5. Schema and partition evolution avoid rewrites, the additive rule from earlier lectures.

## Self-Check Questions

1. What does the table format add to a directory of bare Parquet files?
2. Why does time travel make old citations resolvable, and at what storage cost?
3. What is hidden partitioning, and why does it make partition evolution cheap?
4. How do Iceberg and Delta Lake differ in emphasis?
5. How does a lakehouse table turn a re-ingest into a transaction?

## Further Reading / Connections

- Data Engineering 07 (Parquet and object storage) — the data files the table governs.
- Data Engineering 06 (provenance) — the versioning the snapshots mirror.
- Data Engineering 09 (ELT and CDC) — the destination this lecture upgrades.
- Data Engineering 02 (schemas) — the additive-evolution rule the formats honor.
- Data Engineering 14 (versioning and lineage) — lineage across the table's snapshots.
