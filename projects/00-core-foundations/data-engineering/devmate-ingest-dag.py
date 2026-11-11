"""
Data Engineering — Applied Artifact: DevMate Ingest DAG
=====================================================
Reference Dag for the daily DevMate ingest-and-eval loop, built on the concepts in
topics 19-22 (Airflow authoring, execution, advanced authoring, security).

This file is a REFERENCE, not a runnable part of the repo: it imports
`apache-airflow`, which is not a dependency of this repository (see
projects/04-ai-engineering/devmate/pyproject.toml). It is kept here as the
"apply in lab project" artifact for source-index#31 and is not imported by any
module or test. To run it, install Airflow with a constraints file first:

    pip install "apache-airflow==3.4.0" --constraint constraints-3.4.0.txt

Concepts demonstrated:
    - Dag with schedule, catchup=False (topic 19)
    - TaskFlow tasks with XCom metadata only (topic 19)
    - Pool-throttled ingest, timeout-bounded eval (topic 20)
    - Dynamic task mapping over golden cases (topic 21)
    - Asset-scheduled reindex on passages update (topic 21)
    - Secrets via connection id, no credentials in source (topic 22)
"""

from __future__ import annotations

try:
    from datetime import datetime, timezone

    from airflow.providers.standard.operators.bash import BashOperator
    from airflow.sdk import DAG, Asset, task
except ImportError as exc:  # pragma: no cover - Airflow not installed in this repo
    raise SystemExit(
        "apache-airflow is required to run this Dag. "
        "See the module docstring for install instructions."
    ) from exc

PASSAGES = Asset("devmate://passages")

with DAG(
    dag_id="devmate_ingest",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule="0 3 * * *",
    catchup=False,
    params={"backfill_days": 7},
    tags=["devmate", "rag"],
):
    start_qdrant = BashOperator(
        task_id="start_qdrant",
        bash_command="docker compose up -d qdrant",
        pool="qdrant",
    )

    @task(pool="qdrant")
    def ingest() -> str:
        # Returns the index path only; passages flow through storage (topic 19).
        return "indexes/devmate"

    @task
    def fetch_cases() -> list[str]:
        return ["case_01", "case_02", "case_03"]

    @task
    def run_case(case: str) -> float:
        return 1.0  # Hit@5 per case

    @task
    def gate(scores: list[float]) -> None:
        if any(s < 1.0 for s in scores):
            raise ValueError("Hit@5 below threshold")

    @task(outlets=[PASSAGES])
    def reindex(index_path: str) -> str:
        return index_path

    @task(schedule=[PASSAGES])
    def downstream_refresh() -> None:
        pass

    idx = ingest()
    cases = fetch_cases()
    scores = run_case.expand(case=cases)
    g = gate(scores.collect())
    r = reindex(idx)
    start_qdrant >> idx >> g >> r >> downstream_refresh()


if __name__ == "__main__":
    print("Reference Dag. Requires apache-airflow to execute; see module docstring.")
