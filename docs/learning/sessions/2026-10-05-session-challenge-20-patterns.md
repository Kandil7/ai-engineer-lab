# Challenge 20-patterns + design-patterns dedup and indexing sweep

### Context

ai-engineer-lab, projects/00-core-foundations/python/02-advanced-python — follow-up to the topic-39 Poetry session. User asked "what about Design Patterns", which surfaced three defects: nested duplicate challenges/ dirs inside topic dirs 21–34, challenge sets 01 + 21–34 missing from the index files, and no challenge set at all for topic 20-patterns. User approved all three fixes with "continue".

### Explanation

**Dedup.** Hash-compared all 14 nested `NN-*/challenges/` dirs (topics 21–34) against the central `02-advanced-python/challenges/` path: every file byte-identical, identical file sets, no unique content anywhere. `PRACTICE_SPEC.md` §1 already declares the central path canonical and the nested copies a known bug. Deleted all 14 nested dirs (56 tracked files; recoverable from git history). Verified no references to nested paths exist in any md/yml/ps1/py file, and scanned the rest of the repo: `03-libraries/*`, `04-databases/*`, `05-web-frameworks/fastapi` each have exactly one `challenges/` dir (canonical, not duplicates), so the defect was unique to `02-advanced-python`.

**Challenge 20-patterns** built at the central path: README.md, starter.py, solution.py, test_challenge.py (23 tests). Bronze `adapt()` — provider request normalization (openai/ollama shapes, ValueError edges). Silver `EventBus` — subscribe/unsubscribe/publish with a measured comparison budget of `6 * (subs + publishes)` using CountingStr keys. Gold `ModelRouter` — strategy routing (cheapest/fastest/highest_quality with name tie-breaks, constraint filtering) under a probe-once production budget; the FakeProbe raises on a second call per name. Follow-up asks what breaks first at 10^9 routes (staleness vs budget).

**Verification evidence.** Starter run: 23 failed (NotImplementedError), exit 1. Solution run: 23 passed, exit 0. Non-vacuity demo (scratch script): naive flat-list bus 134,850 comparisons vs budget 3,600 (fires); solution bus 0; naive re-probing router raises on route 2; solution uses 3 probes for 3 models over 60 routes. ruff check + format: 0. mypy `--follow-imports=skip`: 0 issues on all 3 files; plain mypy on starter+solution: 0; repo-wide mypy remains blocked by the pre-existing numpy stub `type statement` error (reproduced identically on challenge 39). Five workspace validators: exit 0. Docs link scan: fail=0. current-focus stamp: 5 days old (fresh).

**Index updates.** `challenges/README.md` now lists all 21 sets (01 marked as a stub honestly); `learning_path.md` challenge table gains a Patterns row and a grouped 21–34 row; `02-advanced-python/README.md` tree block rewritten to describe the real index; `SKILLS_MASTERY_MAP.md` section 2 gains a Practice link to challenge 20.

### Exercises

1. Run both modes: `python -m pytest 02-advanced-python/challenges/20-patterns/test_challenge.py -q` (starter, expect 23 failures), then with `CHALLENGE_USE_SOLUTION=1` (expect 23 passes).
2. Write the naive flat-list EventBus yourself and run the Silver budget test to watch the comparison counter fire.
3. Extend `ModelRouter` with a TTL-based refresh (the Follow-up answer) and prove it still passes the probe budget over 60 routes.
4. Complete the `01-decorators` stub (solution + tests) so its index row stops saying "stub".

### Next Steps

1. Decide whether to commit the working tree (56 deletions, 4 new challenge files, 5 modified docs) — user's call.
2. Complete the `01-decorators` challenge stub or remove it from the tree.
3. Reconcile PRACTICE_SPEC §1 (mandates quiz.md per challenge set) with repo precedent: sets 21–34 and 39 carry no challenge quiz because the topic dir already has one — the spec text or the precedent should give.
4. Topic 20's own `20-patterns.py` exercise/lecture was not modified; challenge 20 only.

---
