# Data Engineering 15: Storage Systems and Database Selection — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Object storage | Immutable, versioned blob store | S3, ADLS, GCS |
| Parquet | Columnar, compressed, schema-enforced format | queryable corpus |
| ORC | Hive-optimized columnar with ACID | warehouse tables |
| Avro | Row-based with schema evolution | Kafka messages |
| Partitioning | Split data by filter keys for scan pruning | `book_id=.../source_version=.../` |
| Data skipping | Skip files via min/max and bloom filters | range excludes the filter |
| PostgreSQL | General relational default, `pgvector` | metadata + vectors |
| Snowflake | Cloud warehouse, storage/compute separated | ELT destination |
| Cassandra | Self-managed wide-column, write-heavy | key lookups at scale |
| Neo4j | Property-graph database, Cypher | multi-hop traversal |

---

## Alphabetical Glossary

### Avro

**Definition:** A row-based serialization format with schema evolution baked in — the schema travels with
the data, so readers resolve fields by name. Built for streaming records, not columnar analytics.

**Example:**
```python
# a Kafka message serialized as Avro with an embedded schema
```

**Related concepts:** Parquet, ORC

---

### Cassandra

**Definition:** A self-managed wide-column store keyed by a partition key with clustering columns,
optimized for write-heavy, single-key lookups at massive scale. The access pattern must be known in
advance.

**Example:**
```python
# read a row by partition key, then sort by clustering columns
```

**Related concepts:** DynamoDB, NoSQL

---

### Data skipping

**Definition:** The technique of skipping whole files during a scan because their column statistics
(min/max, bloom filters) exclude the query's filter value, even within a partition.

**Example:**
```python
# file min(page)=100 max(page)=200 skipped for page == 5
```

**Related concepts:** Partitioning, Parquet

---

### Neo4j

**Definition:** The property-graph database queried with Cypher, ideal for traversal-heavy queries over
relationships that relational joins handle poorly at depth.

**Example:**
```cypher
MATCH (b:Book)<-[:FROM]-(p:Passage) RETURN p
```

**Related concepts:** Neptune, Graph

---

### ORC

**Definition:** Optimized Row Columnar, a columnar format tuned for Hive: stripe-based storage, lightweight
indexes, and ACID support. The choice for a Hive warehouse with transactional tables.

**Example:**
```text
# Hive table stored as ORC with transactional updates
```

**Related concepts:** Parquet, Avro

---

### Parquet

**Definition:** The columnar, compressed, schema-enforced format with per-column statistics. The analytics
default and the queryable corpus format; reading one column reads only that column's bytes.

**Example:**
```python
# passages.parquet partitioned by book_id and source_version
```

**Related concepts:** ORC, Avro, Data skipping

---

### Partitioning

**Definition:** Dividing data by the columns you filter on so a query reads a subset of files rather than
the whole store. Keys must balance scan size against file count.

**Example:**
```text
corpus/book_id=b1/source_version=v1/part-0000.parquet
```

**Related concepts:** Data skipping, Object storage

---

### PostgreSQL

**Definition:** The general-purpose relational database: ACID, rich SQL, and extensions, most relevantly
`pgvector` for vector search alongside metadata. The default for structured, join-heavy data.

**Example:**
```sql
SELECT * FROM passages WHERE book_id = 'b1';
```

**Related concepts:** Snowflake, Redshift

---

## Related Concepts

- **Lakehouse**: the table format over these files (topic 10)
- **Parquet and object storage**: the substrate this lecture completes (topic 07)
- **ELT and CDC**: Snowflake/Redshift as the ELT destination (topic 09)

## Key Takeaways

1. Object storage is immutable and versioned; partition by filter keys.
2. Parquet for analytics, ORC for Hive/ACID, Avro for streaming evolution.
3. Partitioning prunes scans but must avoid tiny files.
4. Each database family wins a specific data shape.
5. The polyglot principle chooses the right store per data type.
