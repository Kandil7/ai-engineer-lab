# Data Engineering 09: ETL vs ELT and CDC — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| ETL | Extract, transform, then load a clean result | pipeline writes finished tables |
| ELT | Extract, load raw, transform in the warehouse | raw layer + SQL transforms |
| Raw layer | Immutable, complete copy of source data in the destination | warehouse staging tables |
| CDC | Change Data Capture: propagate row-level deltas | insert/update/delete stream |
| Query-based CDC | Poll rows changed after a timestamp | `WHERE updated_at > ?` |
| Log-based CDC | Read the database's write-ahead log | binlog, WAL |
| Debezium | CDC connector that publishes binlog/WAL to Kafka | MySQL → Kafka topic |
| Flink CDC | Debezium connectors plus a Flink processing engine | capture and aggregate |
| Before/after image | Row state before and after a change | `{"op":"u","before":...,"after":...}` |
| Upsert | Insert-or-update, naturally idempotent | apply change as upsert |

---

## Alphabetical Glossary

### Before/after image

**Definition:** The row's state before and after a change, carried by a CDC record. The before image is
required to apply deletes and some updates.

**Example:**
```python
{"op": "u", "before": {"id": 7, "title": "old"}, "after": {"id": 7, "title": "new"}}
```

**Related concepts:** CDC, Upsert

---

### CDC

**Definition:** Change Data Capture — capturing insert, update, and delete events from a transactional
database and propagating them to downstream systems, so they stay a near-real-time view of the source.

**Example:**
```text
MySQL binlog -> Debezium -> Kafka -> search index / cache
```

**Related concepts:** Log-based CDC, Debezium

---

### Debezium

**Definition:** Open-source CDC connectors that read a database's binlog or WAL and publish change
records to Kafka. Log-based, so complete and ordered, including deletes.

**Example:**
```python
# binlog record becomes a Kafka record with before/after images
```

**Related concepts:** Log-based CDC, Flink CDC

---

### ELT

**Definition:** Extract, load raw data into the destination, then transform inside the warehouse's
compute. Keeps raw so the transform can be re-run without re-reading the source.

**Example:**
```sql
-- raw layer loaded first, then a transform view
CREATE TABLE passages_clean AS SELECT normalize(original) FROM passages_raw;
```

**Related concepts:** ETL, Raw layer

---

### ETL

**Definition:** Extract, transform in a purpose-built pipeline stage, then load the finished result.
The classic form, right when the destination is a dumb sink or the transform must run outside the
warehouse.

**Example:**
```python
extract(source) -> transform(pages) -> load(passages, warehouse)
```

**Related concepts:** ELT, Transform

---

### Log-based CDC

**Definition:** CDC that reads the database's own write-ahead log (binlog, WAL), so every change is seen
exactly once, in order, including deletes. Contrasts with polling.

**Example:**
```python
# Postgres WAL stream -> Debezium -> change records
```

**Related concepts:** CDC, Query-based CDC

---

### Raw layer

**Definition:** The immutable, complete copy of source data kept in the destination under ELT. It is the
source of record inside the system and makes re-transformation possible.

**Example:**
```python
# passages_raw holds every ingested row, never overwritten in place
```

**Related concepts:** ELT, Immutability

---

### Upsert

**Definition:** Insert-or-update by key. Naturally idempotent — replaying the same change leaves the
same state — which is why CDC sinks are safe to replay.

**Example:**
```python
index[key] = change["after"]  # insert or replace
```

**Related concepts:** CDC, Idempotency

---

## Related Concepts

- **Idempotency**: the property upserts give a CDC replay (topic 03)
- **Provenance**: the source version a change record bumps (topic 06)
- **Lakehouse**: where the ELT destination increasingly lives (topic 10)

## Key Takeaways

1. ETL transforms before load; ELT keeps raw and transforms late.
2. The immutable raw layer is what makes ELT re-runnable.
3. CDC propagates deltas; log-based CDC is complete and ordered.
4. Debezium publishes binlog/WAL; Flink CDC adds a processing engine.
5. Upserts and deletes in log order keep replays idempotent.
