# Data Engineering 10: Lakehouse — Iceberg and Delta Lake — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Data lake | Raw files on cheap object storage | bare Parquet on S3 |
| Warehouse | Structured, ACID data in a proprietary engine | Snowflake, Redshift |
| Lakehouse | Lake economics plus table-format ACID/time travel | Iceberg over Parquet |
| Table format | Metadata layer turning data files into a versioned table | Iceberg, Delta Lake |
| Snapshot | A named, immutable point-in-time state of a table | `snap_v1` |
| Time travel | Querying a table at a past snapshot | read snapshot v1 |
| Hidden partitioning | Layout decoupled from the logical partition column | Iceberg |
| Partition evolution | Change the partition scheme without a rewrite | Iceberg |
| Schema evolution | Add columns additively without rewriting data | `source_hash` added |
| ACID | Atomic, Consistent, Isolated, Durable transactions | a write is all-or-nothing |

---

## Alphabetical Glossary

### ACID

**Definition:** The transaction guarantees the table format adds: a write is atomic (readers see old or
new, never partial), and the result is durable. The reason a lakehouse is more than a directory.

**Example:**
```python
# a re-ingest commits a snapshot atomically; readers never see a half-written table
```

**Related concepts:** Lakehouse, Snapshot

---

### Delta Lake

**Definition:** A table format from Databricks using a `_delta_log` of JSON commits over Parquet files.
Spark-centric, with ACID, time travel, Z-ordering, and schema evolution.

**Example:**
```text
_delta_log/000000.json -> data/part-0000.parquet
```

**Related concepts:** Iceberg, Table format

---

### Iceberg

**Definition:** The open, engine-neutral table format. Organizes tables as metadata, manifest list, and
manifests over data files. Known for hidden partitioning and partition evolution.

**Example:**
```text
metadata.json -> manifest list -> manifests -> data files
```

**Related concepts:** Delta Lake, Table format

---

### Lakehouse

**Definition:** The architecture that keeps data on open object storage but adds a table format's ACID
transactions, schema enforcement, and time travel, combining lake economics with warehouse guarantees.

**Example:**
```python
# Athar corpus: Parquet partitioned by book_id/source_version, governed by Iceberg
```

**Related concepts:** Data lake, Warehouse, Table format

---

### Snapshot

**Definition:** A named, immutable state of a table produced by a write. Every snapshot is queryable,
which is what makes time travel possible.

**Example:**
```python
table.time_travel(snapshot_id="snap_v1").read()
```

**Related concepts:** Time travel, ACID

---

### Table format

**Definition:** The metadata layer over data files that tracks snapshots, schema, and partition
statistics, turning plain Parquet files into a versioned, transactional table.

**Example:**
```python
# Iceberg or Delta Lake over Parquet data files
```

**Related concepts:** Iceberg, Delta Lake, Lakehouse

---

### Time travel

**Definition:** Querying a table as it existed at a past snapshot or timestamp. Every snapshot is
retained, so old states remain addressable.

**Example:**
```python
# resolve an old citation against the corpus snapshot at the time it was written
```

**Related concepts:** Snapshot, Provenance

---

## Related Concepts

- **Provenance**: the source version the snapshots mirror (topic 06)
- **Parquet and object storage**: the data files the table governs (topic 07)
- **ELT and CDC**: the destination this lecture upgrades (topic 09)

## Key Takeaways

1. A lakehouse adds ACID and time travel to cheap open storage.
2. The table format is a metadata layer over plain Parquet files.
3. Iceberg is engine-neutral; Delta Lake is Spark-centric.
4. Time travel keeps old citations resolvable.
5. Schema and partition evolution avoid full rewrites.
