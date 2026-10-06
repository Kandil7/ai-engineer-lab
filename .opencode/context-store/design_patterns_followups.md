---
id: design_patterns_followups
reported_by: opencode
created_at: 2026-10-05T18:30:00.823Z
---

# Design-patterns follow-ups: dedup, indexing, challenge 20-patterns

Session 2026-10-05 (same day as the topic-39 Poetry work, committed as 04e22ca).

## Completed
1. **Nested duplicate removal.** All 14 nested `02-advanced-python/NN-*/challenges/` dirs (topics 21-34) were byte-identical to the central `02-advanced-python/challenges/NN-*/` copies (hash-verified, identical file sets, no unique files). PRACTICE_SPEC.md section 1 declares the central path canonical. Deleted the 14 nested dirs (56 tracked files, recoverable from git). No references to nested paths exist in any md/yml/ps1/py file. No other module has this defect: `03-libraries/*`, `04-databases/*`, `05-web-frameworks/fastapi` each have exactly one canonical challenges/ dir.
2. **Challenge 20-patterns** built at `projects/00-core-foundations/python/02-advanced-python/challenges/20-patterns/` (README.md, starter.py, solution.py, test_challenge.py, 23 tests):
   - Bronze `adapt(provider, model, prompt, max_tokens) -> dict` — openai/ollama request shapes, ValueError on unknown provider and max_tokens < 1.
   - Silver `EventBus` (subscribe/unsubscribe/publish -> int) — measured guard: comparison budget `6 * (subscriptions + publishes)` over 300 CountingStr topics x 300 publishes. Naive flat list = 134,850 comparisons (fails); topic-indexed dict = ~0 (passes).
   - Gold `ModelRouter(models, probe)` with keyword-only `route(max_cost_cents, max_latency_ms, strategy)` — strategies cheapest/fastest/highest_quality, name-ascending tie-breaks, ValueError on no-feasible/unknown-strategy/empty. Production guard: probe each model at most once; FakeProbe raises on duplicate names; 60-route test asserts `len(probe.calls) <= len(models)`. Naive re-probe-per-route raises on route 2; solution uses 3 probes for 3 models.
   - Follow-up: staleness vs probe budget at 10^9 routes (answer sketch in README).
3. **Index sweep.** `challenges/README.md` lists all 21 sets (01-decorators marked stub: starter.py only); `learning_path.md` challenge table gains Patterns + grouped 21-34 rows; `02-advanced-python/README.md` tree block rewritten; `SKILLS_MASTERY_MAP.md` section 2 gains Practice link.

## Verification evidence (all run this session)
- Starter: 23 failed / exit 1. Solution: 23 passed / exit 0.
- Non-vacuity scratch demo: naive bus 134850 > 3600 budget; naive router RuntimeError "probe called twice for 'a'"; solution 0 comparisons, 3 probe calls.
- `python -m ruff check challenges/20-patterns/` = 0; `ruff format --check` = 0 (repo-wide deprecation warning is pre-existing).
- `python -m mypy --follow-imports=skip starter.py solution.py test_challenge.py` = Success; plain mypy on starter+solution = Success. Full-path mypy still blocked by pre-existing numpy stub error (reproduced on challenge 39, baseline).
- Five workspace validators (prompts/workflows/templates/registries/repo-structure) = exit 0.
- Docs gates (ci.yml replica): link scan fail=0; current-focus 2026-09-30, 5 days, fresh.

## Environment facts
- No venv under `projects/00-core-foundations/python/`; use system `python` (3.12.10, pytest 8.4.2, ruff 0.16.4, mypy 2.3.1).
- Run tests from `02-advanced-python/` as workdir: `python -m pytest challenges/20-patterns/test_challenge.py -q`, solution mode via `$env:CHALLENGE_USE_SOLUTION = "1"`.
- Env-var convention: sets 35-39 + 20 use CHALLENGE_USE_SOLUTION; 21-27 use CHALLENGE_MODULE=solution; 28-34 use neither.

## Open items
- Working tree uncommitted: 56 deletions, 4 new challenge-20 files, 5 modified docs (checkpoint auto-file, README, challenges/README, SKILLS_MASTERY_MAP, learning_path), session log. User decides the commit.
- 01-decorators challenge remains a stub (starter only).
- PRACTICE_SPEC section 1 mandates quiz.md per challenge set; repo precedent (21-34, 39, 20) puts quizzes in the topic dir instead — spec or precedent needs reconciling.
