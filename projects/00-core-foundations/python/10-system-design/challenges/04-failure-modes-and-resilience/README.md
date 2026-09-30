# Challenge 04: Failure Modes and Resilience — The Blast Wall

The Athar embedder times out at 14:32. If the failure story is improvised,
the queue backs up and the database pool empties. Classify the failure, bound
its blast radius, and define what the product shows.

## 🥉 Bronze — Classify the Failure (~15 min)

**Task:** Implement `classify_failure(error, context)`:
- `error is None` and `context["staleness"] > 0` → `"silent"`
- `error is None` and `work_started` and not `acknowledged` → `"partial"`
- `error is None` otherwise → `"permanent"`
- error in `context["transient_types"]` → `"transient"`
- any other error → `"permanent"`

**Signature:**
```python
def classify_failure(error: Exception | None, context: dict) -> str
```

| Input | Expected |
|---|---|
| `TimeoutError()`, transient_types=(TimeoutError,) | `"transient"` |
| `ValueError()`, any context | `"permanent"` |
| `None`, `{"staleness": 3}` | `"silent"` |
| `None`, `{"work_started": True, "acknowledged": False}` | `"partial"` |

**Constraints:** context keys are always present. Any correct mapping passes.

---

## 🥈 Silver — The Bulkhead (~35 min)

**Task:** Implement `run_with_bulkhead(tasks, handler, bulkhead, clock)` over
tasks `{"id", "arrival", "duration"}` with `bulkhead = {"capacity", "timeout"}`:
- at most `capacity` tasks in flight; a task arriving when all slots are busy
  is **rejected** (not queued);
- a task whose `duration > timeout` is **timed out** and its handler is never
  invoked (fail fast — a call that cannot finish is not started);
- admitted tasks call `handler(task)` exactly once.

Returns `{"served": int, "rejected": int, "timed_out": int, "handler_calls": int,
"peak_in_flight": int}`. The injected `clock` is an object with `now()` and
`advance(dt)`; the pool advances it by each task's `duration` as work happens.

**Signature:**
```python
def run_with_bulkhead(tasks: list[dict], handler, bulkhead: dict, clock) -> dict[str, int]
```

| Scenario | Expected |
|---|---|
| 3 tasks at t=0, capacity 2, all short | `served=2, rejected=1, handler_calls=2` |
| 1 long task, duration > timeout | `timed_out=1, handler_calls=0` |
| 2 staggered tasks, capacity 2 | both served, `peak_in_flight <= 2` |

**Constraints:** `n <= 10000`. **Guards (call counting):** (a) the saturation
rejection is exact — an unlimited-concurrency implementation serves all 3 and
fails; (b) the timeout task must not invoke the handler — a run-then-check
implementation fails the `handler_calls` assertion; (c) `peak_in_flight` never
exceeds `capacity`. **Adversarial case:** all tasks arriving at the same
instant (the worst case for slot accounting).

---

## 🥇 Gold — The Degradation Ladder (~75 min)

**Task:** Implement `degradation_ladder(state, factory)` where
`state = {"index": "current" | "stale" | "down", "source": bool, "cache": bool}`
and `factory(kind)` produces the answer payload. Return `{"mode", "data"}`:
- index `"current"` → `"full"` with `factory("index")`
- index `"stale"` → `"stale-warning"` with `factory("index")`
- index `"down"`, source up → `"keyword-fallback"` with `factory("source")`
- index `"down"`, source down, cache up → `"cached-only"` with `factory("cache")`
- nothing available → `"unavailable"` with `data = None` — **never fabricate**.

**Signature:**
```python
def degradation_ladder(state: dict, factory) -> dict
```

| Scenario | Expected |
|---|---|
| index current | `mode == "full"` |
| index stale | `mode == "stale-warning"` |
| all down | `mode == "unavailable"`, `data is None` |

**Constraints:** all 12 states of the matrix must map correctly. **Guards:**
(a) exhaustive state matrix — every one of the 12 combinations produces the
documented rung (a solution with a silent default fails at least one cell);
(b) **fabrication invariant** — when nothing is available the data must be
`None`, never a made-up answer; (c) **factory call budget** — at most one
`factory` call per invocation (a "try everything always" fallback chain
fails). **Follow-up:** what breaks first when the stale rung is hit by 90% of
traffic? *(Answer: the fallback becomes the hot path — it needs its own cache
and bulkhead or the ladder protects nothing.)*

---

## Running

```bash
python -m pytest 10-system-design/challenges/04-failure-modes-and-resilience/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 10-system-design/challenges/04-failure-modes-and-resilience/test_challenge.py -q
```
