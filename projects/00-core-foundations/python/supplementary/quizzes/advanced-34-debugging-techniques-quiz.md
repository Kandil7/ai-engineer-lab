# Advanced Python Quiz 34 — Debugging Techniques

**Course:** AI Engineer — Core Foundations · Python
**Level:** Advanced · **Topic:** 34 — Debugging Techniques
**Questions:** 20 (6 Easy · 9 Medium · 5 Hard)
**Time:** 30 minutes

---

## Instructions

- Each question has exactly **one** correct answer (A–D).
- **Code-output questions** show code; choose the output.
- Answers and explanations are at the end — do the quiz **before** reading the key.
- Score yourself: `Score Tracking` section at the end.

---

## Questions

### Easy

**1. Where is the exception actually raised in a traceback?**

A) The first (top) frame
B) The last (bottom) frame
C) In the middle frame
D) There is no way to tell

**2. Which should you log in an exception handler?**

A) `str(exc)`
B) `traceback.format_exc()`
C) `repr(exc.__cause__)`
D) Nothing — exceptions are always visible

**3. What does `breakpoint()` do?**

A) Raises a `BreakpointError`
B) Drops into the `pdb` interactive debugger
C) Logs a warning at the call site
D) Stops the process entirely

**4. What is a "silent bug"?**

A) A bug that produces no log lines
B) Wrong output with no exception — the AI bug class
C) A bug that only appears at night
D) A syntax error hidden in a comment

**5. What is the purpose of `faulthandler.enable()`?**

A) To disable all exception handling
B) To dump Python stack traces on crash signals or on demand
C) To speed up exception raising
D) To catch `SyntaxError` at import time

**6. Why freeze seeds when reproducing a bug?**

A) Seeds make code faster
B) A reproducible failure requires deterministic randomness
C) Seeds are required by pytest
D) Seeds prevent memory leaks

### Medium

**7. Given:**

```python
import random

rng = random.Random(42)
a = rng.shuffle(["a", "b", "c"])
rng2 = random.Random(42)
b = rng2.shuffle(["a", "b", "c"])
print(a == b)
```

**What is the output?**

A) `True`
B) `False`
C) `None` — `shuffle` returns `None`
D) `Error`

**8. In the hypothesis-driven method, what comes immediately after "isolate"?**

A) Fix
B) Hypothesize
C) Reproduce
D) Regression test

**9. What does `traceback.format_exception(type(exc), exc, exc.__traceback__)` return?**

A) A single string with the message
B) A list of formatted traceback lines
C) The exception's class name
D) `None` if the exception was caught

**10. Given:**

```python
def bisect_bad(configs, bad_from):
    lo, hi = 0, len(configs) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid >= bad_from:
            hi = mid
        else:
            lo = mid + 1
    return lo


print(bisect_bad([f"c{i}" for i in range(100)], 42))
```

**What is the output?**

A) `42`
B) `50`
C) `41`
D) `99`

**11. Why must stage-boundary assertions be added BEFORE the retriever in a RAG pipeline?**

A) To speed up retrieval
B) To catch corrupted data at the boundary where it enters, not where it breaks
C) Assertions only work before retrieval
D) To avoid embedding calls

**12. What is the primary difference between a crash and a hang?**

A) Crashes are slower
B) A crash raises an exception (visible); a hang blocks forever (invisible)
C) Hangs always produce tracebacks
D) Crashes only happen on Linux

**13. What does `asyncio.run(main(), debug=True)` do?**

A) Disables all warnings
B) Enables slow-callback and unawaited-task diagnostics
C) Makes coroutines run faster
D) Converts async code to sync

**14. Which is the correct first step when a batch job hangs?**

A) Restart the machine
B) Dump the stack with `faulthandler` to see where threads block
C) Add more threads
D) Increase the timeout

**15. Given `capture(lambda: 1/0)`, what does `capture` return if implemented with `traceback.format_exc`?**

A) `""`
B) `"ZeroDivisionError"` only
C) A string starting with `"Traceback (most recent call last):"`
D) The integer `1`

### Hard

**16. A RAG pipeline silently returns wrong chunks. Which probe proves the retriever ranks by length instead of relevance?**

A) `print(len(retrieve(q, chunks, 1)))`
B) `print(retrieve(q, ["short", "a much longer chunk"], 1))` — if it returns `"short"`, the metric is length
C) `assert len(chunks) > 0`
D) `random.seed(42)` before retrieval

**17. `cap.cmdqueue = ["n", "p x", "n", "p y", "c"]` in a scripted pdb session: why the `n` commands?**

A) To slow down the session
B) To step past assignments so `p x`/`p y` see live values
C) `p` requires `n` first
D) To skip the `__main__` frame

**18. With `PYTHONHASHSEED=0 python repro.py`, what are you fixing?**

A) Random number generation
B) Dict/set iteration order instability
C) The seed of numpy
D) Locale encoding

**19. Which sequence correctly completes the method: reproduce → ____ → hypothesize → ____ → fix + regression test?**

A) isolate → prove
B) prove → isolate
C) log → bisect
D) probe → assert

**20. A regression across 100 commits: what is the minimum number of `git bisect`-style probe runs needed to find the first bad commit?**

A) 100
B) 50
C) ~7 (ceil(log2(100)) + 1)
D) 1

---

## Score Tracking

| Section | Count | Your Score |
|---------|-------|------------|
| Easy (Q1–6) | 6 | /6 |
| Medium (Q7–15) | 9 | /9 |
| Hard (Q16–20) | 5 | /5 |
| **Total** | **20** | **/20** |

**Rating:** 18–20 → Debugging method locked · 14–17 → Review sections 4.1–4.6 · <14 → Re-read the lecture and practice the five-step method on a real bug.

---

## Answer Key

**1. B** — Tracebacks print outside-in; the last (bottom) frame is the raise site.
*Distractors:* A is the entry point, C/D wrong.

**2. B** — `format_exc()` preserves the full frame chain; `str(exc)` keeps only the message.
*Distractors:* A loses frames, C loses the exception, D is false.

**3. B** — `breakpoint()` enters pdb (no-op if `PYTHONBREAKPOINT=0`).
*Distractors:* A/C/D are not what it does.

**4. B** — Silent bugs produce wrong output with no exception — the RAG wrong-chunks class.
*Distractors:* A is about logging, C is not a class, D is a syntax error.

**5. B** — faulthandler dumps stacks on SIGSEGV/SIGABRT and on demand.
*Distractors:* A/C/D wrong about its purpose.

**6. B** — A reproducible failure requires deterministic randomness; a bug that disappears when seeded was a randomness bug.
*Distractors:* A/C/D false.

**7. C** — `list.shuffle` returns `None` (it shuffles in place); `a` and `b` are both `None`.
*Distractors:* A/B compare `None`s correctly but the printed values are `None`, D is wrong — no error.

**8. B** — reproduce → isolate → **hypothesize** → prove → fix.
*Distractors:* A/C/D are other steps in the loop.

**9. B** — `format_exception` returns a **list** of lines; `format_exc` returns the joined string.
*Distractors:* A is `str(exc)`, C is `type(exc).__name__`, D false.

**10. A** — Binary search converges on the first bad index, 42.
*Distractors:* B is the first midpoint, C off-by-one, D the max index.

**11. B** — Assert at the boundary where data enters a stage, so corruption is caught where it is introduced, not where it surfaces.
*Distractors:* A/C/D false.

**12. B** — A crash raises (visible); a hang blocks forever with no exception — hence faulthandler.
*Distractors:* A/C/D false.

**13. B** — `debug=True` enables slow-callback, unawaited-task, and I/O selector diagnostics.
*Distractors:* A/C/D false.

**14. B** — Dump the stack to see exactly where threads block; that is faulthandler's job.
*Distractors:* A/C/D are guesses, not diagnoses.

**15. C** — `format_exc` returns the full traceback starting with the header.
*Distractors:* A is success, B is `str(exc)`, D wrong.

**16. B** — If a 22-char chunk loses to `"short"` (5 chars), the ranking key is length. That is the probe.
*Distractors:* A measures nothing about the metric, C is an invariant not a probe, D is unrelated.

**17. B** — `n` executes the assignment line so the next `p` sees the live value; at the first stop `x`/`y` are not yet defined.
*Distractors:* A/C/D false.

**18. B** — `PYTHONHASHSEED` fixes str/bytes hash randomization, i.e. set/dict iteration order.
*Distractors:* A is `random.seed`, C is numpy's seed, D unrelated.

**19. A** — reproduce → isolate → hypothesize → **prove** → fix + regression test.
*Distractors:* B/C/D reorder or substitute steps.

**20. C** — Binary search: ~7 runs (ceil(log2(100)) + 1) — logarithmic, not linear.
*Distractors:* A is linear, B is half, D impossible.
