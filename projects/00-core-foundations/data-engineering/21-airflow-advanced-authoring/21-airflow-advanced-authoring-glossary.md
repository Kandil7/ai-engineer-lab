# Data Engineering 21: Airflow Advanced Authoring — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Dynamic task mapping | Fan-out over runtime data with `.expand()` | one task per golden case |
| `.collect()` | Gather mapped results into a list | feed the gate task |
| Task group | Visual/logical bundle of tasks | group ingest steps |
| Loop | Mapped instances with per-iteration context | per-book reindex |
| DAG result | Published outcome of a Dag run | Hit@5 summary |
| Asset | Typed dataset with URI; schedule target | `athar://passages` |
| Asset partition | Per-partition consumer run | reindex one book |
| Timetable | Pluggable scheduling rule | business-day calendar |
| Event-driven scheduling | Run on external events (Kafka, files) | ingest on file arrival |
| Deferrable operator | Suspends and hands wait to triggerer | long-poll sensor |
| Trigger | Async watcher run by the triggerer | file-arrival trigger |
| Params schema | JSON-schema validation of trigger params | backfill days 1..30 |
| Serialization | Dag to JSON for DB and cross-process use | XCom values |
| Hook | Client built on a connection | QdrantHook |
| Dynamic Dag | Dag generated at parse time from config | one Dag per tenant |
| YAML Dag | Declarative Dag definition | simple stable pipelines |

---

## Alphabetical Glossary

### Asset

**Definition:** A typed dataset with a URI that producers emit events for and consumer
Dags schedule on. States the data dependency in code.

**Example:**
```python
@task(outlets=[Asset("athar://passages")])
def build_passages(): ...
```

**Related concepts:** Asset partition, Timetable

---

### Collect

**Definition:** Gather the results of a mapped task into a list so a downstream task
can consume them as a single value.

**Example:**
```python
scores = run_case.expand(case=cases)
gate(scores.collect())
```

**Related concepts:** Dynamic task mapping, Task group

---

### Deferrable operator

**Definition:** An operator that, on execution, suspends the task via `self.defer()`
and lets the triggerer watch the condition, freeing the worker slot.

**Example:**
```python
self.defer(trigger=FileTrigger(path="done"), method="resume")
```

**Related concepts:** Trigger, Triggerer (topic 20)

---

### Dynamic Dag

**Definition:** A Dag generated at parse time from configuration or a query. Must stay
deterministic and cheap because parse-time code runs on every scheduler cycle.

**Example:**
```python
for tenant in tenants:
    build_dag(tenant)
```

**Related concepts:** Serialization, Dag bundle (topic 20)

---

### Dynamic task mapping

**Definition:** Fan-out over runtime data: `.expand()` creates one task instance per
item and `.collect()` gathers results. The count is decided at runtime, not parse time.

**Example:**
```python
run_case.expand(case=fetch_cases())
```

**Related concepts:** Collect, Loop

---

### Event-driven scheduling

**Definition:** Scheduling a Dag on external events (Kafka, file arrivals) rather
than on a clock. Pairs with deferrable sensors and assets.

**Example:**
```python
# run when the ingest file lands
```

**Related concepts:** Asset, Timetable

---

### Hook

**Definition:** Python client built on a connection. Tasks ask for a hook by
connection id and never see credentials.

**Example:**
```python
hook = QdrantHook(qdrant_conn_id="qdrant_prod")
```

**Related concepts:** Connection (topic 19), Serialization

---

### Loop

**Definition:** Mapped task iteration with per-iteration context that can be read
downstream; supports skip, retry, and per-iteration failure.

**Example:**
```python
# one mapped instance per book, context carries the book id
```

**Related concepts:** Dynamic task mapping, Task group

---

### Params schema

**Definition:** JSON schema attached to a Dag param for validation at trigger time,
optionally rendering a trigger UI form.

**Example:**
```python
params = {"backfill_days": Param(7, type="integer", minimum=1, maximum=30)}
```

**Related concepts:** Param (topic 19), Serialization

---

### Serialization

**Definition:** Converting a Dag to JSON for storage and cross-process use. Custom
objects need a serializer; XCom values must be serializable.

**Example:**
```python
# non-serializable XCom value fails at the task boundary
```

**Related concepts:** XCom (topic 19), Dynamic Dag

---

### Task group

**Definition:** Bundle of tasks for visual grouping and group-level dependencies.
Layout and dependency sugar, not execution isolation.

**Example:**
```python
with TaskGroup("ingest"):
    extract() >> transform() >> load()
```

**Related concepts:** Dynamic task mapping, Loop

---

### Timetable

**Definition:** Pluggable scheduling rule implementing the timetable interface: data
interval plus next run date. Covers business days and custom calendars.

**Example:**
```python
schedule = BusinessDayTimetable()
```

**Related concepts:** Event-driven scheduling, Asset

---

### Trigger

**Definition:** Async condition watcher registered by a deferrable operator and run
by the triggerer process.

**Example:**
```python
class FileTrigger(BaseTrigger): ...
```

**Related concepts:** Deferrable operator, Triggerer (topic 20)

---

### YAML Dag

**Definition:** Declarative Dag definition in YAML, supporting code tasks for Python
snippets. Fits simple, stable pipelines owned by non-Python teams.

**Example:**
```yaml
# dag_id, schedule, tasks, dependencies in YAML
```

**Related concepts:** Non-Python task SDK, Dynamic Dag

---

## Related Concepts

- **Idempotency** (topic 03): dynamic fan-out and backfill stand on it.
- **Pools** (topic 20): bound mapped-task fan-out against external systems.

## Key Takeaways

1. `.expand()` decides fan-out at runtime; `.collect()` gathers results.
2. Assets state data dependencies in code and combine with time schedules.
3. Deferrable operators free worker slots for long waits.
4. Params schemas prevent bad triggers.
5. Parse-time code runs every cycle; keep it cheap and deterministic.
6. TaskFlow functions stay pytest-testable.
