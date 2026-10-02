"""
Data Engineering — 08: Batch vs Streaming
==========================================
Topics: batch vs streaming decision, orchestrator DAGs, event logs,
        Lambda and Kappa recomputation, ordering and exactly-once.

Why this matters:
    Every pipeline relates to time as batch or streaming. This exercise
    builds a tiny DAG scheduler, an append-only event log, and shows both
    Lambda-style merging and Kappa-style replay with pure stdlib.

Run:      python 08-batch-vs-streaming.py
Verify:   python 08-batch-vs-streaming.py --verify
"""

from __future__ import annotations

import sys
from collections import deque


def topo_sort(dag: dict[str, list[str]]) -> list[str]:
    """Return tasks in dependency order (Kahn's algorithm)."""
    indegree = {t: 0 for t in dag}
    for deps in dag.values():
        for d in deps:
            indegree[d] = indegree.get(d, 0) + 1
    q = deque([t for t, d in indegree.items() if d == 0])
    order = []
    while q:
        t = q.popleft()
        order.append(t)
        for d in dag.get(t, []):
            indegree[d] -= 1
            if indegree[d] == 0:
                q.append(d)
    if len(order) != len(indegree):
        raise ValueError("cycle in DAG")
    return order


class EventLog:
    """An append-only, ordered, replayable log (a miniature broker)."""

    def __init__(self) -> None:
        self.events: list[dict] = []

    def append(self, event: dict) -> int:
        self.events.append(event)
        return len(self.events) - 1  # the offset

    def replay(self, from_offset: int = 0) -> list[dict]:
        return list(self.events[from_offset:])


def window_sum(events: list[dict]) -> int:
    """Aggregate a bounded slice of events (the batch or replay view)."""
    return sum(e["value"] for e in events)


def main() -> None:
    # 1. Orchestrator: a DAG schedules extract -> transform -> load.
    dag = {"extract": ["transform"], "transform": ["load"], "load": []}
    order = topo_sort(dag)
    assert order == ["extract", "transform", "load"]

    # 2. Broker: an append-only log holds the full history.
    log = EventLog()
    log.append({"value": 3})
    log.append({"value": 4})
    log.append({"value": 5})

    # 3. Lambda: batch view (all history) + speed view (recent window).
    batch_view = window_sum(log.replay(0))  # 3 + 4 + 5
    speed_view = window_sum(log.replay(2))  # only the latest slice
    assert batch_view == 12
    assert speed_view == 5

    # 4. Kappa: recompute the whole view by replaying the log.
    log.append({"value": 6})
    recomputed = window_sum(log.replay(0))  # one path, full replay
    assert recomputed == 18

    # 5. Exactly-once simulation: replaying from a checkpoint offset
    #    reproduces the same view (idempotent recomputation).
    checkpoint = 2
    partial = window_sum(log.replay(checkpoint))  # 5 + 6
    assert partial == 11
    assert window_sum(log.replay(checkpoint)) == 11  # replay is deterministic

    print(f"dag order: {' -> '.join(order)}")
    print(f"batch view={batch_view} speed view={speed_view}")
    print(f"kappa replay view={recomputed}")
    print(f"checkpointed replay view={partial} (deterministic)")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
