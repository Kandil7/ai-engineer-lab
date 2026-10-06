# Topic 40-uv: full learning package with verified security facts

### Context

ai-engineer-lab, python curriculum (02-advanced-python). Session goal: deep-research uv and author the full learning-content package for topic 40-uv, anchored on the MLOps MENA talk about migrating legacy projects to uv and securing dependencies.

### Explanation

Delivered topic 40-uv as a complete package mirroring the 39-poetry pattern. Topic dir 40-uv/: 40-uv.py (10 sections, --verify self-check, stdlib tomllib/hashlib only: manifest classification, lock freshness via [manifest] requirements comparison, PEP 508 specifier subset, wheel-tag selection with simplified PEP 425 rules, group/extras flag resolution, hash verification, exclude-newer cooldown picker, uv audit simulation with ignore semantics, command map, mistakes). Lecture/glossary/quiz follow the 39 template. Challenge set challenges/40-uv/: Bronze wheel_tags parser, Silver WheelIndex (parse-once indexing, measured guard: 200 wheels x 100 queries, budget len(wheels)+5, naive re-parsing costs 20,000), Gold audit_stream (streaming auditor, tracemalloc peak < 1MB over 20,000 packages, naive list() peaks at 5.77MB), plus quiz.md. Research verified against: installed uv 0.12.13 CLI help (uv audit exists locally with --locked/--frozen/--output-format sarif/--ignore/--ignore-until-fixed; uv sync is exact by default with --inexact opt-out; --only-group excludes main deps), Astral blog 2026-06-08 (uv audit preview, 4-10x faster than pip-audit, UV_MALWARE_CHECK=1 opt-in OSV MAL check aborting sync before install because PyPI quarantine removes from index not object storage, PEP 792 adverse statuses), official docs (universal cross-platform uv.lock, pylock.toml PEP 751 relationship, migration paths: uv add -r, uvx pipreqs --mode no-pin for bare source trees, uvx migrate-to-uv for Poetry/Pipenv/pip-tools). Key distinction taught: --locked (resolve then fail if lock would change) vs --frozen (skip resolution entirely, installs stale lock happily); constraint-dependencies (restrict if requested) vs override-dependencies (force against ranges).

### Rationale (Why this?)

uv is the current default for reproducible Python environments and now carries the security layer (audit, malware check, cooldowns) that pip stacks assemble from separate tools. The topic was framed around the two legacy shapes the source talk covers (venv+requirements.txt, bare source tree) plus the Poetry comparison from topic 39. All facts verified against the installed binary and primary sources, not memory.

### Next Steps

Candidate follow-ups: challenge quiz.md backfill for sets 20-34 and 39 (spec requires quiz.md; 35-38 have it); run_uv smoke test wiring if uv-based verification is wanted; topic 41 candidate (pdm or hatch) to complete the tooling track; consider a docs/learning walkthrough of the uv.lock format from a real generated lock.

---

## Quiz backfill: 16 challenge sets brought up to spec (2026-10-06)

### Context

ai-engineer-lab, python curriculum (02-advanced-python). Follow-up in the same session: PRACTICE_SPEC.md requires quiz.md in every challenge set, but sets 20-34 and 39 shipped without one (only 35-38 and the reference set 49 had it).

### Explanation

Backfilled quiz.md for all 16 sets missing it: 20-patterns, 21-concurrency-comparison through 34-debugging-techniques, and 39-poetry. Each follows the house format verified from 35-unicode-and-arabic-text/quiz.md: title line, 8 single-line multiple-choice questions with inline options (A/B/C/D on one or two lines), and a final **Answers:** key line. Questions test decisions and consequences from each set's README (guards, adversarial inputs, naive-solution failure modes), not trivia. 01-decorators was left without a quiz deliberately: it is the documented stub (starter.py only, no solution or tests), so there is no content to quiz against. Verification: scripted check confirms 8 questions + 8-key answers line in every set except the stub; all five workspace validators exit 0; docs gates green (link_scan_fail=0, focus stamp 6 days).

### Rationale (Why this?)

The spec is the contract: an authored set that violates it is a bug. The backfill closes the gap without touching any tested code, so no test re-runs were needed beyond the validators.

### Next Steps

01-decorators needs its full set (solution, tests, quiz) to exit stub status; a spot-check pass by the user on quiz answer quality is worthwhile since most keys are B-heavy, matching the 35-38 house style.

---
