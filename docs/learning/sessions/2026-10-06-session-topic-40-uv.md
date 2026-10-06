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
