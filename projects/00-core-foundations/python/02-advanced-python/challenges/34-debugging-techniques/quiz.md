# Challenge 34 — Quiz: Debugging Techniques

1. `capture(fn)` returns:
   - A) the result  (B) the full traceback string, or `""` on success  (C) `None`  (D) the exception object
2. `capture(lambda: 1/0)` output contains:
   - A) only the message  (B) `"Traceback (most recent call last):"` and `"ZeroDivisionError"`  (C) a stack hash  (D) nothing
3. Each boundary assertion message must:
   - A) be empty  (B) name its stage  (C) be uppercase  (D) include the input
4. `[" ok ", ""]` through the pipeline raises `AssertionError` mentioning:
   - A) stage-3  (B) stage-1 (empty chunk after strip)  (C) nothing  (D) stage-2
5. Stage 2 (dedupe) asserts:
   - A) output is sorted  (B) nothing is lost (count and types)  (C) input is unique  (D) output is short
6. `make_repro(42)` called twice on the same input produces:
   - A) different orders  (B) identical output (seeded `random.Random`)  (C) a raise  (D) sorted output
7. `bisect_bad` over 100 configs uses at most:
   - A) 100 probes  (B) `ceil(log2(n)) + 1` probes  (C) 1 probe  (D) n/2 probes
8. For a real RAG bug, the first randomness to freeze is:
   - A) the LLM temperature  (B) every seed (shuffle, sampling, retrieval order)  (C) the clock  (D) the cache

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
