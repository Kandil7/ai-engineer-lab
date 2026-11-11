# Data Engineering 20: Airflow Execution and Operations

> **Pinned reference:** Apache Airflow 3.4.0 stable documentation
> (<https://airflow.apache.org/docs/apache-airflow/stable/index.html>). Concepts are
> Airflow's; the through-line is this repo's DevMate pipeline.

## Topic Overview

A Dag defines what runs. Operations decides whether it runs reliably. The difference
between a demo and a production scheduler is everything in this lecture: the
architecture (scheduler, dag processor, workers, triggerer, API server, metadata
database), executors and how tasks actually execute, concurrency controls (parallelism,
pools, priority weights), retries and SLAs, deferrable operators at scale, deployment
and monitoring, security, and the Airflow 3 deltas that reshape all of it.

The through-line is DevMate again. Topic 19 scheduled the daily ingest loop on one
machine. This lecture asks what changes when the loop must run every day for a year:
which executor, how many parallel tasks, what happens when the LLM task hangs, who gets
paged when Hit@5 regresses, and how the pipeline survives a scheduler restart.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Name the Airflow components and what each owns.
2. Choose an executor from the workload, with reasons.
3. Bound concurrency with parallelism, pools, and priority weights.
4. Configure retries, timeouts, and SLAs that match failure modes.
5. Decide when a sensor should be deferrable and what the triggerer costs.
6. List the pieces of a production deployment and how failure is detected.
7. Describe the Airflow 3 shifts: Task SDK, Dag bundles, public interface.

## Prerequisites

- Data Engineering 19 (Dag orchestration).
- Data Engineering 15 (storage and databases) for the metadata database discussion.
- DevOps Docker basics for the deployment section.

---

## 1. The Architecture

### The components

Airflow 3 splits the system into cooperating processes:

```text
scheduler:    decides what to run next (the brain)
dag processor: parses Dag files into the metadata database
executor:     dispatches scheduled task instances to workers
workers:      execute the tasks
triggerer:    watches conditions for deferrable tasks
API server:   serves the UI and the stable REST API
metadata DB:  Postgres/MySQL, the single source of state
```

### Why the split matters

Each component scales and fails independently. The scheduler can restart without
losing task state because state lives in the database, not in memory. A worker crash
loses one task instance, which retries. This is the same lesson as the DevMate
structural splits: separate responsibilities so failure is containable.

### Task execution flow

A task instance goes: scheduled by the scheduler, dispatched by the executor, executed
by a worker, state written back to the database. Every state transition is a database
row, which is why the UI can show history and why reprocessing is possible.

## 2. Executors

### The spectrum

- **LocalExecutor**: tasks run as subprocesses on one host. Simple, no broker, one
  point of failure. Right for a single-machine DevMate loop.
- **CeleryExecutor**: workers across machines with a message broker (Redis/RabbitMQ).
  The classic scale-out choice, with broker operations added.
- **KubernetesExecutor**: each task gets its own pod, its own image, its own
  resources. Maximum isolation and autoscaling, most moving parts.

### Multiple executors

Airflow can run several executors concurrently and route tasks by executor config on
the task or Dag. A common pattern: cheap Python tasks on LocalExecutor, heavy LLM or
GPU tasks on KubernetesExecutor.

### Choosing

The decision inputs are: task resource variance, isolation requirements, and how much
operations budget exists. A homogeneous, low-volume loop stays local. Heterogeneous
resource needs (a 2 GB reindex beside a GPU eval) push toward Kubernetes. Do not adopt
Celery for a workload with three tasks a day.

## 3. Concurrency Control

### The knobs

- `max_active_runs_per_dag`: how many Dag runs of one Dag may run concurrently.
- `max_active_tasks_per_dag`: the Dag-wide task cap.
- `parallelism` (core config): the executor-wide default.
- **Pools**: named slot limits shared across Dags. Two slots for the Qdrant pool means
  at most two tasks touch Qdrant at once, whatever Dag they belong to.
- **Priority weights**: when slots are scarce, higher weight runs first.

### Why pools matter most

Pools are the only control that protects an external system from the scheduler
itself. Without a pool, one backfill of fifty parallel ingest tasks can saturate
Qdrant. The pool is the throttle between the orchestrator and its downstream services,
and it is set once, in the UI or by migration, not per Dag.

### The DevMate mapping

`qdrant` pool with two slots; `llm` pool with one slot because the eval gate is the
rate-limiting step anyway; ingest priority above reporting tasks.

## 4. Failure Semantics

### Retries

Per-task `retries` with `retry_delay`, optionally exponential via `retry_exponential_backoff`.
Set retries on tasks whose failures are transient (network, service warm-up) and zero
on tasks whose failures are bugs. A retry on a logic error just delays the same crash
three times.

### Timeouts

`execution_timeout` bounds a task's runtime. It is the antidote to the hung LLM call:
without it, one stuck request holds a worker slot indefinitely and the queue backs up
silently.

### SLAs

SLAs alert when a Dag or task misses its deadline, separate from task failure. The
eval gate finishing at noon instead of 06:00 is not an error, but it is an operational
event someone must know about.

### The pairing rule

Every retry needs a timeout, because a task that can hang must not retry into another
hang, and every timeout needs a decision about retries. Configure them together or the
behavior under failure is accidental.

## 5. Deferrable Operators in Production

### The cost model

A deferrable task releases its worker slot and hands the condition to the triggerer.
The triggerer is a single long-running process that can watch thousands of conditions.
The economics: workers are the scarce resource; the triggerer is cheap waiting.

### When to defer

Sensors waiting hours, long-polling external jobs, anything where the wait exceeds a
few minutes. The mode='reschedule' middle ground releases the slot only between pokes
and is fine for short waits with frequent checks.

### The operational cost

The triggerer becomes part of the failure surface: if it dies, deferred tasks stall
quietly. Run it with the same monitoring weight as the scheduler. This is the hidden
price of deferrable mode: moving waiting from workers to a process means that process
is now load-bearing.

## 6. Production Deployment

### The database

Postgres is the standard metadata backend. SQLite is development only. The database
is the system's memory: back it up, monitor it, and treat schema migrations as
deploy-time work (Airflow runs them on upgrade).

### Deployment shape

Multi-node: at least two schedulers and two API servers for redundancy, workers scaled
by load, one triggerer per pair. Container images come from the official production
image or the Helm chart for Kubernetes. Dag files arrive by git sync: Dag bundles in
Airflow 3 make the source of Dags a configured, monitored input rather than a shared
directory.

### Logging and monitoring

Tasks log per attempt, shipped centrally so a rerun's logs survive the worker that
died. Airflow emits metrics (statsd/Prometheus): scheduler heartbeat, task counts, pool
occupancy, queue depth. Health endpoints exist for both API server and scheduler.
Callbacks (`on_failure_callback`) route task failures to notifications.

### What gets paged

The failure signal that matters: scheduler heartbeat lost, task failure rate above
baseline, pool saturation, and SLA misses. Dashboard numbers without thresholds are
decoration; each of these four needs a threshold and an owner.

## 7. Security

### The model

Connections encrypt secrets at rest in the metadata database; the auth manager controls
who sees which Dags (RBAC); the Airflow 3 multi-team mode scopes resources per team.
Secrets backends (Vault, AWS Secrets Manager) move credentials out of the metadata
database entirely for regulated environments.

### The Dag-file trust boundary

Dag files execute arbitrary Python with the scheduler's privileges. Write access to
the Dag bundle is production access; gate it like a deploy, not like a wiki.

## 8. Airflow 3 Deltas

### What changed

- **Task SDK**: `airflow.sdk` decouples task authoring from the core; non-Python task
  SDKs and YAML Dags are possible.
- **Dag bundles**: Dags come from declared sources (git, custom importers) with
  versioning awareness, not one flat folder.
- **Public interface**: the documented extension surface for operators, plugins, UI,
  and executors, replacing incidental internals.
- **Deferrable and resumable tasks**: durable execution matures beyond sensors.
- **Assets**: the data-driven scheduling model (topic 19), now first-class.

### Why it matters here

The Airflow 2 knowledge that survives is the model: Dags, intervals, retries, pools.
The internals that changed are exactly the ones you should have been treating as
implementation detail. Learn the public interface; ignore internals you would have
been hard-coding against.

## Real-World Application

- DevMate's loop graduates from LocalExecutor on the workstation to CeleryExecutor
  only when a second workload competes for the machine; until then local is correct.
- A `qdrant` pool (2 slots) and an `llm` pool (1 slot) bound the pressure on both
  services during backfills.
- The eval task gets `execution_timeout` of 30 minutes and 2 retries; the ingest task
  gets 0 retries because a mid-run crash is a bug, and idempotency makes the manual
  re-run safe.
- Postgres for metadata, two scheduler replicas, logs shipped off-host, and a page on
  scheduler heartbeat loss or SLA miss.

## Common Mistakes

1. **Unbounded retries on logic errors.** The same bug crashes three times, slower.
2. **No execution_timeout.** One hung LLM call holds a slot all night.
3. **No pools.** A backfill saturates Qdrant and everything downstream of it.
4. **Retries without timeouts, timeouts without retry decisions.** Failure behavior
   under stress is then accidental.
5. **Treating the triggerer as set-and-forget.** Deferred tasks stall silently when it
   dies; monitor it like the scheduler.
6. **SQLite in production.** The metadata database is the system's memory; SQLite
   cannot take concurrent scheduler writes.
7. **Paging on dashboard colors instead of thresholds.** Numbers without owners are
   decoration.

## Key Takeaways

1. State lives in the metadata database; components are replaceable because of it.
2. Executor choice follows resource variance and isolation needs, not fashion.
3. Pools are the throttle between the orchestrator and its external systems.
4. Retries, timeouts, and SLAs are configured as one decision, not three.
5. Deferrable waiting trades worker slots for a load-bearing triggerer.
6. Airflow 3's deltas confirm the rule: depend on the model, not the internals.

## Self-Check Questions

1. Which component decides what runs next, and where does it keep that decision?
2. What workload property pushes you off LocalExecutor, and to which executor?
3. How does a pool protect Qdrant from a fifty-task backfill?
4. Why must a retry always be paired with a timeout?
5. What exactly breaks when the triggerer dies, and why is it silent?
6. What makes Dag-file write access equivalent to production access?

## Further Reading / Connections

- Data Engineering 19 (DAG orchestration) — the authoring half this operationalizes.
- Data Engineering 15 (storage and databases) — the metadata database and its care.
- DevOps Docker lectures (`projects/06-devops/docker/`) — the deployment substrate.
- Airflow 3.4 docs: Core Concepts (Executor, Resumable Tasks), Administration and
  Deployment (Production Deployment, Logging & Monitoring, Pools, Cluster Policies),
  and Best Practices.
