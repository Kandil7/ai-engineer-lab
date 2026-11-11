# Source Learning: Apache Airflow 3.4.0 Docs

- **Type**: doc
- **Date Started**: 2026-11-11
- **Status**: Completed
- **Template**: source-doc.template.md

---

# Source Summary (Docs): Apache Airflow 3.4.0 Stable

- **Source type:** Official Docs
- **URL:** https://airflow.apache.org/docs/apache-airflow/stable/index.html
- **Studied:** 2026-11-11
- **Related project/path:** `projects/00-core-foundations/data-engineering/19-dag-orchestration`,
  `projects/00-core-foundations/data-engineering/20-airflow-execution`

## Why I Read This

Airflow is the canonical batch scheduler for the data-engineering domain, and the
lab had no orchestration topic at all: the 18 existing topics covered ETL, storage,
lakehouse, and feature stores but nothing that scheduled them. The lab's through-line
is DevMate's daily ingest-and-eval loop, which is a real scheduled pipeline.

## Key Concepts (confirmed)

- A **Dag** is a workflow defined as Python: schedule, tasks, dependencies, callbacks.
  The Dag file is a definition that the scheduler parses; it does not execute at parse
  time.
- **TaskFlow** (`@task`) turns plain functions into tasks, inferring dependencies from
  argument passing; those functions stay pytest-testable.
- **XCom** carries small metadata between tasks through the metadata database; large
  data flows through storage with the reference in XCom.
- **Sensors** poll a condition (poke, reschedule, or deferrable mode); deferrable
  mode suspends the task and hands the wait to the triggerer, holding no worker slot.
- **Assets** let a Dag schedule on a dataset update event rather than on a clock.
- **Catchup** fills every missed interval; **backfill** re-runs a historical range
  deliberately. Both are only safe on an idempotent pipeline.
- **Executors**: Local (subprocesses), Celery (broker + workers), Kubernetes (pod per
  task). Multiple executors can run concurrently with per-task routing.
- **Pools** are named slot limits shared across Dags and throttle external systems.
- **Retries, execution timeouts, and SLAs** are three separate levers that must be
  configured as one failure decision.
- **Airflow 3** shifts: Task SDK (`airflow.sdk`), Dag bundles as declared sources,
  the public interface, durable/resumable tasks, and first-class assets.

## My Inferences (not stated, my interpretation)

- The repo's existing idempotency topic (Data Engineering 03) is the precondition
  that makes Airflow's catchup and backfill usable; without it, the scheduler
  faithfully amplifies bad discipline. This is why orchestration sits after
  idempotency in this track.
- LocalExecutor is the right starting point for a single-machine daily loop; moving
  to Celery or Kubernetes is a workload-variance decision, not a default upgrade.

## Code / Examples Worth Keeping

```python
from airflow.sdk import DAG, task, Asset

with DAG(dag_id="devmate_ingest", schedule="0 3 * * *", catchup=False):
    up = BashOperator(
        task_id="start_qdrant", bash_command="docker compose up -d qdrant"
    )

    @task
    def ingest() -> str: ...

    @task(schedule=[Asset("athar://passages")])
    def reindex(): ...

    up >> ingest() >> reindex()
```

## Practical Exercise

- `19-dag-orchestration.py --verify` proves: cycle rejection at parse, dependency-first
  topological order, one Dag run per missed interval (catchup), and idempotent replay.
- `20-airflow-execution.py --verify` proves: a 2-slot pool throttles a 50-task
  backfill, priority weights decide dispatch, a hanging eval is killed and retried
  within its timeout, and deferred waits hold no worker slot.

## Open Questions / Low-Confidence Areas

- Triggerer high-availability and failover behavior in Airflow 3 (docs are thin).
- The exact boundary between assets and the older datasets concept across 2.x to 3.x.

## Link to Project Task

- `projects/00-core-foundations/data-engineering/19-dag-orchestration`
- `projects/00-core-foundations/data-engineering/20-airflow-execution`
- `registries/knowledge-registry.yaml` (`data.orchestration`, `data.orchestration-ops`)
- `registries/evidence.yaml` (`ev-data-orchestration-scheduler`, `ev-data-orchestration-ops-executor`)

## ملخص عربي (Arabic Summary)

- Airflow يعرّف سير العمل (Dag) ككود Python: جدول زمني، مهام، تبعيات، إعدادات.
- XCom ينقل بيانات وصفية (metadata) بين المهام؛ البيانات الكبيرة تنتقل عبر التخزين.
- catchup و backfill آمنان فقط على خط أنابيب idempotent.
- executors: Local و Celery و Kubernetes؛ pools تتحكم في الضغط على الأنظمة الخارجية.
- Airflow 3: Task SDK، Dag bundles، واجهة عامة، assets كجدولة مدفوعة بالبيانات.
