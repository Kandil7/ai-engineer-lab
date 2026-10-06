# Challenge 22 — Quiz: Asyncio Advanced

1. With `n_calls >= limit`, the semaphore makes `max_in_flight`:
   - A) exactly `limit`  (B) `n_calls`  (C) 1  (D) 0
2. `run_limited(5, 10)` returns `max_in_flight`:
   - A) 10  (B) 5 (never more than n_calls)  (C) 0  (D) undefined
3. `asyncio.Queue(maxsize=m)` makes the observed queue size:
   - A) unbounded  (B) `<= m`  (C) exactly `m`  (D) random
4. The naive unbounded-list pipeline fails because:
   - A) lists are slow  (B) observed sizes exceed the bound  (C) items get lost  (D) it cannot count
5. On task failure, `asyncio.TaskGroup`:
   - A) leaves pending tasks running  (B) cancels the still-pending tasks  (C) restarts them  (D) ignores the failure
6. A `gather`-based batch returns `cancelled ==`:
   - A) the pending count  (B) 0 (gather does not cancel siblings)  (C) n  (D) -1
7. `run_batch(5, 2)` returns:
   - A) `(2, 2)`  (B) `(5, 0)`  (C) `(0, 5)`  (D) `(4, 1)`
8. Cancellation is counted in each task's:
   - A) `finally`  (B) `except asyncio.CancelledError` handler  (C) return value  (D) semaphore

**Answers:** 1-A, 2-B, 3-B, 4-B, 5-B, 6-B, 7-A, 8-B
