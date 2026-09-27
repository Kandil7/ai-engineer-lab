# Queues and Workflows Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Queue | Durable buffer decoupling producers from consumers |
| Job | Unit of queued work with identity, payload, attempt count |
| Producer | Component that enqueues jobs (API, importer) |
| Worker | Component that dequeues and executes jobs |
| Ack (acknowledge) | Worker's signal that work is durable and complete |
| At-least-once | Delivery guarantee: a job may run more than once |
| Exactly-once | Guarantee you cannot assume from brokers; design around it |
| Idempotency | Re-running an operation produces the same state (no-ops) |
| Natural key | Business identity used for dedupe (`source_ref`, content hash) |
| Insert-if-absent | Write pattern enforcing idempotency by key |
| Redelivery | Broker resends a job after a crash/timeout before ack |
| Retry | Re-running a failed job |
| Transient error | Temporary failure worth retrying (timeout, 5xx) |
| Permanent error | Failure that will not change on retry (validation) |
| Exponential backoff | Retry delay doubling per attempt |
| Jitter | Randomized delay component preventing retry storms |
| Attempt cap | Max retries before giving up (`max_attempts`) |
| Dead-letter queue (DLQ) | Queue of jobs that exhausted retries or failed permanently |
| Poison message | Job that fails on every attempt (malformed payload) |
| Replay | Re-running DLQ jobs after a fix (safe if idempotent) |
| Bounded in-flight | Cap on concurrently processed jobs |
| Backpressure | Producer slows when workers/queue are saturated |
| Job age | Time a job waits; a latency metric for the queue |
| Queue depth | Number of pending jobs; a capacity metric |
| Workflow | Ordered multi-job pipeline (ingest → embed → index) |
| Job payload contract | The shape of a job's data (see component contracts) |
| Content hash | Hash of text used as natural key for chunk dedupe |
| Storm | Thundering herd of retries hitting a recovered dependency |

---

## Detailed Definitions

### Queue and job
A queue decouples work duration from request latency and survives process death. A job carries `job_id`, `kind`, `payload`, `attempts`, `max_attempts` — identity is what makes retries and DLQ entries actionable.

### At-least-once delivery
The only safe assumption: a worker crash between "work done" and "ack" causes redelivery. Any job may run twice. Exactly-once is a fiction at the broker level; *effectively*-once comes from idempotent handlers.

### Idempotency and natural keys
Handlers must be no-ops on second delivery. Achieved with a natural key (`source_ref`, content hash) and insert-if-absent semantics. The exercise proves: redelivered job, still one row.

### Retry policy
Transient errors retry; permanent errors do not. Exponential backoff with jitter prevents storms; the attempt cap bounds work and routes exhaustion to the DLQ.

### Dead-letter queue
Where jobs land after exhausting retries or failing permanently. It is an operational surface with an owner: inspect, fix data, replay (safe because idempotent), or drop. DLQ depth is a monitored metric.

### Bounded workers and backpressure
`max_in_flight` caps concurrent jobs, bounding memory and propagating backpressure to producers — a fast import cannot starve workers or OOM the process.

### When not to queue
Synchronous user-facing answers, trivial work, or strict global ordering belong inline. The queue is for slow, bursty, survivable work.

### The Athar ingest workflow
`/ingest` enqueues batch jobs; workers normalize, embed, and insert keyed by `(source_ref, chunk_index)`; reruns are no-ops; Postgres remains the source of truth and the index is derived.
