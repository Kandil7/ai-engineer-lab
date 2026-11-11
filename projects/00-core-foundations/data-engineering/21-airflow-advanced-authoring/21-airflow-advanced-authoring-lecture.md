# Data Engineering 21: Airflow Advanced Authoring

> **Pinned reference:** Apache Airflow 3.4.0 stable documentation
> (<https://airflow.apache.org/docs/apache-airflow/stable/index.html>). Concepts are
> Airflow's; the through-line is this repo's DevMate pipeline.

## Topic Overview

Topic 19 covered the authoring spine: Dags, TaskFlow, sensors, XCom, scheduling.
This lecture covers the advanced authoring surface that makes a Dag express real
workloads: dynamic task mapping (fan-out over data), loops, task groups, assets and
asset-aware scheduling in depth, timetables and event-driven scheduling, deferrable
operators and how to write one, serialization, custom connections and hooks,
non-Python task SDKs and YAML Dags, dynamic Dag generation, and params with JSON
schema and trigger UI forms.

The through-line is DevMate's eval matrix. The offline eval runs over a set of
golden cases; each case is a task instance that must fan out, collect results, and
gate the run. That is dynamic task mapping plus a result task, and it is the pattern
this lecture teaches.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Fan out a task over a runtime list with `.expand()` and collect with `.collect()`.
2. Choose between mapped tasks, loops, and task groups for fan-out.
3. Schedule a Dag on an asset update and combine time and asset schedules.
4. Write a custom timetable and an event-driven schedule.
5. Explain how deferrable operators work and when to write one.
6. Validate params with a JSON schema and render a trigger form.
7. Decide when YAML Dags or a non-Python SDK fit.

## Prerequisites

- Data Engineering 19 (Dag orchestration) and 20 (execution).
- Comfort with Python decorators and type hints.

---

## 1. Dynamic Task Mapping

### The problem

A task that must run once per item in a list: one ingest per book, one eval per
golden case. Writing the loop in Python at parse time produces a fixed number of
tasks and breaks when the list changes at runtime. Dynamic task mapping creates one
task instance per item at runtime, from data produced by an upstream task.

### `.expand()` and `.collect()`

```python
@task
def fetch_cases() -> list[str]:
    return load_golden_cases()


@task
def run_case(case: str) -> float:
    return score(case)


@task
def gate(scores: list[float]) -> None:
    assert all(s >= 0.7 for s in scores)


cases = fetch_cases()
scores = run_case.expand(case=cases)
gate(scores.collect())
```

`.expand()` fans out; `.collect()` gathers the mapped results into a list for the
downstream task. The number of instances is decided when `fetch_cases` runs, not
when the Dag file is parsed.

### Limits and placement

Mapped tasks have a configurable max (operator and Dag level) to protect downstream
systems. Mapping over a task group is supported for layout. Templated fields and
mapped arguments interact: a templated field is rendered per mapped instance.

### When not to map

Mapping is for homogeneous fan-out. Heterogeneous steps with different operators,
different retries, or different executors stay as explicit tasks. Mapping a single
heavy task fifty times is a backfill hazard: use pools (topic 20).

## 2. Loops, Task Groups, and the DAG Result

### Loops

Airflow loops (`@task` with iteration) create mapped instances with a loop context
that downstream tasks can read. Use them when each iteration needs context from its
position, or when data must pass between iterations. Loops support failure, skip,
and retry semantics per iteration, and an iteration's result can be used outside the
loop.

### Task groups

A task group bundles related tasks for visual grouping and group-level dependencies.
It is layout and dependency sugar, not execution isolation; the tasks inside still
run on workers under the usual concurrency rules.

### The DAG result

A result task marks the Dag's outcome and is retrievable after the run. Use it to
publish a single summary (the eval Hit@5) that downstream consumers and the UI can
read without scraping task logs.

## 3. Assets and Asset-Aware Scheduling in Depth

### What an asset is

An asset is a typed dataset with a URI. A producer task declares `outlets=[Asset(...)]`
and emits an event when it finishes; a consumer Dag declares `schedule=[Asset(...)]`
and runs on that event. The pipeline now states its data dependency in code.

### Asset-aware scheduling

A Dag can schedule on multiple assets, with conditional expressions (all-of, any-of),
and can combine asset and time-based schedules. Asset events carry metadata the
consumer can read, and cross-team filtering (producer_teams) scopes events in
multi-team deployments.

### Asset partitions

Partitions let a consumer run per partition of the asset rather than per event, which
is how a per-book reindex avoids reprocessing the whole corpus when one book
changes.

### When to use assets over cron

If the real trigger is "the data changed", schedule on the asset. Cron is for
"every Tuesday at 03:00" and nothing else. Mixing both is supported and common: a
daily fallback plus an asset trigger for freshness.

## 4. Timetables and Event-Driven Scheduling

### Timetables

A timetable is a pluggable scheduling rule for anything cron cannot express:
business days, custom calendars, `@every` presets. Built-in timetables cover most
needs; a custom one implements the timetable interface and is registered. Timetables
define both the data interval and the next run date.

### Event-driven scheduling

Airflow 3 supports scheduling on external events: Kafka topics, file arrivals, and
other triggers. This is the path from "run on a clock" to "run when something
happens", and it pairs with deferrable sensors and assets.

### Time zones

Dags can be time-zone aware; the web UI shows local time. Always set the timezone
explicitly on the schedule and on `start_date` to avoid silent off-by-one intervals
around daylight-saving transitions.

## 5. Deferrable Operators and Triggers

### How they work

A deferrable operator, on execution, calls `self.defer(trigger=..., method=...)` and
returns. The task instance is suspended and the triggerer watches the condition; when
it fires, the named method on the operator runs to completion. The worker slot is
free for the whole wait.

### Writing one

Subclass an operator, implement `execute()` to defer when waiting, implement the
resume method, and register a trigger. The trigger is a separate class that
implements the async wait and serializes its state so the triggerer can resume after
a restart.

### Mode='reschedule' versus deferrable

Mode='reschedule' releases the slot only between pokes and is fine for short waits
with frequent checks. Deferrable is for long waits and needs the triggerer to be
running and monitored. The choice is a wait-duration decision, not a style one.

## 6. Params, Serialization, and Connections

### Params with schema

Params accept a JSON schema for validation and can render a trigger UI form. A
backfill count param validated as an integer between 1 and 30 prevents a bad trigger
from reprocessing a year of data.

### Serialization

Dag serialization converts the Dag to JSON for the database and for cross-process
use. Most Airflow objects serialize; custom objects need a serializer. Serialization
settings control which. The practical limit: anything stored in XCom or in the Dag
must be serializable, which is another reason XCom stays metadata.

### Connections and hooks

Connections store credentials and endpoints; hooks are the clients built on them.
Custom connections register a connection type and a hook. Tasks ask for a hook by
connection id and never see credentials. This is the same boundary as `.env` handling
in the DevMate gate.

## 7. Dynamic Dags and Non-Python Authoring

### Dynamic Dag generation

Dags can be generated at parse time from a config file or a database query. The
generated Dags are first-class Dags with their own schedule and history. Keep
generation deterministic and cheap: parse-time code runs on every scheduler cycle.

### Non-Python task SDKs

Airflow 3's Task SDK allows compiled-language SDKs (Go, Rust, Java) and YAML Dags.
YAML Dags define tasks and scheduling declaratively and support code tasks for
Python snippets. Use them for simple, stable pipelines owned by non-Python teams;
use Python Dags when logic, testing, or dynamic generation matters.

### Packaging Dags

Dags arrive via Dag bundles (git sync, custom importers) in Airflow 3. Packaging
them as Python packages with a proper structure keeps imports predictable and
`.airflowignore` keeps non-Dag files out of parsing.

## 8. Testing Dags in Depth

### The layers

Import-error detection in CI, `dag.test()` to execute the Dag locally in one process,
unit tests for task functions, and integration tests against real services. TaskFlow
functions are plain Python, so the bulk of the logic is testable without Airflow.

### What to assert

Assert the graph shape (task count, dependencies), the params schema, and the task
function outputs. Assert that a Dag with a bad import fails to parse. These are the
cheap tests; the expensive ones are integration tests against Qdrant and the LLM.

## Real-World Application

- DevMate's eval matrix: `run_case.expand(case=fetch_cases())` fans out one task per
  golden case, `.collect()` feeds the gate, and the gate task fails the run when
  Hit@5 drops below 1.0.
- Schedule the nightly eval on the asset emitted by the ingest Dag, plus a weekly
  cron fallback, so a missed asset event still triggers a run.
- Pass the collection name and index path between tasks by XCom; never the passages.
- Validate the backfill-day param as 1..30 with a JSON schema so a bad trigger cannot
  reprocess a year.

## Common Mistakes

1. **Mapping a single heavy task hundreds of times.** Fan-out amplifies load; bound it
   with pools and max_active_tis_per_dag.
2. **Parse-time work in dynamic Dags.** A database query in the Dag file runs on every
   scheduler cycle.
3. **Cron when the trigger is data.** If the step should run when the asset updates,
   schedule on the asset.
4. **Deferring without monitoring the triggerer.** Deferred tasks stall silently.
5. **Untyped params.** A free-form backfill count is a foot-gun; validate it.
6. **Shipping unserializable objects in XCom.** They fail at task boundaries, not at
   authoring time.

## Key Takeaways

1. Dynamic mapping decides fan-out at runtime from upstream data.
2. Assets state data dependencies in code and combine with time schedules.
3. Deferrable operators trade worker slots for a monitored triggerer.
4. Params with schemas prevent bad triggers.
5. Parse-time code runs every cycle; keep it cheap and deterministic.
6. TaskFlow functions stay pytest-testable, which is where most testing belongs.

## Self-Check Questions

1. When is `.expand()` the right tool, and when are explicit tasks better?
2. How does an asset-scheduled Dag differ from a cron-scheduled one, and can they
   combine?
3. What does a deferrable operator do on execution, and what must be monitored?
4. Why must parse-time code in a dynamic Dag be cheap and deterministic?
5. What breaks if an XCom value is not serializable?
6. What does a params JSON schema buy you at trigger time?

## Further Reading / Connections

- Data Engineering 19 (Dag orchestration) — the authoring spine this extends.
- Data Engineering 20 (execution and operations) — pools, executors, and the triggerer.
- Airflow 3.4 docs: Authoring and Scheduling (Mapped tasks, Loops, Asset Definitions,
  Timetables, Event-Driven Scheduling, Deferrable Operators & Triggers, Connections &
  Hooks, DAG Result, Non-Python Task SDKs, Writing Dags in YAML), Core Concepts
  (Tasks, Params, XComs), and Testing a Dag.
