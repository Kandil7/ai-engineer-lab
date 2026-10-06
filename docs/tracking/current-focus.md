# Current Focus — Execution Window

> What to work on RIGHT NOW. Update weekly. Be specific — this replaces decision fatigue.
>
> ⚠️ A staleness gate fails CI if this file is more than 8 days old: `make fresh-check`
> locally and the Tracking freshness step in `.github/workflows/ci.yml`.

**Last updated:** 2026-10-06

---

## Active Window

**Week 2** — 2026-10-06 → 2026-10-12 (RAG + application window)

**Plan:** [Active Track — 10-Week AI Engineer](../roadmap/active-track-10-week.md)
(adopted 2026-08-02 by [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md))

**Strategic follow-on (not active yet):**
[Production AI Systems Engineer roadmap](../learning/design/production-ai-systems-engineer-roadmap.md)
— phased P1–P8 production depth. Start only after A4 and preferably A6.

**Project:** DevMate — `projects/04-ai-engineering/devmate/`

**Content track:** [ADR-0006](../decisions/0006-adopt-master-ai-engineering-curriculum.md)
lifted the lecture moratorium. Decision made 2026-09-26: the "Master AI Engineering" content
is adopted as `docs/curriculum/` (4 lecture + workbook modules anchored to DevMate) — no
separate `projects/04-ai-engineering/master-ai-engineering/` directory will be created.
`embeddings/`, `prompt-engineering/`, `rag-system/` were filled 2026-09-29 with learning
content (4-6 topics each, lecture + glossary + exercise + quiz).

---

## Main Goal

Week 1 (A2) mostly closed offline: golden cases + eval harness foundation shipped.
Remaining A2: Langfuse keys + live traced ask. A3 harness code exists; live retrieval
and the two ADRs are next once Qdrant/ingest are up.

---

## Today's Tasks

1. ~~DevMate lint/types/tests pass locally~~ — verified 2026-09-26
2. ~~GitHub Actions green on `master`~~ — CI run 36269637267, 2026-09-26
3. Repair Tier 0 backlog R1–R7 + R9 (`../../projects/00-core-foundations/python/admin/mastery-plan/10-remediation-backlog.md`)
4. ~~Master AI Engineering module decision~~ — adopted as `docs/curriculum/` (ADR-0006)
5. ~~Fill empty modules: `embeddings/`, `prompt-engineering/`, `rag-system/`~~ — done 2026-09-29
6. ~~Write DevMate unit tests for the stats command~~ — `tests/unit/test_cli_stats.py`
7. ~~10 prompt golden cases for `devmate ask`~~ — done 2026-09-30
8. Add Langfuse keys to `projects/04-ai-engineering/devmate/.env` (from self-hosted compose UI) and run one traced `devmate ask`
9. ~~Offline eval harness~~ — `python -m devmate.eval.run_ragas --mode offline` works; 52 unit tests green
10. Live retrieval eval: start qdrant, ingest repo, run `--mode live`; write chunking ADR with measured numbers
11. Full DevMate gate after any further code change
12. ~~Skills-mastery content + challenge sets for the python module~~ — done 2026-09-30 (11 topics, 11 challenge sets, SKILLS_MASTERY_MAP.md; 186 tests verified)
13. ~~Topic 39 Poetry + challenge set~~ — done 2026-10-05 (committed 04e22ca)
14. ~~Challenge 20 Patterns + dedup of 14 nested challenge dirs~~ — done 2026-10-05 (committed 5de7c8f)
15. ~~Topic 40 uv: full learning package + challenge set~~ — done 2026-10-06
16. ~~Quiz backfill: quiz.md for all 16 sets missing it (20–34, 39)~~ — done 2026-10-06
17. ~~Legacy curriculum suite repaired and promoted to gating in CI~~ — done 2026-10-06 (311 passed, 7 skipped; fixed `practice_no_solutions.py` U+00D7 SyntaxError and `18-tracking-platforms.py` artifact-after-end bug)
18. ~~Adopt uv for DevMate: `uv lock`, commit `uv.lock`, CI `uv sync --locked` + `uv audit`~~ — done 2026-10-06 (166 packages; qdrant 1.8.2 to 1.12.2 fixing CVE-2024-3829 with .search() signature verified; audit advisory with ignore-until-fixed on the no-fix CVEs)
19. ~~Single local gate: `infra/scripts/local-ci.ps1` + `infra/scripts/docs-gates.ps1`~~ — done 2026-10-06 (LOCAL CI: ALL GREEN)
20. ~~python-jose migration~~ — done 2026-10-06 by removal: jose/passlib were dead deps (imported nowhere), so no pyjwt replacement was needed; relock dropped rsa/ecdsa and their unfixable CVEs; `uv audit` now gates in CI with zero findings
21. ~~DevMate review quick wins~~ — done 2026-10-06: secret_key production guard, debug=False default, ConfigDict, pathlib import moved up, all 11 datetime.utcnow() sites to datetime.now(UTC); mypy stays 3.12 (numpy 2.5.3 stubs unparsable under 3.11, documented in pyproject)
22. The editable-install .pth pointed at the pre-rename `fullstack-ai-engineer-lab` path and broke `import devmate`; fixed by hand, and `uv sync` ownership of the venv prevents recurrence
23. Remaining review debt: split `cli/main.py` stats (115 lines) + agent dispatch table; API/agent test coverage (47% overall); `devmate/ui/` missing so compose `ui` service fails — start only needed infra

---

## Week 0 Success Criteria

- [x] DevMate lint/types/tests pass locally (ruff 0, format clean, mypy 0, pytest 52 pass as of 2026-09-30)
- [x] Offline eval harness runs and prints a metrics table (`devmate.eval.run_ragas`, 2026-09-30)
- [x] `devmate stats` CLI runs and prints repository statistics (verified 2026-09-26)
- [x] `.ai` registry system validated and gated (`tests/*/validate.ps1` × 5, wired into CI)
- [x] GitHub Actions green on `master` (CI run 36269637267, 2026-09-26)
- [x] Tests exist for the stats command (4 tests in `tests/unit/test_cli_stats.py`)
- [ ] Legacy backlog R1–R7, R9 closed (reproduce + verify each fix)
- [x] 10 prompt golden cases committed (`evaluations/prompts/golden-cases/devmate.jsonl`, 2026-09-30)
- [ ] Langfuse keys configured and one live traced `devmate ask` recorded
- [x] Offline schema tests for golden cases (`tests/unit/test_prompt_golden.py`)
- [x] `master-ai-engineering/` decision made — adopted as `docs/curriculum/` (2026-09-26)
- [x] `embeddings/`, `prompt-engineering/`, `rag-system/` no longer empty (filled 2026-09-29)
- [x] Skills-mastery gaps closed in `projects/00-core-foundations/python/` — SKILLS_MASTERY_MAP.md + 11 challenge sets (186 tests: starter fails / solution passes, 2026-09-30)

---

## Do Not Work On

- ❌ **Unanchored lectures** — curriculum content must trace to a DevMate concept or an
  interview answer (ADR-0006). No "tutorial for its own sake".
- ❌ Go / Flutter / Next.js — removed to focus on AI Engineering
- ❌ Athar / Baligh — [phase 2](../roadmap/phase-2-athar-baligh.md), after A7
- ❌ RAG implementation beyond the existing scaffold — week 2, after the eval harness exists
- ❌ Classical ML / PyTorch — deferred to week 11+ (A10)
- ❌ R8 pandas renumbering + R10 CI matrix — staged follow-ups; they risk churn this window

---

## Active Milestones

| ID | Milestone | Week | Status |
| --- | --- | --- | --- |
| A1 | CI green + `devmate stats` CLI | 0 | **Done** (CI run 36269637267) |
| A2 | LLM layer traced and costed | 1 | In Progress — Ollama path verified. Prompt golden cases + offline schema tests done 2026-09-30. Remaining: Langfuse keys + live traced `devmate ask` |
| A3 | RAG with measured eval + 2 ADRs | 2–3 | **In Progress** — offline eval harness implemented 2026-09-30 (`devmate.eval.run_ragas`); golden sets load; Hit@5 offline recorded path = 1.0; live retrieval still needs Qdrant + ingest; chunking/vector ADRs still open |
| A4 | **Deployed at a public URL** | 4 | Planned |

Full list: [`../roadmap/milestones.md`](../roadmap/milestones.md)

---

## Next Window Preview

**Week 2** (2026-10-06 → 2026-10-12) — RAG. Qdrant up, ingest this repo, live retrieval
eval with measured Hit@5, chunking ADR with numbers. DevMate `ask` end to end with
tracing. Target application date is 2026-10-12 (week 10 of the track) — portfolio
deliverables (A4 deployment) take priority over new content.

---

## Blockers

> What's preventing progress? Empty = no blockers.

- `make` is not installed on this machine — run the underlying commands directly:
  DevMate checks from `projects/04-ai-engineering/devmate/.venv`, validators via
  `powershell -File tests/<area>/validate.ps1`. Install GnuWin32 make or use WSL to
  restore `make` parity.
- Poetry 2.4.3 is installed, but the repo standard is pip-from-pyproject (see Makefile);
  CI was switched to match on 2026-09-26.

---

## Notes

- Read *AI Engineering* (Huyen) ch. 1–3 during week 1 — **after** each day's building.
- English-only from here: code, comments, commits, PRs, docs, and personal notes.
- Stuck longer than 45 minutes → log it in `mistakes.md` and move on.
