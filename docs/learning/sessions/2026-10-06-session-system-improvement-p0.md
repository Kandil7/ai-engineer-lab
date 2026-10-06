# P0: legacy suite repaired, CI promotion scoped to tests, focus file truthful

### Context

ai-engineer-lab system improvement, P0 batch. The CI scope comment claimed 68 legacy failures; measured reality was 311 passed / 2 failed. Both failures were real bugs; the advisory job was hiding a nearly-green suite.

### Explanation

Fixed the two legacy failures: (1) practice_no_solutions.py carried U+00D7 in both a comment and the code line F = (C × 9/5) + 32, a SyntaxError on import; replaced with * in both places, minimal 2-line diff (an initial edit-tool pass reformatted the whole file and was reverted). (2) 18-tracking-platforms.py called mem.log_artifact() after log_run() had already called tracker.end(), tripping the adapter's own assert; extended log_run with an artifacts=() parameter so artifacts log inside the run window, demo updated. Legacy suite now 311 passed, 7 skipped, 0 failed. Promoted the CI legacy-lint job from advisory to gating on tests only: ruff stays advisory because the module carries ~2.3k style findings (I001/E402/N806) across teaching files, which is deferred churn per current-focus.md; the job now runs pytest -q as the gate and ruff --statistics as a visible advisory. Updated the stale CI scope comment (2026-09-26 to 2026-10-06). Rewrote current-focus.md: new stamp 2026-10-06, tasks 13-18 added (topics 39/40, challenge 20, quiz backfill, suite repair marked done; uv adoption as task 18), active window moved to Week 2 with the 2026-10-12 application date noted. All five validators exit 0; docs gates green (focus age 0 days).

### Rationale (Why this?)

CI now gates the entire curriculum instead of apologizing for it, and the tracking file matches measured reality. The promotion was scoped to tests rather than lint because gating 2.3k style findings would recreate the permanently-red pipeline the original comment warned about.

### Next Steps

P1 next: uv adoption for DevMate (lock, CI sync --locked, uv audit) and infra/scripts/local-ci.ps1 + docs-gates.ps1 to end the temp-dir replica. Then P2 DevMate review debt (secret_key guard, debug default, mypy 3.11, API tests). The ubuntu CI run of the promoted job is the remaining unknown: the suite is green on Windows; linux behavior of the 7 skipped tests is unverified.

---
