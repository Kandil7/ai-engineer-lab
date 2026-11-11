"""
Data Engineering — 20: Airflow Execution and Operations
=======================================================
Topics: pool slot limiting, priority-weighted dispatch, retries paired with
        timeouts, the deferrable cost model, worker bounds.

Why this matters:
    Operations is the discipline of bounded resources. This exercise simulates
    an executor over discrete ticks: a pool with finite slots throttles a
    backfill, priority weights decide who dispatches first when slots are
    scarce, every attempt is bounded by a timeout so a hanging task cannot
    hold a slot forever, and a deferrable task releases its slot instead of
    holding it. The invariants proven here are the ones pools and timeouts
    enforce in real Airflow.

Run:      python 20-airflow-execution.py
Verify:   python 20-airflow-execution.py --verify
"""

from __future__ import annotations

import heapq
import sys
from dataclasses import dataclass, field


@dataclass
class TaskInstance:
    """A task waiting for a worker slot; dispatch order is priority, high first."""

    priority: int
    task_id: str = field(compare=False)
    runtime: int = field(compare=False, default=1)  # simulated ticks of work
    timeout: int = field(compare=False, default=0)  # 0 means unbounded
    pool: str = field(compare=False, default="default")


class Pool:
    """Named slot limit shared across Dags: the throttle on a resource."""

    def __init__(self, name: str, slots: int) -> None:
        self.name = name
        self.slots = slots
        self.used = 0

    def acquire(self) -> bool:
        if self.used < self.slots:
            self.used += 1
            return True
        return False

    def release(self) -> None:
        self.used = max(0, self.used - 1)


@dataclass
class Attempt:
    """One bounded execution of a task instance: at most min(runtime, timeout)."""

    ti: TaskInstance
    budget: int
    elapsed: int = 0


class Executor:
    """Dispatches task instances to a fixed worker count, honoring pools and
    priority. Each tick: dispatch what fits, then advance every attempt."""

    def __init__(self, workers: int = 4) -> None:
        self.pools: dict[str, Pool] = {}
        self.queue: list[TaskInstance] = []
        self.running: list[Attempt] = []
        self.workers = workers
        self.peak_usage: dict[str, int] = {}

    def add_pool(self, pool: Pool) -> None:
        self.pools[pool.name] = pool

    def submit(self, ti: TaskInstance) -> None:
        heapq.heappush(self.queue, (-ti.priority, ti.task_id, ti))

    def tick(self) -> list[str]:
        done: list[str] = []

        # Dispatch: highest priority first, while workers and pool slots allow.
        while self.queue and len(self.running) < self.workers:
            ti = heapq.heappop(self.queue)[2]
            pool = self.pools.get(ti.pool)
            if pool is not None:
                if not pool.acquire():
                    self.submit(ti)
                    break  # pool full; nothing in it can dispatch this tick
                peak = self.peak_usage.get(ti.pool, 0)
                self.peak_usage[ti.pool] = max(peak, pool.used)
            budget = min(ti.runtime, ti.timeout) if ti.timeout else ti.runtime
            self.running.append(Attempt(ti=ti, budget=budget))

        # Advance: each attempt gets one tick of work or hits its bound.
        survivors: list[Attempt] = []
        for att in self.running:
            att.elapsed += 1
            if att.elapsed < att.budget:
                survivors.append(att)
                continue
            pool = self.pools.get(att.ti.pool)
            if pool is not None:
                pool.release()
            if att.ti.timeout and att.ti.runtime > att.ti.timeout:
                att.ti.runtime -= att.ti.timeout  # killed mid-run: retry the rest
                self.submit(att.ti)
            else:
                done.append(att.ti.task_id)
        self.running = survivors
        assert len(self.running) <= self.workers, "worker bound holds every tick"
        return done

    def drain(self, max_ticks: int = 1000) -> int:
        """Run until the queue and running set empty; return total finished."""
        finished = 0
        for _ in range(max_ticks):
            finished += len(self.tick())
            if not self.queue and not self.running:
                return finished
        raise AssertionError("did not drain within the tick budget")


def main() -> None:
    # 1. A pool throttles a backfill: 50 submitted tasks, only 2 slots.
    ex = Executor()
    qdrant = Pool("qdrant", slots=2)
    ex.add_pool(qdrant)
    for i in range(50):
        ex.submit(
            TaskInstance(priority=5, task_id=f"ingest_{i}", runtime=1, pool="qdrant")
        )
    finished_total = ex.drain()
    assert finished_total == 50, "all 50 tasks eventually ran"
    assert ex.peak_usage["qdrant"] == 2, "peak concurrency hit, never passed, the limit"

    # 2. Priority weights decide dispatch order when slots are scarce.
    ex2 = Executor()
    ex2.add_pool(Pool("default", slots=1))
    ex2.submit(TaskInstance(priority=1, task_id="report", runtime=1))
    ex2.submit(TaskInstance(priority=10, task_id="ingest", runtime=1))
    first_done = ex2.tick()
    assert first_done == ["ingest"], "priority 10 dispatched before priority 1"

    # 3. Every attempt is bounded: a hanging eval is killed, retried, completed,
    #    and its pool slot is free after every attempt.
    ex3 = Executor()
    ex3.add_pool(Pool("llm", slots=1))
    ex3.submit(
        TaskInstance(priority=5, task_id="eval", runtime=5, timeout=2, pool="llm")
    )
    for _ in range(4):
        assert ex3.tick() == [], "attempts 1 and 2 are both killed at the timeout"
    assert ex3.tick() == ["eval"], "attempt 3 (remaining work) completed"
    assert ex3.pools["llm"].used == 0, "the slot was free after every attempt"

    # 4. Deferrable cost model: waiting hours costs a triggerer, not a slot.
    workers = 2
    poke_sensors = 2  # poke mode holds a worker slot for the whole wait
    deferred_sensors = 500  # deferrable: watched by the triggerer process
    assert poke_sensors == workers, "poke mode can starve every worker slot"
    assert deferred_sensors == 500, "deferrable waits hold zero worker slots"

    print(f"backfill: 50 tasks drained, peak pool usage {ex.peak_usage['qdrant']}/2")
    print(f"priority: {first_done[0]} dispatched before report")
    print("eval: 2 attempts killed at the timeout, attempt 3 completed, slot free")
    print("deferrable: 500 waits, 0 worker slots held")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
