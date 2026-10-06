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

## P1: uv adoption with verified qdrant fix, advisory audit, single local gate (2026-10-06)

### Context

ai-engineer-lab system improvement, P1 batch. Goal: uv adoption for DevMate, advisory security audit in CI, single local gate, in-repo docs gates.

### Explanation

uv.lock committed for DevMate (166 packages, revision 3) via `uv lock`; `uv sync --locked --extra dev --dry-run` exits 0. Bumped qdrant-client 1.8.2 to 1.12.2 (`>=1.9,<1.13`) fixing CVE-2026-85394-class input-validation CVE-2024-3829; verified the 1.12.2 wheel still exposes `QdrantRemote.search(collection_name, query_vector, query_filter, limit, with_payload, with_vectors)` matching vector_store.py:234 exactly. `uv audit` triage: three no-fix CVEs (python-ecdsa Minerva GHSA-wj6h-64fc-37mp, python-jose alg-confusion GHSA-3qf3-8w2g-rqmx) suppressed with --ignore-until-fixed so they resurface when fixed; ragas SSRF + langchain-community archived live in the optional eval extra, excluded from the CI surface via --no-extra; `rsa is archived` has no ignore mechanism and keeps the audit advisory. CI devmate job rewritten: setup-uv with cache, `uv sync --locked --extra dev`, gate via `uv run --frozen` (ruff, format, mypy, pytest), audit advisory with continue-on-error. Created infra/scripts/local-ci.ps1 (devmate 4 checks + legacy suite + 5 validators + docs gates; verified LOCAL CI: ALL GREEN) and infra/scripts/docs-gates.ps1 (link scan + freshness, matches the bash replica), documented in MAKEFILE.md. Repaired a broken local env on the way: the devmate .venv editable .pth pointed at the pre-rename `fullstack-ai-engineer-lab` path so `import devmate` failed (9 collection errors); fixed the .pth line, suite back to 52 passed. Reverted a dirtied tracked .coverage. Updated current-focus tasks 18-21 and plan.md lockfile note.

### Rationale (Why this?)

The audit gate follows the same judgment as the legacy-lint promotion: gate what is green, report the rest with tracked remediation. Bare --ignore on the fixable qdrant CVE was rejected in favor of actually fixing it; bare --ignore was never applied anywhere.

### Next Steps

P2 next: python-jose to pyjwt+cryptography migration (removes the unsuppressible rsa-archived status and CVE-2026-85394); then the audit step can gate. DevMate review debt after that (secret_key guard, debug default, mypy 3.11, API tests). The ubuntu run of all three promoted/rewritten CI jobs is unverified until the next push to master.

---
