# Data Engineering 09: ETL vs ELT and CDC

## Topic Overview

Where the transform happens is the ETL-versus-ELT question, and whether the transform runs continuously
on change is the CDC question. ETL transforms before loading, in a purpose-built pipeline; ELT loads
raw first and transforms inside the warehouse. CDC captures row-level changes from a transactional
database and streams them downstream, so a search index, cache, or warehouse reflects the source in
near real time instead of on a nightly reload.

The shift from ETL to ELT is a consequence of storage getting cheap and compute moving into the
warehouse. Once the destination is itself a compute engine (Snowflake, BigQuery, Spark), the
transform can happen there, and the raw data is kept for re-transformation. That single change — keep
raw, transform late — is what makes a pipeline re-runnable against new business logic without
re-reading the source.

CDC is the streaming answer to a specific problem: a transactional system owns the truth, and every
other system is a derived view of it. Rather than full reloads, CDC reads the database's own change log
and propagates only the deltas. For Athar, the source is books, not a transactional table, but the same
pattern applies to a Shamela database sync or to invalidating DevMate's cache when an underlying record
changes.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the difference between ETL and ELT and when each wins.
2. Justify keeping raw data in the destination and transforming late.
3. Explain Change Data Capture and why log-based beats query-based.
4. Describe how Debezium and Flink CDC read a database's change log.
5. Map before/after row images to insert, update, and delete downstream.
6. Apply CDC to cache invalidation and search-index sync.
7. Connect re-transformation to the re-run safety of earlier lectures.

## Prerequisites

- Data Engineering 01 (ETL) for the transform stage's role.
- Data Engineering 08 (batch vs streaming) for where CDC sits on the streaming side.

---

## 1. ETL Versus ELT

### The classic ETL

ETL extracts, transforms in a purpose-built stage, then loads a clean result into the warehouse. The
transform is done once, in the pipeline, and the warehouse stores only the finished shape. The rule
from Data Engineering 01 — transform pure, load idempotent — is the classic form.

### The ELT shift

ELT extracts, loads the raw data into the warehouse first, and transforms inside the warehouse as a
later step. The raw layer is kept; the transform is expressed in the warehouse's SQL. The shift became
practical when the destination was itself a powerful compute engine.

### The deciding factor

The deciding factor is where the compute power and the need to re-transform live. If the destination
is a warehouse with real compute, ELT lets you re-transform raw data without re-reading the source. If
the destination is a dumb sink, ETL must do the transform first. The trade is raw-storage cost against
re-runnability: ELT keeps raw, pays storage, and buys the ability to change the transform later.

## 2. Why Transform Late

### Keep raw, transform late

The ELT insight is that raw data is the durable asset and the transform is an opinion you may revise.
When the transform changes — a new normalization rule, a bug fix — ELT re-runs the transform against
the stored raw layer. ETL must go back to the source, which may be gone or expensive to re-read.

### The link to re-run safety

This is the same principle as Data Engineering 01's "pipeline as a function": keep the input so the
function can be re-applied. ELT makes the warehouse hold the input, so the transform is always
re-runnable against it. The raw layer is the source of record inside the system.

### The cost and the guardrail

The cost is storage, and the guardrail is that the raw layer must be immutable and complete, exactly
like the object-storage principles of Data Engineering 07. A raw layer that is overwritten in place
breaks the re-runnability that justified ELT in the first place.

## 3. Change Data Capture

### What CDC is

CDC captures row-level changes — insert, update, delete — from a transactional database and propagates
them downstream. Instead of a full reload, only the deltas move. The downstream system (search index,
cache, warehouse, analytics) stays a faithful, near-real-time view of the source.

### The two forms

Query-based CDC polls the table for rows changed after a timestamp. It is simple but cannot see
deletes, and it risks missing or double-reading rows between polls. Log-based CDC reads the database's
own write-ahead log (MySQL binlog, Postgres WAL) and therefore sees every change exactly once,
including deletes.

### Why log-based wins

Log-based CDC is complete and ordered, because the log is the database's own record of truth. It is the
same "ordered, replayable log" idea as the broker in Data Engineering 08, but it is produced by the
database itself. The log is what makes deletes visible and ordering exact.

## 4. Debezium and Flink CDC

### Debezium

Debezium is the log-based CDC connector that reads binlog and WAL, converts each change to a record
with before and after row images, and publishes to Kafka. It turns the database's internal log into a
stream, without polling:

```text
MySQL binlog ──> Debezium ──> Kafka topic ──> consumers (index, cache, warehouse)
```

### Flink CDC

Flink CDC combines Debezium's connectors with Flink's streaming engine, so the captured changes feed
stateful aggregation, joins, and exactly-once sinks directly. Where Debezium alone produces a stream,
Flink CDC both captures and processes it in one engine.

### The record shape

The unit of CDC is the change record with two images:

```python
{"op": "u", "before": {"id": 7, "title": "old"}, "after": {"id": 7, "title": "new"}}
```

The `op` is insert, update, or delete; `before` and `after` are the row images. Downstream logic maps
these to its own operations, and this mapping is where correctness lives.

## 5. Applying Changes Downstream

### The mapping

Each change record maps to a downstream operation. Insert and update become an upsert; delete becomes a
remove. The key is that the downstream operation is derived from the change record, never guessed:

```python
def apply_change(change: dict, index: dict) -> None:
    if change["op"] in ("c", "u"):
        index[change["after"]["id"]] = change["after"]  # upsert
    elif change["op"] == "d":
        index.pop(change["before"]["id"], None)  # remove
```

### The ordering rule

Changes for one row must apply in log order, or a stale update can overwrite a newer one. This is the
same ordering discipline as streaming in Data Engineering 08: within a partition (one row's key), order
is preserved; across rows, it does not matter.

### The link to idempotency

An upsert is naturally idempotent: replaying the same change leaves the same state. That is why CDC
sinks are safe to replay — the operation, not the count of operations, determines the state, which is
the idempotency principle from Data Engineering 03.

## 6. Cache Invalidation and Index Sync

### The canonical use case

The most common CDC use is keeping a derived view in sync. When a source row changes, the search index
must re-index it and the cache must drop the stale entry. CDC turns "invalidate on change" from a
manual concern into a stream the cache and index subscribe to.

### The failure mode

Stale cache is the concrete failure: the source changed, the cache did not, and the user sees an old
answer. CDC removes the timing gap by propagating the change immediately instead of on a schedule. The
link to provenance (Data Engineering 06) is direct: the cache key carries a source version, and CDC is
what bumps it.

### The Athar/DevMate mapping

Athar's book revision is a coarse-grained change: a new `source_version` replaces the old. DevMate's
underlying records, if they lived in Postgres, would emit CDC change records that invalidate the
semantic cache and re-index Qdrant. The mechanism is the same at every granularity.

## 7. Choosing Among These

### ETL, ELT, or CDC

ETL when the destination is a dumb sink or the transform must run outside the warehouse. ELT when the
destination is a compute engine and re-transformation matters. CDC when a transactional system is the
source of truth and downstream views must follow it in near real time.

### They compose

They are not mutually exclusive. A modern pipeline often is ELT for the analytical warehouse and CDC
for the operational views (search, cache). The Athar corpus is batch ETL from book files; a Shamela
metadata sync would be CDC from the source database. The choice follows the source, exactly as the
batch-versus-stream decision did.

### The exit-test connection

Every choice returns to re-run safety: ETL re-runs from the source, ELT re-runs from the raw layer, and
CDC replays from the log. All three make the pipeline a function of its input, which is the property
the roadmap's exit test checks.

## Real-World Application

- Loading raw Athar book pages into a warehouse and expressing normalization as SQL, so a rule change
  re-runs against the stored raw layer.
- Using Debezium to stream a Shamela metadata table's changes into Kafka, then into the search index.
- Invalidating DevMate's semantic cache when an underlying document changes, via the change record.
- Applying change records as upserts and deletes so a replay leaves the same state.

## Common Mistakes

1. **Query-based CDC for deletes.** Deleted rows are never seen and linger downstream.
2. **Transforming before load when the warehouse has compute.** Forgoes re-runnability for no reason.
3. **Overwriting the raw layer in place.** Breaks the re-transformation ELT promised.
4. **Applying changes out of order.** A stale update overwrites a newer one for the same row.
5. **Ignoring the before image.** Deletes and some updates cannot be applied without it.
6. **Re-implementing CDC by full reload.** Polling the whole table to find deltas.

## Key Takeaways

1. ETL transforms before load; ELT loads raw and transforms in the warehouse.
2. ELT's raw layer makes the transform re-runnable without re-reading the source.
3. CDC propagates row-level deltas; log-based CDC is complete and ordered, unlike polling.
4. Debezium reads binlog/WAL into Kafka; Flink CDC adds a processing engine on top.
5. Apply changes as upserts and deletes in log order, so replays stay idempotent.

## Self-Check Questions

1. What deciding factor tips a pipeline from ETL toward ELT?
2. Why does the raw layer in ELT have to be immutable and complete?
3. Why can query-based CDC not see deletes, and why does log-based CDC solve this?
4. What are the before and after images used for in a change record?
5. Why does applying changes in log order matter, and how does it relate to idempotency?

## Further Reading / Connections

- Data Engineering 01 (ETL) — the transform stage whose position this lecture relocates.
- Data Engineering 03 (idempotency) — the upsert semantics CDC sinks rely on.
- Data Engineering 06 (provenance) — the source version that CDC bumps.
- Data Engineering 08 (batch vs streaming) — the log and ordering that CDC inherits.
- Data Engineering 10 (lakehouse) — where ELT's destination increasingly lives.
