# Data Engineering 08: Batch vs Streaming — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Batch | Bounded data processed on a schedule | nightly corpus ingest |
| Streaming | Unbounded events processed as they arrive | live usage telemetry |
| Orchestrator | Schedules a task DAG | Airflow, Prefect |
| Engine | Spreads one job's compute across machines | Apache Spark |
| Broker | Ordered, durable, replayable event log | Kafka, Pulsar, Kinesis |
| Stream engine | Maintains state to compute over the log | Flink, Kafka Streams |
| Lambda | Batch layer + speed layer + serving layer | correct and fresh, two paths |
| Kappa | Single stream; recompute by replaying the log | one path, log as system of record |
| Watermark | Signal that no older events will arrive | close a time window |
| Exactly-once | A retry neither drops nor double-counts | checkpointed streaming state |

---

## Alphabetical Glossary

### Batch

**Definition:** Processing a bounded dataset on a schedule or trigger. Cheap, simple, and re-runnable
from the source. Right for finite corpora like Athar's books.

**Example:**
```python
# a new or corrected book triggers a batch ingest
```

**Related concepts:** Streaming, Orchestrator

---

### Broker

**Definition:** A system that holds an ordered, durable log of records. Producers append; consumers
read by offset. The log is the source of truth and the replay mechanism.

**Example:**
```python
# Kafka topic "usage-events": append-only, ordered per partition
```

**Related concepts:** Streaming, Kappa

---

### Exactly-once

**Definition:** The guarantee that a crash and retry neither drops an event nor processes it twice.
Achieved by writing state and output atomically with a checkpoint.

**Example:**
```python
# checkpoint (offset, window_state) written together with output
```

**Related concepts:** Checkpointing, Streaming

---

### Kappa

**Definition:** Architecture that treats everything, including history, as a stream with a single
processing path. Reprocessing means resetting the offset and replaying the log.

**Example:**
```python
# recompute = reset consumer offset to zero and replay
```

**Related concepts:** Lambda, Broker

---

### Lambda

**Definition:** Architecture with a batch layer (correct, stale by one cycle), a speed layer (fresh,
recent window), and a serving layer that merges them. Costs two code paths.

**Example:**
```text
batch view (through yesterday) + speed view (today) = query result
```

**Related concepts:** Kappa, Batch, Streaming

---

### Orchestrator

**Definition:** A scheduler that turns a dependency graph of tasks into a schedule, enforcing order,
retries, and backfills.

**Example:**
```python
extract_task >> transform_task >> load_task  # Airflow DAG
```

**Related concepts:** Engine, Batch

---

### Streaming

**Definition:** Processing an unbounded feed of events as they arrive. Adds ordering, exactly-once, and
state costs, paid continuously.

**Example:**
```python
# live usage events aggregated in a rolling window
```

**Related concepts:** Batch, Broker, Watermark

---

### Watermark

**Definition:** A progress signal telling a streaming engine that no event older than a timestamp will
arrive, so a window can be closed and emitted. Trades latency against completeness.

**Example:**
```python
# watermark = max_event_time - allowed_lateness
```

**Related concepts:** Streaming, Exactly-once

---

## Related Concepts

- **Checkpointing**: the durable state that lets a streaming job resume (topic 04)
- **Idempotency**: the property that makes a streaming retry safe (topic 03)
- **Feature pipelines**: where streaming aggregation produces features (topic 13)

## Key Takeaways

1. Batch for bounded sources; stream only the latency-bound slice.
2. Orchestrators schedule, engines compute; they are different tools.
3. The broker's replayable log is what makes streaming recoverable.
4. Lambda costs two code paths; Kappa costs log retention.
5. Ordering and exactly-once are the continuous costs of streaming.
