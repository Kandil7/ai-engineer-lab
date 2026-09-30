# Challenge 02: Queues and Workflows — The Embed Queue

Thousands of Athar chunks wait for embedding. The workers will crash mid-job,
the broker will redeliver, and one payload is malformed forever. Design the
queue semantics that survive all three.

## 🥉 Bronze — Idempotent Insert (~15 min)

**Task:** Implement `insert_if_absent(store, key, value)`, inserting
`store[key] = value` only when absent. Returns `True` if inserted, `False` if
already present.

**Signature:**
```python
def insert_if_absent(store: dict, key: str, value) -> bool
```

| Input | Expected |
|---|---|
| fresh key | `True`, store updated |
| existing key | `False`, store unchanged |

**Constraints:** any correct approach passes.

---

## 🥈 Silver — The Retry Policy (~35 min)

**Task:** Implement `run_job(job, handler, policy, sleep)`:
- `handler(job)` returns `True` on success or raises.
- `policy = {"max_attempts": int, "base_delay": float, "transient": tuple}`
- Transient exceptions (in `policy["transient"]`) retry with exponential
  backoff: the delay for attempt *k* is `base_delay * 2**(k-1)`, passed to the
  injected `sleep(delay)` — never a real sleep.
- Permanent exceptions are **not** retried.
- Returns `"done"` or `"dead_letter"`.

**Signature:**
```python
def run_job(job: dict, handler, policy: dict, sleep) -> str
```

| Scenario | Expected |
|---|---|
| succeeds first try | `"done"`, no sleep calls |
| fails transiently twice, then ok | `"done"`, sleeps `[base, 2*base]` |
| raises permanent error | `"dead_letter"`, handler called exactly once |
| always fails transiently | `"dead_letter"`, handler called exactly `max_attempts` |

**Constraints:** `max_attempts <= 10`. **Guards (call counting):** (a) the
sleep sequence is exactly `[base, 2*base, ...]` — a constant-delay or
unbounded-retry implementation fails; (b) permanent errors invoke the handler
**once**; (c) exhaustion invokes it exactly `max_attempts` times. **Adversarial
case:** a handler failing `max_attempts - 1` times then succeeding.

---

## 🥇 Gold — The Worker Pool (~75 min)

**Task:** Implement `run_worker_pool(jobs, handler, policy)`, processing
`(job_id, payload)` pairs where some ids are **redelivered duplicates** and
some jobs are poison (always fail transiently). Returns
`{"done": int, "dead_lettered": int, "skipped_duplicates": int, "handler_calls": int}`:
- each unique id produces at most one `done`;
- redeliveries count as `skipped_duplicates`;
- poison ids end in `dead_lettered` after `max_attempts` handler calls each.

**Signature:**
```python
def run_worker_pool(jobs: list[tuple[str, str]], handler, policy: dict) -> dict[str, int]
```

| Input | Expected |
|---|---|
| 3 unique + 2 redeliveries | `done=3, skipped_duplicates=2` |
| 1 poison id (attempted 3x) | `dead_lettered=1, handler_calls=3` |
| `[]` | all zeros |

**Constraints:** 10k jobs, memory ceiling 8 MB peak (`tracemalloc`) — storing
per-job histories blows it; counters + a dedupe set stay flat. **Guards:**
(a) idempotency — exact `done`/`skipped_duplicates` accounting under
redelivery; (b) `handler_calls` exact (retry accounting); (c) memory ceiling.
**Follow-up:** what breaks first at 10^7 jobs? *(Answer: the in-memory queue
and the dedupe set — you need a real broker with visibility timeouts and a
persistent dedupe store.)*

---

## Running

```bash
python -m pytest 10-system-design/challenges/02-queues-and-workflows/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 10-system-design/challenges/02-queues-and-workflows/test_challenge.py -q
```
