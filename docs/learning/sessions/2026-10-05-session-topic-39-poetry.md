# Topic 39 Poetry: challenge set + index/count updates

### Context

Repo ai-engineer-lab, `projects/00-core-foundations/python/02-advanced-python/`. Prior session wrote and committed topic 39-poetry (exercise, lecture, glossary, quiz). This session finished the work item: the Bronze/Silver/Gold challenge set under `challenges/39-poetry/`, plus every README/count index that enumerates Phase 2 topics.

### Explanation

The challenge follows PRACTICE_SPEC tiers with repo-consistent placement. Files: `README.md` (tiers + exact tables), `starter.py` (signatures only), `solution.py` (reference with "Why this approach" docstrings), `test_challenge.py` (loads starter by default, solution via `CHALLENGE_USE_SOLUTION="1"` — the 35-38 convention, not 27's older `CHALLENGE_MODULE`).

Bronze `expand_constraint` expands Poetry `^ ~ ~= *.*` and comma lists into `(lower, upper)` PEP 508 pairs; `!=`/`===` raise ValueError. Silver `install_closure` walks a package graph with an index-once strategy; the test wraps names in a `CountingStr` and caps comparisons at `10 * n` over a 2000-package chain whose root sits last in the list, so a per-node list scan (2,001,000 comparisons) fails while the indexed walk stays near 2,000. Gold `audit_manifest` returns fresh/groups/unsatisfied/sizes/fetches: freshness is the sha256 content-hash over the documented key subset (test carries its own reference implementation), groups implement `only/with/without` with ValueError on unknown names, and the fake index raises on a duplicate fetch so two-loop size summation dies while a fetch-once cache passes.

Index updates: `02-advanced-python/README.md` (38 to 39 topics, tree, table row, new "Tooling (39)" learning-order section), `challenges/README.md` row, `learning_path.md` (count, table, challenge table), `python/README.md` (tree, quick-start row), `SKILLS_MASTERY_MAP.md` dependency-management row, `docs/roadmap/skills-matrix.md` and `progress-dashboard.md` counts.

### Alternatives

Challenge-dir quiz was considered. Rejected because each topic carries exactly one quiz: 01-34 keep it in the topic dir, 35-38 only have it in the challenge dir because those topic dirs lack one. Topic 39 has a topic-dir quiz, so the challenge stays quiz-less like 21-34.

`run_smoke_tests.py` skip-list trick (naming the file like `39-pip.py`) was not needed: `39-pip.py` is skipped because it cannot run standalone, whereas `39-poetry.py` runs clean and passes the harness.

### Rationale (Why this?)

The comparison budget and fetch counter are deterministic and offline, per spec's ban on wall-clock assertions; both guards were proven non-vacuous by running a naive implementation (2,001,000 comparisons against a 20,000 budget). The content hash needed a test-side reference so learners can verify freshness without guessing Poetry's exact key set — the README documents those keys, and the exercise file already taught the same algorithm.

### Exercises

1. Run the starter, solve Bronze, then `python -m pytest 02-advanced-python/challenges/39-poetry/test_challenge.py -q`.
2. Validate with `$env:CHALLENGE_USE_SOLUTION = "1"` and confirm 30 passed.
3. Break the solution deliberately: make `audit_manifest` sum direct and total sizes in two loops and watch IndexDouble reject the duplicate fetch.
4. Replace the indexed walk in `install_closure` with a scan and watch the comparison budget fail at n=2000.
5. Add a `[dependency-groups]` block to the manifest fixture and confirm freshness flips to False.

### Next Steps

Commit decision is the user's (files are staged-ready but uncommitted). Possible follow-ups: teach `poetry lock --regenerate` recovery in the lecture, or add `39-poetry` to the PRACTICE_SPEC challenge-quiz exception note now that two quiz placements coexist.

---
