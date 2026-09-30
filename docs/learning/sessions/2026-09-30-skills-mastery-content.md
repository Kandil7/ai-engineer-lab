# Skills Mastery Content: Gap-Filling the Python Learning Module

### Context

Session in `projects/00-core-foundations/python/` (fullstack-ai-engineer-lab). Goal: complete full learning content for every section of the Athar skills table (Production Python, Maintainable Code, Testing, Databases, Backend/APIs, System Design) and add sections that do not exist.

### Explanation

Gap analysis against the 6-skill Athar table found existing phases strong on Python fundamentals, libraries, FastAPI, and DSA, but missing: Unicode/Arabic text handling; separation of concerns/DI as a dedicated topic; code review; the full test taxonomy (contract/regression/data); migrations (Alembic); backup/restore; and an entire system-design phase (contracts, queues, consistency, failure modes, ADRs).

Created 11 new topic directories (35 files) in the established 3-file format (exercise .py + lecture .md + glossary .md), each exercise runnable offline on stdlib with a `--verify` mode:

- `02-advanced-python/35-unicode-and-arabic-text` — code points vs bytes, normalization NFC/NFKC, lam-alef presentation forms, harakat stripping, Arabic-Indic digit folding, bidi, collation, bounded-memory batch importer with located failures.
- `02-advanced-python/36-separation-of-concerns` — layered pipeline (parser→normalizer→validator→indexer), Protocols, constructor DI, composition root, frozen config, library-grade logging, spy-double proof, engine-swap mastery test.
- `02-advanced-python/37-code-review-and-refactoring` — review lenses (correctness→structure→tests→security→style), smell measurement via ast, extract-method, strategy-over-conditional, lock tests, four-part review comments.
- `02-advanced-python/38-test-strategy-contract-regression` — unit/integration/contract/regression/data tests on one pipeline; byte-for-byte provenance test; idempotent rerun; golden known-failure cases; pytest forms.
- `04-databases/sqlalchemy/11-migrations-alembic` — revision chains, upgrade/downgrade, expand→backfill→contract, idempotent data migrations, migration testing, lineage-preserving schema edits.
- `04-databases/postgresql/07-backup-and-restore` — verify-by-restore, RPO/RTO, WAL/PITR, 3-2-1, derived index excluded from backup surface, disaster runbook, corruption detection.
- `10-system-design/` (new phase, 5 topics + README) — component contracts (four-part, compatibility classes, migration paths), queues/workflows (at-least-once, idempotency, backoff, DLQ, bounded workers), consistency/staleness (truth-vs-derived, drift, cache TTL/invalidation, read-your-writes, staleness state machine), failure modes (taxonomy, FMEA-lite, timeouts, cascading failure, bulkheads, degradation ladder), ADRs (format, threshold test, status lifecycle, enforcement links).

Plus `SKILLS_MASTERY_MAP.md` mapping the Arabic table's 6 skills to all topics with Athar application and mastery evidence, and updates to `README.md`/`learning_path.md`.

### Alternatives

1) Filling gaps into existing numbered topics (rejected: breaks established numbering and discoverability). 2) Writing one monolithic guide instead of topic directories (rejected: the repo convention is 3-file topic dirs with runnable exercises). 3) Skipping exercises and writing lectures only (rejected: the mastery criteria demand runnable proofs like the engine-swap and idempotent-rerun tests).

### Rationale (Why this?)

Matched the repo's established convention exactly (NN-name/ with .py + -lecture.md + -glossary.md), so new content slots into the existing learning path and smoke-test runner. Every exercise is stdlib-only and offline, honoring PRACTICE_SPEC rule "no network, no service dependency." The skills map makes the Arabic table's mastery criteria verifiable rather than aspirational.

### Exercises

1. Run each new exercise with `--verify` and read the PASS list. 2. Break the batch importer (corrupt a record) and observe the line-numbered failure. 3. Swap `InMemoryIndex` for `PrefixIndex` in topic 36 and confirm validation errors are identical. 4. In topic 38, add a 21st known-failure case and see it fail before the fix. 5. Write one real ADR for a decision in a project of yours, validated by topic 05's rules.

### Next Steps

Challenge sets per PRACTICE_SPEC for the 11 new topics (Bronze/Silver/Gold tiers). Wire the new test markers into CI. Extend the skills map with links into 08-mlops and 09-genai case studies as capstone references.

---

## Challenge Sets Completed for All 11 New Topics (2026-09-30)

### Context

Follow-up to the skills-mastery content session in `projects/00-core-foundations/python/`. The 11 new topics (35-38 advanced-python, 11-migrations, 07-backup, 10-system-design 01-05) had lectures and exercises but no practice challenge sets per `PRACTICE_SPEC.md`.

### Explanation

Created 11 complete challenge sets (60 files: README + starter + solution + test_challenge + quiz each) at the central challenges paths, following the 49-collections-toolkit reference exactly. Every set implements the spec's non-negotiable rules: Bronze/Silver/Gold tiers, measured guards (comparison counting via CountingStr, call counting via spies, tracemalloc ceilings — never wall-clock), deterministic seeded data, starter-default target (importlib loading, CHALLENGE_USE_SOLUTION=1 for reference), explicit edge coverage, adversarial guard cases, and Athar-domain framing. The Silver/Gold guards separate naive from correct: O(n^2) pairwise comparison budgets, fail-fast-vs-collect-all validation, one-shot-vs-expand-backfill-contract migrations, count-only-vs-byte-for-byte restore verification, apply-all-vs-point-in-time WAL replay, one-step-vs-rolling-upgrade plans, no-TTL-vs-TTL cache loader call budgets, arrival-order-vs-versioned event apply, unlimited-vs-bulkhead concurrency, and partial-vs-complete ADR validation. Created four challenges/README.md indexes (none existed before).

A parallel first attempt via builder subagents returned empty results and wrote nothing — diagnosed and built directly instead per the guardrails. Several verification cycles caught real bugs: the shared SpyIndex double-count in challenge 36, the visit_Return name-rewrite gap in challenge 37's AST state-threading, TTL boundary semantics in challenge 03, and the markdown bold-marker parse in challenge 05.

### Alternatives

1) Re-delegate to subagents after the silent failure (rejected per guardrails: diagnose yourself). 2) Skip the Gold tier's measured guards (rejected: the spec requires naive-but-correct to FAIL a guard). 3) Wall-clock timing assertions (rejected explicitly by the spec).

### Rationale (Why this?)

Direct construction with per-set two-mode verification (starter must fail, solution must pass) caught every design flaw before it reached the learner. The guards are all deterministic (counts, hashes, memory ceilings) so the suites are CI-stable.

### Exercises

1. Pick any set and solve starter.py until the suite goes green. 2. Break one guard intentionally (e.g. replace dict grouping with pairwise comparison in 35) and watch the budget fail. 3. Time yourself against the Bronze/Silver/Gold estimates. 4. Re-solve Gold with a different structure and confirm the guard still passes. 5. Add one more known-failure case to 38's suite.

### Next Steps

Add the challenge sets to the module's smoke test discovery if desired. Wire CHALLENGE_USE_SOLUTION=1 runs into CI as a reference-regression job. Continue extending gold-case coverage in `evaluations/prompts/golden-cases/`.

---
