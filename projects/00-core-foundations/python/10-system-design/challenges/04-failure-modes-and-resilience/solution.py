"""
Challenge 04: Failure Modes and Resilience — Reference Solution
===============================================================
"""

from __future__ import annotations

from collections.abc import Callable


def classify_failure(error: Exception | None, context: dict) -> str:
    """Map an error + context to 'transient' | 'permanent' | 'partial' | 'silent'.

    Why this approach: the response follows the class, so classifying
    before responding is the whole discipline — transient gets retries,
    permanent gets a dead-letter, partial gets idempotent resume, silent
    gets metrics (there is nothing to catch).
    """
    if error is None:
        if context.get("staleness", 0) > 0:
            return "silent"
        if context.get("work_started") and not context.get("acknowledged"):
            return "partial"
        return "permanent"
    if isinstance(error, tuple(context.get("transient_types", (TimeoutError,)))):
        return "transient"
    return "permanent"


def run_with_bulkhead(
    tasks: list[dict], handler: Callable[[dict], None], bulkhead: dict, clock
) -> dict[str, int]:
    """Run tasks with concurrency cap + fail-fast timeouts.

    Why this approach: the bulkhead's slot accounting is what keeps one
    dependency's slowness from consuming every worker — saturation is
    answered with an explicit rejection, never an unbounded queue. Timeouts
    are checked BEFORE the call: a task that cannot finish is not started.
    """
    capacity = int(bulkhead["capacity"])
    timeout = float(bulkhead["timeout"])
    slots: list[float] = [0.0] * capacity  # finish time per slot
    served = rejected = timed_out = handler_calls = 0
    peak = 0

    for task in sorted(tasks, key=lambda t: t["arrival"]):
        arrival = float(task["arrival"])
        duration = float(task["duration"])
        free = [i for i in range(capacity) if slots[i] <= arrival]
        if not free:
            rejected += 1
            continue
        if duration > timeout:
            timed_out += 1
            continue
        slot = free[0]
        slots[slot] = arrival + duration
        busy = sum(1 for s in slots if s > arrival)
        peak = max(peak, busy)
        clock.advance(duration)
        handler(task)
        handler_calls += 1
        served += 1

    return {
        "served": served,
        "rejected": rejected,
        "timed_out": timed_out,
        "handler_calls": handler_calls,
        "peak_in_flight": peak,
    }


def degradation_ladder(state: dict, factory: Callable[[str], dict]) -> dict:
    """Map failure state to the degradation rung; never fabricate an answer.

    Why this approach: the ladder is a total function over the state space
    — every combination has a designed rung, and the bottom rung is an
    honest refusal. A confident wrong answer is the one outcome a
    scholarly product may never ship.
    """
    index = state.get("index", "down")
    if index == "current":
        return {"mode": "full", "data": factory("index")}
    if index == "stale":
        return {"mode": "stale-warning", "data": factory("index")}
    if state.get("source"):
        return {"mode": "keyword-fallback", "data": factory("source")}
    if state.get("cache"):
        return {"mode": "cached-only", "data": factory("cache")}
    return {"mode": "unavailable", "data": None}
