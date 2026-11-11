# Data Engineering 20: Airflow Execution and Operations — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Scheduler | Decides what runs next, state in the metadata DB | heartbeat metric |
| Dag processor | Parses Dag files into the database | parse in CI |
| Executor | Dispatches task instances to workers | Local, Celery, Kubernetes |
| Worker | Process that executes tasks | subprocess or pod |
| Triggerer | Watches deferrable conditions | long sensor waits |
| Metadata DB | Single source of state, Postgres in prod | Dag runs, XComs |
| Pool | Named slot limit shared across Dags | `qdrant` pool, 2 slots |
| Parallelism | Executor-wide task concurrency cap | core config |
| Priority weight | Which task runs first when slots are scarce | ingest > report |
| Retry | Automatic re-execution after failure | 2 retries, 5 min delay |
| Execution timeout | Hard runtime bound per task | 30 min for eval |
| SLA | Deadline alert, separate from failure | eval done by 06:00 |
| Deferrable | Task suspends; triggerer watches | hours-long sensor |
| Callback | Hook on state change | `on_failure_callback` |
| Dag bundle | Declared source of Dag files | git-synced repo |

---

## Alphabetical Glossary

### Callback

**Definition:** Hook invoked on task or Dag state change, such as
`on_failure_callback`, used to route failures to notifications.

**Example:**
```python
task = ingest.override(on_failure_callback=page_oncall)
```

**Related concepts:** Monitoring, SLA

---

### Dag bundle

**Definition:** Airflow 3 mechanism declaring where Dags come from: a git sync, a
custom importer, a local dir. Replaces the flat dags folder assumption.

**Example:**
```yaml
dag-bundles:
  - name: repo
    type: git
```

**Related concepts:** Dag processor, Deployment

---

### Deferrable

**Definition:** Task mode that releases the worker slot and hands the wait condition
to the triggerer. Cheap waiting, at the price of a load-bearing triggerer.

**Example:**
```python
BashSensor(task_id="wait", deferrable=True)
```

**Related concepts:** Triggerer, Sensor (topic 19)

---

### Executor

**Definition:** Component that dispatches scheduled task instances to workers:
LocalExecutor (subprocesses), CeleryExecutor (broker + workers),
KubernetesExecutor (pod per task).

**Example:**
```python
# LocalExecutor: right for a single-machine daily loop
```

**Related concepts:** Worker, Scheduler

---

### Execution timeout

**Definition:** Hard runtime bound per task instance. The antidote to a hung task
holding a worker slot indefinitely.

**Example:**
```python
eval_task = eval.override(execution_timeout=timedelta(minutes=30))
```

**Related concepts:** Retry, SLA

---

### Metadata database

**Definition:** The Postgres (production) or SQLite (development) database holding
all Airflow state: Dag runs, task instances, XComs, connections.

**Example:**
```python
# state lives here, which is why a scheduler restart loses nothing
```

**Related concepts:** Scheduler, Dag run (topic 19)

---

### Parallelism

**Definition:** Executor-wide cap on concurrently running tasks. The Dag-level and
run-level caps sit inside it.

**Example:**
```ini
[core] parallelism = 32
```

**Related concepts:** Pool, Priority weight

---

### Pool

**Definition:** Named set of slots shared across Dags, limiting how many tasks may
touch a resource concurrently. The throttle between scheduler and external systems.

**Example:**
```python
# "qdrant" pool with 2 slots: a backfill cannot saturate Qdrant
```

**Related concepts:** Parallelism, Backfill (topic 19)

---

### Priority weight

**Definition:** Per-task weight deciding queue order when slots are scarce:
higher weights run first.

**Example:**
```python
ingest.priority_weight = 10
report.priority_weight = 1
```

**Related concepts:** Pool, Executor

---

### Retry

**Definition:** Automatic re-execution of a failed task after a delay, with optional
exponential backoff. Right for transient failures, wrong for logic bugs.

**Example:**
```python
task = fetch.override(retries=2, retry_delay=timedelta(minutes=5))
```

**Related concepts:** Execution timeout, Idempotency (topic 03)

---

### Scheduler

**Definition:** The Airflow brain: decides which task instances to run next based on
Dag state, dependencies, and concurrency limits. Restart-safe because state is in
the metadata database.

**Example:**
```python
# monitor: scheduler heartbeat metric
```

**Related concepts:** Metadata database, Executor

---

### SLA

**Definition:** Deadline that, when missed, raises an alert independent of task
success or failure. Late-but-successful is still an operational event.

**Example:**
```python
dag.sla = timedelta(hours=6)  # eval loop done by 06:00
```

**Related concepts:** Execution timeout, Callback

---

### Task SDK

**Definition:** Airflow 3's decoupled task-authoring interface (`airflow.sdk`),
enabling non-Python task SDKs and YAML Dags.

**Example:**
```python
from airflow.sdk import task
```

**Related concepts:** TaskFlow (topic 19), Public interface

---

### Triggerer

**Definition:** Long-running process executing deferred triggers. Thousands of
conditions per process; its death stalls deferred tasks silently.

**Example:**
```python
# monitor the triggerer like the scheduler
```

**Related concepts:** Deferrable, Monitoring

---

### Worker

**Definition:** Process or container that executes a task instance. Scale-out unit
for CeleryExecutor, isolation unit for KubernetesExecutor.

**Example:**
```python
# one worker crash loses one task instance, which retries
```

**Related concepts:** Executor, Retry

---

## Related Concepts

- **Dag orchestration** (topic 19): the authoring half this operationalizes.
- **Idempotency** (topic 03): retries and backfills stand on it.
- **Storage and databases** (topic 15): the metadata database is one more database
  to operate.

## Key Takeaways

1. State lives in the metadata database; components are replaceable because of it.
2. Executor choice follows workload variance and isolation needs.
3. Pools protect external systems from the scheduler's own enthusiasm.
4. Retries, timeouts, and SLAs are one decision about failure, not three.
5. Deferrable waiting makes the triggerer load-bearing; monitor it.
