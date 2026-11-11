# Data Engineering 19: DAG Orchestration — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Dag | Workflow defined as Python: schedule, tasks, dependencies | `devmate_ingest` |
| Dag run | One execution of a Dag over one interval | nightly run at 03:00 |
| Logical date | Start of the interval a Dag run processes | `2026-03-04T03:00` |
| Task | One unit of work in a Dag | ingest, reindex, eval |
| Operator | Template for one kind of work | `BashOperator` |
| TaskFlow | Decorator API turning functions into tasks | `@task` |
| Sensor | Task that waits for a condition | wait for the eval gate |
| XCom | Small metadata passed between tasks | index path, row count |
| Variable | Global key-value configuration | `QDRANT_URL` |
| Param | Per-run configuration with schema | backfill day count |
| Connection | Stored credentials for an external system | `qdrant_prod` |
| Asset | Typed dataset with URI, schedule target | `athar://passages` |
| Catchup | Scheduler fills every missed interval | `catchup=False` |
| Backfill | Deliberate re-run over a historical range | reprocess last week |
| Timetable | Pluggable scheduling rule | business-day calendar |

---

## Alphabetical Glossary

### Asset

**Definition:** A typed dataset with a URI that producers emit events for and
consumer Dags schedule on. The Airflow 3 successor to datasets; states the data
dependency in code.

**Example:**
```python
@task(schedule=[Asset("athar://passages")])
def reindex(): ...
```

**Related concepts:** Schedule, Sensor

---

### Backfill

**Definition:** Deliberate re-execution of a Dag over a historical interval,
honoring dependencies. Safe only when the pipeline is idempotent.

**Example:**
```python
# fix a transform, backfill the last 7 days
```

**Related concepts:** Catchup, Idempotency (topic 03)

---

### Catchup

**Definition:** Scheduler behavior that fills every missed interval between
`start_date` and now. `catchup=False` runs only the latest interval.

**Example:**
```python
with DAG(dag_id="devmate_ingest", schedule="0 3 * * *", catchup=False):
```

**Related concepts:** Backfill, Logical date

---

### Connection

**Definition:** Stored, encrypted credentials and endpoint for an external system,
referenced by id. A hook is the client built on it.

**Example:**
```python
hook = QdrantHook(qdrant_conn_id="qdrant_prod")
```

**Related concepts:** Variable, Hook

---

### Dag

**Definition:** Directed acyclic graph; Airflow's model of a workflow: schedule,
tasks, dependencies, callbacks. Parsed, never executed, as a file.

**Example:**
```python
with DAG(dag_id="devmate_ingest", schedule="0 3 * * *"):
    ...
```

**Related concepts:** Dag run, Task

---

### Dag run

**Definition:** One execution of a Dag over one interval, with its own state, logs,
and identity used by retries, backfills, and the UI.

**Example:**
```python
# grid view: one column per Dag run
```

**Related concepts:** Logical date, Catchup

---

### Deferrable

**Definition:** Sensor mode that suspends the task and lets the triggerer watch the
condition, so a long wait holds no worker slot.

**Example:**
```python
FileSensor(task_id="wait", filepath="done.txt", deferrable=True)
```

**Related concepts:** Sensor, Triggerer

---

### Logical date

**Definition:** The start of the schedule interval a Dag run processes. The
identity that ties a run to the data window it covers.

**Example:**
```python
# daily run at 03:00 on Mar 5 processes the interval ending then
```

**Related concepts:** Dag run, Backfill

---

### Operator

**Definition:** Template for one kind of task work: Bash, Python, or a provider
integration. Instantiating it creates a task.

**Example:**
```python
up = BashOperator(task_id="start_qdrant", bash_command="docker compose up -d qdrant")
```

**Related concepts:** TaskFlow, Task

---

### Param

**Definition:** Per-run configuration passed at trigger time, optionally validated
against a JSON schema. Configures the run, not the deployment.

**Example:**
```python
# trigger with {"since_days": 7}
```

**Related concepts:** Variable, Dag run

---

### Sensor

**Definition:** A task that polls a condition until it holds or times out: a file, a
row, another Dag run. Modes: poke, reschedule, deferrable.

**Example:**
```python
@task.sensor
def eval_gate(): ...
```

**Related concepts:** Deferrable, Task

---

### TaskFlow

**Definition:** The `@task` decorator API that turns plain functions into tasks,
inferring dependencies from argument passing and testing with pytest.

**Example:**
```python
@task
def ingest() -> str: ...
```

**Related concepts:** Operator, XCom

---

### Timetable

**Definition:** Pluggable scheduling rule beyond cron and timedelta: business days,
custom calendars, `@every` presets.

**Example:**
```python
schedule = CronDataIntervalTimetable("0 3 * * 1-5", timezone="UTC")
```

**Related concepts:** Schedule, Cron

---

### Triggerer

**Definition:** Airflow process that runs deferred triggers, watching conditions for
deferrable sensors without holding worker slots.

**Example:**
```python
# a 3-hour deferrable sensor costs the triggerer, not a worker
```

**Related concepts:** Deferrable, Executor (topic 20)

---

### Variable

**Definition:** Global key-value configuration read by tasks from the metadata
database or environment. Configures the deployment.

**Example:**
```python
url = Variable.get("QDRANT_URL")
```

**Related concepts:** Connection, Param

---

### XCom

**Definition:** Cross-communication: small metadata passed between tasks through the
metadata database. Never for data; large results go through storage.

**Example:**
```python
# return the index path, not the passages
```

**Related concepts:** TaskFlow, Asset

---

## Related Concepts

- **Idempotency** (topic 03): the precondition catchup and backfill stand on.
- **Batch versus streaming** (topic 08): Airflow is the batch-side scheduler.
- **Provenance** (topic 06): Dag run identity plus task logs gives pipeline-level
  lineage.

## Key Takeaways

1. Dag file is a definition; the scheduler executes it.
2. TaskFlow functions are plain Python and pytest-testable.
3. XCom is metadata, storage is data.
4. Long waits belong to reschedule or deferrable sensors.
5. Catchup and backfill require idempotency to be safe.
