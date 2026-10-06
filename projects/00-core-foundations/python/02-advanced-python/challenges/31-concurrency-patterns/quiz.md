# Challenge 31 — Quiz: Concurrency Patterns

1. A `TokenBucket(capacity=3)` rejects the 4th call at t=0 with:
   - A) `True`  (B) `False` (bucket empty)  (C) a raise  (D) a block
2. After advancing the fake clock +1.0 s at rate 1.0, exactly:
   - A) 3 tokens refill  (B) 1 token refills  (C) 0 tokens  (D) capacity resets
3. After +100 s, the bucket holds:
   - A) 100 tokens  (B) at most `capacity` (refill is capped)  (C) 0  (D) infinity
4. All timing uses injected clocks so tests:
   - A) sleep briefly  (B) run in milliseconds with zero sleeping, deterministic  (C) need real time  (D) are flaky
5. `produce` into a full bounded queue returns `False`:
   - A) immediately, possibly hanging  (B) within `timeout`, never hanging  (C) after raising  (D) never
6. `consume` returns items in:
   - A) LIFO order  (B) FIFO order  (C) random order  (D) size order
7. While the circuit is open, `call()`:
   - A) invokes `fn`  (B) raises `RuntimeError` and `fn` is NOT invoked  (C) queues the call  (D) sleeps
8. After the cooldown, one success moves the breaker to:
   - A) `open`  (B) `closed` (a failure would re-open it)  (C) `half_open` forever  (D) `short_circuited`

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
