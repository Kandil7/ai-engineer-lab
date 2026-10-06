# Challenge 24 — Quiz: Memory and GC

1. Refcounts alone cannot free a reference cycle because:
   - A) refcounts are cached  (B) each object keeps the other's count above zero  (C) cycles are immortal  (D) `del` is forbidden
2. `collect_cycle(1)` returns:
   - A) 0  (B) 1 (a self-cycle is still collected)  (C) 2  (D) raises
3. On Python 3.13, `sys.getsizeof(instance)` is 48 bytes for both plain and slotted classes, so honest sizing must:
   - A) sample repeatedly  (B) include `__dict__` sizes  (C) use `gc.get_stats`  (D) divide by n
4. The measured `slots_ratio` at n=10,000 is about:
   - A) 1.0  (B) 2.8  (C) 0.5  (D) 48
5. A `WeakValueDictionary` entry whose only reference is temporary:
   - A) stays forever  (B) is evicted instantly (trap: length 0)  (C) leaks  (D) raises
6. After deleting the strong reference to the kept entry, the cache length is:
   - A) 1  (B) 0  (C) 2  (D) unchanged
7. `sum_materialized(100_000)` peaks at least:
   - A) 2x  (B) 10x above the streamed sum  (C) equal  (D) half
8. The `tracemalloc` tracer must run:
   - A) around the test  (B) inside each function (start/stop, read peak)  (C) in a thread  (D) after gc

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
