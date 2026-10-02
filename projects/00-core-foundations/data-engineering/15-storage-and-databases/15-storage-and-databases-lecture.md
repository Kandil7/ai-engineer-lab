# Data Engineering 15: Storage Systems and Database Selection

## Topic Overview

Every data system ends in storage, and the choice of storage is the choice of a query pattern, a
consistency guarantee, and a cost curve. This lecture closes the curriculum by turning the storage
decision into a rubric: object storage for the corpus, columnar files for analytics, and a database
whose model — relational, document, wide-column, time-series, or graph — matches how the data is read
and written.

The file formats are the substrate. Parquet is columnar and compression-friendly; ORC is
Hive-optimized with ACID; Avro is row-based with schema evolution, built for streaming serialization.
The databases are the engines over them: PostgreSQL for relational truth, Snowflake and Redshift for the
analytical warehouse, MongoDB and Cassandra and DynamoDB for the NoSQL models, InfluxDB and TimescaleDB
for time series, and Neo4j and Neptune for graphs. The skill is not knowing every tool but reading the
workload and matching it.

For our systems the answer is already partly written. Athar's corpus is Parquet on object storage, its
vectors in Qdrant, and its metadata relational. DevMate's stats are relational, its cache key-value, and
its retrieval graph-shaped only if the citation graph grows complex. Each data type lands in a different
store, and that is correct, not a failure to standardize.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Apply object-storage best practices: immutability, versioning, lifecycle, and partition pruning.
2. Choose Parquet, ORC, or Avro by workload.
3. Design a partition scheme that prunes scans without creating small files.
4. Place each database family — relational, document, wide-column, time-series, graph — on its strength.
5. Select among PostgreSQL, Snowflake, Redshift, MongoDB, Cassandra, DynamoDB, InfluxDB, TimescaleDB,
   Neo4j, and Neptune with a rubric.
6. Map Athar and DevMate data types to their stores.
7. Defend the polyglot principle: the right store per data shape, not one store for everything.

## Prerequisites

- Data Engineering 07 (Parquet and object storage) for the file substrate.
- Data Engineering 10 (lakehouse) for the table format over those files.

---

## 1. Object Storage Best Practices

### The principles

Object storage (S3, ADLS, GCS) is immutable, versioned, and cheap to store but costly to read wholesale
and to list at scale. The practices follow from that cost model: write objects once, keep versioning on,
tier by access, and partition so a query reads only what it needs.

### The practices

- **Immutability and versioning** — write a new object rather than edit; keep history for rollback.
- **Lifecycle tiers** — hot for recent snapshots, cold for archives; the same retention logic as
  provenance (Data Engineering 06).
- **Prefix partitioning** — encode the partition keys in the object prefix (`book_id=b1/source_version=v1/`)
  so a filter reads one prefix.
- **Avoid hot prefixes** — a high-cardinality key as the first prefix spreads requests; a single hot key
  becomes a throughput bottleneck.

### The link back

These are the Data Engineering 07 principles restated as operations: the layout is the storage-level
expression of traceability, and immutability is what keeps an old citation resolvable.

## 2. Columnar Formats: Parquet, ORC, Avro

### Parquet

Columnar, compressed, schema-enforced, with min/max statistics per column for data skipping. The
analytics default; the queryable corpus format (Data Engineering 07).

### ORC

Also columnar, but Hive-optimized: stripe-based storage, lightweight indexes, and ACID support for
streaming upserts. The choice when the ecosystem is Hive and you need transactional tables.

### Avro

Row-based with schema evolution baked into the format: the schema travels with the data, so readers
resolve fields by name and can evolve additively. Built for serialization and streaming (Kafka
messages), not for columnar analytics.

### The selection

Analytics over many rows, few columns → Parquet. Hive warehouse with ACID → ORC. Streaming records with
evolving schema → Avro. The decision is about the access pattern: columnar reads versus row serialization.

## 3. Partitioning Strategies

### The goal

Partitioning exists so a query reads a subset of files, not the whole store. The partition keys must be
the columns you filter by, and the partition granularity must balance scan size against file count.

### The rules

- **Partition by filter keys.** `book_id`, `source_version`, and a coarse time grain (`year/month/day`)
  are the classic filters.
- **Prune, do not scatter.** A filter on the partition key skips whole prefixes; a filter on a
  non-partition column still reads everything.
- **Avoid small files.** Partitioning by a high-cardinality key (per-passage, per-second) produces many
  tiny files, which is slow to list and wasteful — the anti-pattern of Data Engineering 07.
- **Data skipping.** Within a file, min/max and bloom filters let an engine skip files whose value range
  excludes the filter, even inside a partition.

### The code shape

```text
corpus/
  book_id=b1/
    source_version=v1/
      part-0000.parquet    # read this prefix only for b1/v1
```

## 4. Relational Databases

### PostgreSQL

The general-purpose relational default. ACID, rich SQL, extensions — most relevantly `pgvector` for
vector search, which lets one database hold both metadata and embeddings. The workhorse for DevMate's
stats and Athar's catalog.

### Snowflake and Redshift

The analytical warehouses, built for ELT (Data Engineering 09): load raw, transform in SQL, columnar
storage, separation of storage and compute (Snowflake) or distribution keys (Redshift). The choice when
analytical scale outgrows a single Postgres instance.

### The relational criterion

Choose relational when the data is structured, the queries are joins and aggregations, and you need
ACID guarantees. It is the default until a specific non-relational shape forces a different model.

## 5. NoSQL Families

### Document: MongoDB

Schema-flexible documents, indexed fields, natural for heterogeneous records. Right when the record
shape varies and you query by nested fields, not joins.

### Wide-column: Cassandra and DynamoDB

Keyed by a partition key with clustering columns, optimized for write-heavy, single-key lookups at
massive scale. Cassandra is self-managed and tunable; DynamoDB is managed with single-digit-millisecond
latency. Right when the access is always by key and availability outranks ad-hoc querying.

### The NoSQL criterion

Choose NoSQL when the access pattern is known and fixed — a single-key lookup, a write-heavy stream —
and the relational join model buys nothing. The cost is ad-hoc queries: you must know the access pattern
in advance.

## 6. Time-Series and Graph

### Time-series: InfluxDB and TimescaleDB

Time-series data is append-only, timestamp-ordered, and queried by time range with downsampling. InfluxDB
is the purpose-built metric store with retention policies; TimescaleDB is a PostgreSQL extension that
turns ordinary tables into hypertables partitioned by time, giving SQL on top of time-series. The choice
for DevMate's cost and usage telemetry over time.

### Graph: Neo4j and Amazon Neptune

Graph data is about relationships: who cites whom, which passages reference which books. Neo4j is the
property-graph database with Cypher, ideal for traversal-heavy queries; Neptune is AWS's managed graph
service supporting both property graphs and RDF. The choice when the query is a traversal — "find all
passages that cite this book through two hops" — that a relational join handles poorly at depth.

### The criterion

Choose time-series when the workload is append-only, time-ordered metrics; choose graph when the core
query is multi-hop traversal over relationships. Both exist because the relational model is a poor fit
for those specific shapes.

## 7. The Selection Rubric and the Polyglot Principle

### The rubric

Five questions decide the store: what is the access pattern (key lookup, join, traversal, time range),
what consistency is required (ACID versus eventual), what latency is acceptable, what is the scale, and
what is the operational cost the team can bear. The store that wins each question is rarely the same for
two different data types.

### The polyglot principle

One data system, many stores, each matched to a shape. Athar is already polyglot: Parquet on object
storage for the corpus, Qdrant for vectors, PostgreSQL for metadata and provenance, and — when the
citation graph grows — a graph store for the reference relationships. No single store does all four
well, and forcing one to is the classic over-standardization mistake.

### The exit-test connection

The roadmap's storage bar is that every data type lives in a store that matches its shape, and that the
choice is a reasoned decision, not a default. The rubric, applied honestly, is the deliverable — and the
traceability properties from every earlier lecture survive because the provenance fields travel with the
data into whatever store holds it.

## Real-World Application

- Keeping the Athar corpus as Parquet partitioned by `book_id`/`source_version` on object storage with
  versioning and lifecycle tiers.
- Storing DevMate repository stats and the provenance catalog in PostgreSQL, with `pgvector` for
  metadata-plus-embedding needs.
- Writing usage telemetry to TimescaleDB for time-range dashboards, or InfluxDB for retention-bounded
  metrics.
- Adding a graph store only when the citation graph's traversal queries exceed what Postgres joins do
  at depth.

## Common Mistakes

1. **One store for everything.** The relational default applied to vectors, graphs, and time series.
2. **Partitioning by a high-cardinality key.** Millions of tiny files, slow listing.
3. **Filtering on non-partition columns.** A scan that reads the whole store anyway.
4. **Choosing NoSQL for ad-hoc queries.** The access pattern must be known in advance.
5. **Storing columnar data as Avro, or streaming rows as Parquet.** The format must match the access
   pattern.
6. **No lifecycle policy.** Every snapshot retained hot forever, cost without benefit.

## Key Takeaways

1. Object storage is immutable and versioned; partition by the keys you filter on.
2. Parquet for columnar analytics, ORC for Hive/ACID, Avro for streaming schema-evolution.
3. Partitioning prunes scans but must not scatter into tiny files.
4. Each database family — relational, document, wide-column, time-series, graph — wins a specific shape.
5. The polyglot principle: the right store per data type, chosen by a rubric, not a default.

## Self-Check Questions

1. What three object-storage practices follow from its cost model?
2. When is Avro the right format rather than Parquet?
3. Why is partitioning by a high-cardinality key an anti-pattern?
4. What access pattern tips a dataset from PostgreSQL into a graph store?
5. What five questions make up the storage-selection rubric?

## Further Reading / Connections

- Data Engineering 07 (Parquet and object storage) — the file substrate this lecture completes.
- Data Engineering 10 (lakehouse) — the table format over these files.
- Data Engineering 09 (ELT and CDC) — Snowflake/Redshift as the ELT destination.
- Data Engineering 06 (provenance) — the fields that travel into whatever store is chosen.
- `projects/04-ai-engineering/devmate/src/devmate/` — the stores (Postgres, Qdrant, cache) this maps to.
