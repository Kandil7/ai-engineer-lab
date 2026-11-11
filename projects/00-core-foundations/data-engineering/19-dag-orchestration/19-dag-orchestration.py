"""
Data Engineering — 19: DAG Orchestration
========================================
Topics: the Dag model, dependencies and acyclicity, topological execution,
        catchup/backfill interval generation, XCom-as-metadata, idempotent runs.

Why this matters:
    Airflow's value is the model, not the library. This exercise rebuilds a
    miniature scheduler with plain Python: a Dag that rejects cycles, executes
    tasks in topological order, generates one Dag run per missed interval
    (catchup), passes only metadata between tasks, and proves a re-run is
    idempotent. The properties proven here are the same ones a real Dag needs.

Run:      python 19-dag-orchestration.py
Verify:   python 19-dag-orchestration.py --verify
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from datetime import date, timedelta


class CycleError(Exception):
    """The dependency graph is not acyclic."""


class Task:
    """One unit of work: a function plus its upstream task ids."""

    def __init__(
        self,
        task_id: str,
        fn: Callable[..., object],
        upstream: list[str] | None = None,
    ) -> None:
        self.task_id = task_id
        self.fn = fn
        self.upstream = list(upstream or [])


class Dag:
    """A directed acyclic graph of tasks, parsed but never executed at import."""

    def __init__(self, dag_id: str, tasks: list[Task]) -> None:
        self.dag_id = dag_id
        self.tasks = {t.task_id: t for t in tasks}
        self._assert_acyclic()

    def _assert_acyclic(self) -> None:
        """Parse-time acyclicity check: every task must be reachable in topo order."""
        state: dict[str, int] = {}

        def visit(tid: str) -> None:
            if state.get(tid) == 1:
                raise CycleError(f"cycle detected at task '{tid}'")
            if state.get(tid) == 2:
                return
            state[tid] = 1
            for up in self.tasks[tid].upstream:
                if up not in self.tasks:
                    raise CycleError(f"task '{tid}' depends on unknown task '{up}'")
                visit(up)
            state[tid] = 2

        for tid in self.tasks:
            visit(tid)

    def topological_order(self) -> list[str]:
        """Dependency-first execution order (DFS post-order)."""
        seen: set[str] = set()
        order: list[str] = []

        def visit(tid: str) -> None:
            if tid in seen:
                return
            seen.add(tid)
            for up in self.tasks[tid].upstream:
                visit(up)
            order.append(tid)

        for tid in self.tasks:
            visit(tid)
        return order


class DagRun:
    """One execution of a Dag over one interval. Carries XCom metadata."""

    def __init__(self, run_id: str, logical_date: date) -> None:
        self.run_id = run_id
        self.logical_date = logical_date
        self.xcom: dict[str, object] = {}
        self.state: dict[str, str] = {}
        self.counts: dict[str, int] = {}

    def execute(self, dag: Dag) -> None:
        """Run tasks in topological order; record per-task state and counts."""
        for tid in dag.topological_order():
            self.state[tid] = "running"
            out = dag.tasks[tid].fn(self.xcom)
            self.counts[tid] = int(out) if isinstance(out, int) else 1
            self.xcom[tid] = out  # XCom is metadata: small values only
            self.state[tid] = "success"


def daily_intervals(start: date, end: date) -> list[date]:
    """One logical date per schedule interval, inclusive, in order (catchup)."""
    days = (end - start).days + 1
    return [start + timedelta(days=i) for i in range(days)]


def make_ingest_dag() -> Dag:
    """The DevMate daily loop as a miniature Dag: up >> ingest >> eval."""

    def start_qdrant(xcom: dict[str, object]) -> int:
        return 1  # the container is up

    def ingest(xcom: dict[str, object]) -> int:
        assert xcom.get("start_qdrant") == 1, "ingest depends on start_qdrant"
        return 100  # passages indexed

    def eval_gate(xcom: dict[str, object]) -> int:
        assert xcom.get("ingest") == 100, "eval depends on ingest counts"
        return 1  # Hit@5 gate passed

    return Dag(
        "devmate_ingest",
        [
            Task("start_qdrant", start_qdrant),
            Task("ingest", ingest, upstream=["start_qdrant"]),
            Task("eval_gate", eval_gate, upstream=["ingest"]),
        ],
    )


def main() -> None:
    dag = make_ingest_dag()

    # 1. Order is dependency-first: no task runs before its upstream.
    order = dag.topological_order()
    assert order.index("start_qdrant") < order.index("ingest"), "upstream first"
    assert order.index("ingest") < order.index("eval_gate"), "eval last"

    # 2. A cycle is a parse-time error, exactly as in a real Dag file.
    try:
        Dag(
            "cyclic",
            [
                Task("a", lambda x: 1, upstream=["b"]),
                Task("b", lambda x: 1, upstream=["a"]),
            ],
        )
        raise AssertionError("cycle was not rejected")
    except CycleError:
        pass

    # 3. Catchup: one Dag run per missed interval, in order.
    intervals = daily_intervals(date(2026, 3, 1), date(2026, 3, 5))
    assert [d.day for d in intervals] == [1, 2, 3, 4, 5], "one run per interval"

    runs: list[DagRun] = []
    for logical in intervals:
        run = DagRun(f"scheduled__{logical}", logical)
        run.execute(dag)
        runs.append(run)
    assert len(runs) == 5
    assert all(all(s == "success" for s in r.state.values()) for r in runs)

    # 4. XCom is metadata: the count moved between tasks, not the corpus.
    first = runs[0]
    assert first.xcom["ingest"] == 100, "metadata (count) passed via XCom"

    # 5. Backfill re-runs are idempotent: same interval, same result state.
    replay = DagRun("backfill__2026-03-01", intervals[0])
    replay.execute(dag)
    assert replay.state == first.state, "idempotent: identical replay state"
    assert replay.counts == first.counts, "idempotent: identical counts"

    print(f"dag={dag.dag_id} tasks={len(dag.tasks)} order={order}")
    print(f"catchup: {len(runs)} Dag runs, one per interval")
    print("cycle rejected at parse; backfill replay idempotent")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
