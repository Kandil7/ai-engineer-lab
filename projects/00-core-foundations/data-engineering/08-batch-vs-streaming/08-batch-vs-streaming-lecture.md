# Data Engineering 08: Batch vs Streaming

## Topic Overview

Batch and streaming are the two ways a pipeline relates to time. Batch processes a bounded dataset on
a schedule; streaming processes an unbounded event feed as it arrives. The choice is not a matter of
taste but of two facts: is the source finite, and how fresh must the consumer's view be. Data
Engineering 01 sketched the decision; this lecture gives it machinery, the tools each side uses, and
the two architectures that try to get both at once.

The tooling splits cleanly. Batch runs on orchestrators (Airflow, Prefect) and distributed engines
(Apache Spark). Streaming runs on brokers that hold the event log (Kafka, Pulsar, Kinesis) and engines
that process it (Flink, Spark Structured Streaming, Kafka Streams). Knowing the tool is less important
than knowing the contract each enforces: an orchestrator guarantees a schedule and a dependency graph;
a broker guarantees an ordered, replayable log.

The architectures are the hard part. Lambda runs a batch layer and a speed layer in parallel and
merges them; Kappa runs a single stream and reprocesses by replaying the log. Both exist to answer one
question: how do I get fresh results without giving up the correctness of a full batch recomputation.
For Athar, the answer is usually batch; for DevMate's live telemetry, it begins to lean streaming.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose batch versus streaming from the source and the freshness requirement.
2. Place the right tool on each side: orchestrator versus broker, engine versus engine.
3. Explain Lambda architecture, its three layers, and why it needs two code paths.
4. Explain Kappa architecture and what replaying the log buys.
5. Reason about exactly-once and ordering, the two costs streaming charges.
6. Map the Athar corpus to batch and DevMate telemetry to the streaming candidate.
7. Defend the default: batch first, streaming only when freshness demands it.

## Prerequisites

- Data Engineering 01 (ETL) for the batch-versus-stream decision at the stage level.
- Data Engineering 03 (idempotency) and 04 (checkpointing) for the correctness streaming depends on.

---

## 1. The Decision, Revisited

### Two questions, not one

Batch versus streaming is answered by two questions. First, is the source bounded? A book corpus is
bounded; a live chat feed is not. Second, how fresh must the result be? A nightly citation corpus is
fine at daily freshness; a recommendation that must reflect the last click needs seconds.

### The default

Start with batch. Batch is cheap, simple, and re-runnable from the source. Streaming's cost is paid
continuously — ordering, exactly-once, state, backpressure — while its benefit applies only when
freshness matters. The rule is: batch until a real latency requirement appears, then move exactly the
latency-sensitive slice, not the whole pipeline.

### Where the boundary sits for us

Athar is bounded: books are finite and change rarely, so a new book is a batch trigger. DevMate's cost
ledger and cache-hit counters are bounded per day and fit batch aggregation. The streaming candidate is
live usage telemetry, where a dashboard should update in near real time, but that is a small, clearly
latency-bound slice.

## 2. Batch Tooling

### Orchestrators: Airflow and Prefect

An orchestrator turns a dependency graph (a DAG) into a schedule. Airflow expresses each task as an
operator, the DAG as Python, and the scheduler enforces ordering, retries, and backfills. Its mental
model is a scheduler with a directed acyclic graph of tasks:

```python
# Airflow-style DAG: extract -> transform -> load, with retries.
with DAG("corpus_ingest", schedule="@daily") as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load, retries=2)
    extract_task >> transform_task >> load_task
```

Prefect makes the same idea more Python-native: a workflow is a decorated function whose dependencies
are ordinary calls, with the runtime adding retries, caching, and observation. The trade is Airflow's
mature scheduling and ecosystem against Prefect's lower ceremony.

### The distributed engine: Spark

Spark is not an orchestrator; it is the compute that executes a batch job across many machines. Where
an orchestrator says when and in what order, Spark says how to spread one job's work. It reads Parquet
(Data Engineering 07), pushes down predicates to skip partitions, and is the workhorse for
recomputation at corpus scale.

### The split to remember

Orchestrator = schedule and dependency. Engine = parallel compute for one job. A large batch pipeline
uses both: Airflow schedules a Spark job nightly. Conflating them is the most common tooling mistake in
this space.

## 3. Streaming Tooling

### The broker: Kafka, Pulsar, Kinesis

A broker is an ordered, durable log of records. Producers append; consumers read with an offset. The
log is the source of truth and the replay mechanism. Kafka is the de facto standard; Pulsar adds
built-in tiered storage; Kinesis is AWS's managed answer. The contract is the same: append-only,
ordered within a partition, replayable.

### The engine: Flink and friends

The engine consumes the log and maintains state to compute over time: aggregations, joins, and windows.
Flink is the reference engine, with true streaming semantics and exactly-once state. Kafka Streams is a
library built into Kafka; Spark Structured Streaming applies Spark's batch engine to micro-batches.

### Why the log matters

Because the log is replayable, a streaming job can be rebuilt from zero by replaying history. That
single property — replayability — is what makes streaming recoverable and is the foundation Kappa
architecture stands on.

## 4. Lambda Architecture

### The three layers

Lambda, from Nathan Marz, runs three layers:

- **Batch layer** — the immutable master dataset and the batch views recomputed from it. Always
  correct, always stale by one cycle.
- **Speed layer** — incremental real-time views that cover only the recent window, trading some
  correctness for freshness.
- **Serving layer** — merges the two: batch view up to yesterday plus speed view for today.

```text
events ──> batch layer ──> batch view ─┐
   │                                   ├──> serving layer ──> query
   └──> speed layer ──> realtime view ─┘
```

### The cost: two code paths

The batch view and the speed view are two different implementations of the same logic — one in Spark,
one in Flink — that must agree at the seam. That dual maintenance is the well-known cost of Lambda. The
inconsistency between the two layers is a correctness bug that only appears when the two views disagree.

### When Lambda still wins

Lambda remains justified when the batch computation is fundamentally different from the incremental one
(for example, a full recomputation that cannot be expressed incrementally), and when the team can
afford to keep two paths in sync.

## 5. Kappa Architecture

### One path, everything is a stream

Kappa, from Jay Kreps, eliminates the batch layer. Everything — including the historical data — is a
stream, and there is a single processing path. Reprocessing is replay: point the same job at an earlier
offset in the log.

```text
log (full history) ──> stream processor ──> view
recompute = reset offset and replay
```

### What it buys and what it costs

Kappa removes the dual code path: one implementation, one view. The cost is that the log must retain
enough history for any recomputation, which makes the broker the system of record and inflates its
storage. If a full recomputation needs a year of history, the log must hold a year of history.

### The practical middle

The pragmatic rule is a hybrid: batch for the historical, large recomputations where Spark on Parquet
is far cheaper; streaming only for the fresh slice. Full Kappa is for systems whose value is freshness
end to end, like a real-time analytics product, not a citation corpus.

## 6. Exactly-Once and Ordering

### The two costs streaming charges

Streaming charges two costs batch does not. Ordering: events arrive out of order across partitions, and
a window must know when it is complete. Exactly-once: a crash mid-processing must not double-count or
drop an event.

### Why they are hard

Out-of-order events need watermarks — a signal of "no older events will arrive" — and watermarks trade
latency against completeness. Exactly-once needs the engine to write state and output atomically with
its checkpoint, which is exactly the checkpointing discipline of Data Engineering 04, applied
continuously.

### The lesson that carries over

The properties that made batch safe — idempotency and checkpointing — are not optional in streaming;
they are the minimum bar to stand on. A streaming job without checkpoints is a batch job that never
finishes and cannot be resumed.

## 7. Choosing for Our Systems

### Athar: batch

The corpus is bounded and changes rarely. Ingest is a batch job triggered by a new or corrected book,
and the passage table is a batch view. Streaming would add ordering and exactly-once machinery for no
freshness gain.

### DevMate telemetry: the streaming candidate

Usage counts, cache hits, and cost per request are naturally a live feed. If a dashboard needs
near-real-time cost, that slice becomes a Kappa-style stream: an event log plus a Flink or Kafka
Streams aggregation. The corpus and the telemetry live on opposite sides of the boundary, and that is
correct, not a contradiction.

### The exit-test connection

The roadmap's data-engineering bar is a pipeline that can be re-run safely. Batch delivers that
directly; streaming delivers it only if the log is replayable and the job checkpoints. Choosing batch
where bounded is how you keep re-run safety cheap.

## Real-World Application

- Scheduling the Athar corpus ingest as a nightly Airflow/Prefect DAG whose three stages are the
  extract-transform-load functions from Data Engineering 01.
- Running a full recomputation in Spark against the Parquet corpus when the normalization rules change.
- Streaming DevMate usage events through Kafka into a Flink window that feeds a cost dashboard.
- Choosing Kappa for the telemetry slice only, keeping the corpus on batch, rather than forcing one
  architecture onto both.

## Common Mistakes

1. **Streaming a bounded source.** Ordering and exactly-once paid for a corpus that never needed them.
2. **Conflating the orchestrator and the engine.** Airflow schedules; Spark computes; both are needed.
3. **Lambda's two code paths drifting apart.** The batch and speed views disagree at the seam.
4. **Kappa without log retention.** A recomputation that needs history the log no longer holds.
5. **Ignoring ordering and exactly-once.** A streaming job that double-counts on retry.
6. **No checkpointing.** A streaming job that cannot resume from a crash.

## Key Takeaways

1. Batch for bounded sources and daily freshness; stream only the latency-bound slice.
2. Orchestrators schedule and order; engines spread compute; they are different jobs.
3. Brokers give an ordered, replayable log; the log is what makes streaming recoverable.
4. Lambda merges a correct batch view with a fresh speed view at the cost of two code paths.
5. Kappa uses one stream and reprocesses by replay, but the log must retain the history.

## Self-Check Questions

1. What two facts decide batch versus streaming, and why is batch the default?
2. Why is the broker's replayable log the foundation of streaming recovery?
3. What is the single most expensive cost of Lambda architecture?
4. Under what condition does Kappa architecture fail, and why?
5. Why does streaming still need the idempotency and checkpointing of earlier lectures?

## Further Reading / Connections

- Data Engineering 01 (ETL) — the stage-level batch-versus-stream decision.
- Data Engineering 03 (idempotency) and 04 (checkpointing) — the correctness streaming assumes.
- Data Engineering 07 (Parquet and object storage) — the batch engine's read path.
- Data Engineering 13 (feature pipelines) — where streaming aggregation meets features.
- `projects/04-ai-engineering/devmate/src/devmate/obs/` — the cost ledger this feeds.
