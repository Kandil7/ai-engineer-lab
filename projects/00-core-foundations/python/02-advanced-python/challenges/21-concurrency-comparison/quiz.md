# Challenge 21 — Quiz: Concurrency Comparison

1. I/O-bound work with 10,000 calls should use:
   - A) threads  (B) processes  (C) async  (D) sequential
2. CPU-bound work should use:
   - A) threads  (B) processes (the GIL serializes threads)  (C) async  (D) recursion
3. I/O-bound with few calls defaults to:
   - A) async  (B) threads  (C) processes  (D) threads + processes
4. Eight 0.05 s sleeps under a ThreadPoolExecutor take:
   - A) 0.40 s  (B) under 0.24 s (overlapped)  (C) 0.05 s  (D) 8 s
5. Windows `spawn` requires the pool worker to be:
   - A) a lambda  (B) a nested function  (C) at module top level (importable)  (D) decorated
6. A thread-based CPU parallel run fails the perf guard because:
   - A) threads are slower to start  (B) the GIL serializes bytecode execution  (C) sleep is inaccurate  (D) pickling fails
7. `choose_model("gpu", 5)` returns:
   - A) `"processes"`  (B) `"async"`  (C) `ValueError`  (D) `"threads"`
8. The Silver guard asserts `elapsed <`:
   - A) `sleeps * delay`  (B) `sleeps * delay * 0.6`  (C) `delay`  (D) `sleeps`

**Answers:** 1-C, 2-B, 3-B, 4-B, 5-C, 6-B, 7-C, 8-B
