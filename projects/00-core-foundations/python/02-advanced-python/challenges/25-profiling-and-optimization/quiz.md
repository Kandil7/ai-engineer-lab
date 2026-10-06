# Challenge 25 — Quiz: Profiling and Optimization

1. First-occurrence dedup in O(n) uses:
   - A) `list.index`  (B) a `set` of seen values  (C) `sorted`  (D) nested loops
2. The naive `if x not in result` dedup fails the guard because it is:
   - A) O(n)  (B) O(n²) — tens of seconds at 100,000 items  (C) O(n log n)  (D) unstable
3. `hash_join` reaches O(n) by:
   - A) sorting both sides  (B) building the index dict once, O(1) lookups  (C) hashing strings twice  (D) skipping duplicates
4. The adversarial join input places matches:
   - A) at the start  (B) at the end (reverse-ordered ids), forcing the scan  (C) randomly  (D) nowhere
5. A record whose `chunk_id` is missing from the index is:
   - A) raised  (B) skipped  (C) retried  (D) defaulted to `""`
6. Memoized `fib(25)` makes about:
   - A) 242,785 calls  (B) 49 calls  (C) 25 calls  (D) 0 calls
7. `fib_stats(0)` returns:
   - A) `(0, 0)`  (B) `(0, 1)`  (C) `(1, 0)`  (D) `(1, 1)`
8. The call count is the smoking gun because it is exactly what:
   - A) the profiler reports to spot exponential recursion  (B) the GIL measures  (C) tracemalloc shows  (D) the set tracks

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-A
