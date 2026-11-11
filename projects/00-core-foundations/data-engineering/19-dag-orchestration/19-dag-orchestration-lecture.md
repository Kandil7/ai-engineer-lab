# Data Engineering 19: DAG Orchestration

> **Pinned reference:** Apache Airflow 3.4.0 stable documentation
> (<https://airflow.apache.org/docs/apache-airflow/stable/index.html>). Concepts are
> Airflow's; the through-line is this repo's DevMate pipeline.

## Topic Overview

An orchestration scheduler answers one question: what runs, when, in what order, and
what happens when it fails? Cron answers it with a flat list of timers. Airflow answers
it with a Dag: the workflow declared as Python code, with dependencies, retries,
scheduling, and history built in.

This lecture covers the authoring half of Airflow. The Dag model and its parts, the
TaskFlow API, dependencies and control flow, sensors, XCom, variables, params,
connections and hooks, scheduling (cron, timetables, assets), catchup and backfill, and
testing Dags. The running half, executors and production operations, is Data
Engineering 20.

The through-line is DevMate. The daily repo-ingest and RAG-refresh job is a real
scheduled pipeline: start Qdrant, ingest the repo, reindex, run the offline eval, and
gate on the Hit@5 number. Written as a Dag, each of those steps is a task with retries
and counts, the whole run is visible in a UI, and a missed day is caught up
automatically instead of silently skipped.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what a Dag is and how it differs from a script or a cron line.
2. Declare tasks with operators and the TaskFlow API, and wire dependencies.
3. Choose between XCom, variables, and params for passing data.
4. Use sensors, including deferrable mode, for external conditions.
5. Schedule with cron, timedelta, timetables, and assets.
6. Predict what catchup and backfill will run, and when.
7. Test a Dag with dag.test() and unit tests.

## Prerequisites

- Data Engineering 01 (ETL stages) and 03 (idempotency).
- Data Engineering 08 (batch versus streaming).
- Comfortable reading Python decorators.

---

## 1. Why Orchestrate

### The cron problem

A cron line runs a script at a time. It does not chain steps, retry on failure, record
history, backfill missed runs, or show you anything. Every pipeline eventually grows a
second step, then a third, and the cron line becomes a shell script full of `&&` and
prayer.

### The Dag answer

Airflow's answer is workflows as code. A Dag (directed acyclic graph, written "Dag" in
Airflow 3) declares the tasks, the order, and the schedule in Python:

```python
from datetime import datetime

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="devmate_ingest", start_date=datetime(2026, 1, 1), schedule="0 3 * * *"
):
    up = BashOperator(
        task_id="start_qdrant", bash_command="docker compose up -d qdrant"
    )

    @task
    def ingest() -> str: ...

    @task
    def eval() -> float: ...

    up >> ingest() >> eval()
```

The code is versioned, reviewable, and testable like any other code. That is the whole
point: the pipeline stops being an artifact on one server and becomes a unit of
software.

### What you get free

Retries with backoff, per-task history and logs, a UI to trigger and clear runs, missed
runs tracked and backfillable, and dependency-aware scheduling. You would build all of
this badly in a shell script.

## 2. The Dag and Its Parts

### The model

A Dag encapsulates everything needed to execute a workflow: the schedule, the tasks,
the dependencies, the callbacks, and the operational parameters. Nothing executes in
the Dag file itself; parsing the file only builds the model. This is the most important
mental shift: a Dag file is a definition, not a program.

### Dag runs and logical dates

The scheduler creates a Dag run per schedule interval. Each run has a logical date,
the start of the interval it processes. A daily Dag triggered at 03:00 on March 5
processes the interval that ends then. Retries, backfills, and the UI all hang off this
identity: a Dag run is one execution of one interval.

### Catchup

`catchup=True` makes the scheduler fill every missed interval between `start_date` and
now, in order. `catchup=False` runs only the latest interval. For DevMate's ingest,
catchup is wrong: re-ingesting last week's repo adds nothing. For a billing pipeline,
catchup is mandatory: missing a day of invoices is a real loss. The choice is per-Dag
and it is a business decision, not a default.

## 3. Declaring Tasks

### Operators

An operator is a template for one kind of work. `BashOperator` runs a shell command,
`PythonOperator` calls a function, provider packages add hundreds more. Instantiating
an operator in a Dag file creates a task:

```python
hello = BashOperator(task_id="hello", bash_command="echo hello")
```

### TaskFlow

The TaskFlow API turns plain functions into tasks with the `@task` decorator:

```python
@task
def ingest() -> str:
    return run_ingest()


@task
def eval(hit_target: float = 1.0) -> float: ...
```

TaskFlow infers dependencies from argument passing and handles serialization of small
return values via XCom. In Airflow 3 the decorators live in `airflow.sdk`, which is
the Task SDK boundary. Prefer TaskFlow for Python work; use operators when a packaged
integration already exists.

### Dependencies

The `>>` and `<<` operators wire order; a list means fan-out or fan-in:

```python
up >> [ingest(), reindex()] >> eval()
```

Task groups bundle related tasks for layout and group-level dependencies. The graph
must stay acyclic; a cycle is a parse-time error, which is the acyclic in DAG doing
real work.

## 4. Sensors

### What a sensor is

A sensor is an operator that waits for a condition: a file arriving, an API returning
a row, another Dag run finishing. It polls until the condition holds, the timeout
expires, or it is poked out of existence.

### Poke versus reschedule versus deferrable

`mode="poke"` holds a worker slot while polling. `mode="reschedule"` releases the slot
between pokes. A deferrable sensor goes further: it suspends the task entirely and the
triggerer process watches the condition, so a three-hour wait costs no worker at all.
The rule: long waits should never hold a worker slot.

## 5. Data Between Tasks

### XCom

XComs (cross-communications) pass small metadata between tasks: a row count, an
identifier, a path. They live in the metadata database and are the mechanism behind
TaskFlow's return-value plumbing. The rule is strict: XCom is metadata, never data.
Passing a dataframe through XCom serializes it into the database and turns every task
boundary into a bottleneck.

### The alternative

Large data flows through storage: the producer writes to object storage or a table and
XCom carries the reference. DevMate's ingest passes the index path, not the passages.

### Variables and params

Variables are global key-value configuration read by tasks, set in the UI or
environment. Params are per-Dag-run configuration passed at trigger time, with JSON
schema validation available. The split: variables configure the deployment, params
configure the run.

## 6. Connections and Hooks

### The pattern

A connection stores credentials and an endpoint for an external system in the metadata
database, encrypted. A hook is the Python client built on a connection. Tasks never
hard-code hosts or passwords; they ask for a hook by connection id.

### Why it matters

Credentials rotate without a code change, and a leaked Dag file carries no secrets.
This is the same discipline as `.env` handling in the DevMate gate: configuration
outside the artifact.

## 7. Scheduling

### Cron and timedelta

`schedule="0 3 * * *"` is cron, daily at 03:00. `schedule=timedelta(hours=6)` is
interval-based, relative to the Dag's start. Both create time-based data intervals.

### Timetables

A timetable is a pluggable scheduling rule for anything cron cannot express: business
days, custom calendars. `@every`, cron presets, and `CronDataIntervalTimetable` cover
most needs before writing one.

### Assets

Assets are typed datasets with URIs that producers emit events for and consumers
schedule on. A Dag with `schedule=asset` runs when the asset updates, regardless of
time. This is the Airflow 3 answer to "run when the data changed", and it replaces the
old datasets concept:

```python
from airflow.sdk import Asset


@task(outlets=[Asset("athar://passages")])
def build_passages(): ...


@task(schedule=[Asset("athar://passages")])
def reindex(): ...
```

The pipeline now states its data dependency in code: reindex runs when passages are
rebuilt, and the interval between them can be zero.

## 8. Backfill

### What it does

Backfill re-runs the Dag over a historical interval, honoring dependencies. It is the
operational twin of catchup: catchup is automatic for missed intervals, backfill is
deliberate, over a range you choose, for a fix or a rebuild.

### The precondition

Backfill is safe only when the pipeline is idempotent (Data Engineering 03). A
non-idempotent ingest backfilled three times triples the data. This is why
idempotency precedes orchestration in this track: the scheduler amplifies whatever
discipline the pipeline has, good or bad.

## 9. Testing Dags

### The layers

Airflow recommends: Dag-level import errors caught in CI, `dag.test()` to execute the
Dag locally in one process, unit tests for task functions, and integration tests
against real services. The task functions are plain Python, so the TaskFlow style pays
twice: it is testable with pytest without Airflow.

### The repo gate

A Dag file that fails to parse fails every future run; import errors are the cheapest
bug to catch and the most expensive to miss. The lab's pattern applies unchanged: a
validator on every commit, not on the first failed 3 a.m. run.

## Real-World Application

- The DevMate daily loop: start Qdrant, ingest, reindex, run the offline eval, gate on
  Hit@5, notify on regression. Each step is a task; the eval gate is a sensor or a
  failing task that blocks the rest.
- Schedule the loop with cron at a quiet hour, `catchup=False` because repo re-ingest
  is not interval-valuable.
- Pass the Qdrant collection name and index path between tasks by XCom; pass the
  passages themselves through storage, never XCom.
- Make ingest idempotent first (Data Engineering 03), then schedule it: a retry or a
  backfill must not duplicate the corpus.

## Common Mistakes

1. **Treating the Dag file as a program.** Top-level code runs on every parse; work
   belongs in tasks.
2. **Passing dataframes through XCom.** XCom is metadata; data goes through storage.
3. **Poke-mode sensors on long waits.** A held worker slot for hours is a scheduling
   outage in waiting.
4. **`catchup=True` on a non-idempotent Dag.** The scheduler then faithfully
   duplicates the data for every missed interval.
5. **Hard-coded credentials in the Dag file.** Connections and hooks exist for this.
6. **Cron when the real trigger is data.** If the step should run when the asset
   updates, schedule on the asset, not on the clock.

## Key Takeaways

1. A Dag is a versioned, testable definition; the scheduler executes it, not the file.
2. TaskFlow turns task functions into testable Python.
3. XCom carries metadata; storage carries data.
4. Long waits belong in reschedule or deferrable sensors, never poke mode.
5. Catchup and backfill are only safe on top of idempotency.
6. Assets let the pipeline state its data dependencies in code.

## Self-Check Questions

1. What executes when a scheduler parses a Dag file, and what never executes there?
2. Why is `catchup=False` right for DevMate's ingest but wrong for an invoices
   pipeline?
3. How should a 100 MB result move between two tasks?
4. What is the difference between a variable and a param?
5. When does an asset-scheduled Dag run, and what problem does that solve?
6. What property must a pipeline have before backfill is safe?

## Further Reading / Connections

- Data Engineering 20 (Airflow execution and operations) — executors, pools,
  deferrable operators in production, deployment.
- Data Engineering 03 (idempotency) — the precondition for catchup and backfill.
- Data Engineering 08 (batch versus streaming) — Airflow is the batch-side scheduler.
- Airflow 3.4 docs: Core Concepts (Dags, Dag Runs, Tasks, Sensors, XComs), Authoring
  and Scheduling (Assets, Timetables, Backfill), and `dag.test()` in Testing a Dag.
