---
id: devmate_a2_golden_cases_2026_09_30
reported_by: builder
created_at: 2026-09-30T15:09:15.629Z
---

# A2 progress: prompt golden cases shipped (2026-09-30)

## Done
- evaluations/prompts/golden-cases/devmate.jsonl — 10 DevMate ask golden cases with expected_properties (groundedness, citations, must_not_* flags)
- evaluations/prompts/golden-cases/devmate-README.md — schema + maintenance rules
- projects/04-ai-engineering/devmate/src/devmate/eval/validate_prompt_golden.py — offline validator (no API)
- projects/04-ai-engineering/devmate/tests/unit/test_prompt_golden.py — 5 offline tests
- Path fix: GOLDEN_PATH uses Path(__file__).parents[6] = repo root (file is under src/devmate/eval/)
- Ruff: split validate_cases to clear C901; print → sys.stderr/stdout for T20

## Verification (2026-09-30)
- ruff check . → All checks passed
- ruff format --check . → 50 files already formatted
- mypy src/ → no issues in 33 source files
- pytest -q → 42 passed (includes 5 new golden tests)

## Remaining A2
- Langfuse keys in projects/04-ai-engineering/devmate/.env (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST)
- One live traced devmate ask run
- P-track (production AI) stays gated on A4/A6

## Tracing wiring FACT
- llm/client.py wraps llm.complete with tracer.trace(...)
- obs/tracing.py exports spans to Langfuse when keys present
- cost_tracker.record_usage called on all provider complete paths

