# Current Focus — Execution Window

> What to work on RIGHT NOW. Update weekly. Be specific — this replaces decision fatigue.
>
> ⚠️ A staleness gate fails CI if this file is more than 8 days old: `make fresh-check`
> locally and the Tracking freshness step in `.github/workflows/ci.yml`.

**Last updated:** 2026-09-26

---

## Active Window

**Week 0 (cont.)** — 2026-09-26 → 2026-09-28 (weekend sprint)

**Plan:** [Active Track — 10-Week AI Engineer](../roadmap/active-track-10-week.md)
(adopted 2026-08-02 by [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md))

**Project:** DevMate — `projects/04-ai-engineering/devmate/`

**Content track:** [ADR-0006](../decisions/0006-adopt-master-ai-engineering-curriculum.md)
lifted the lecture moratorium, but the `projects/04-ai-engineering/master-ai-engineering/`
module it names does not exist yet, and `embeddings/`, `prompt-engineering/`, `rag-system/`
are empty directories (0 files each, verified 2026-09-26). Decide: create the module or
retire the task — do not leave it dangling.

---

## Main Goal

Finish Week 0 debt: the workspace registry system is now gated in CI, DevMate packaging
and the DB layer are repaired, and lint/types/tests pass locally. Remaining: legacy
Python baseline repair and the curriculum module decision above.

---

## Today's Tasks

1. DevMate lint/types/tests pass locally — ruff, ruff format, mypy, pytest verified 2026-09-26
2. Push to `master` and confirm GitHub Actions green (new `workspace` job + pip-based `devmate` job)
3. Repair Tier 0 backlog R1–R7 + R9 (`../../projects/00-core-foundations/python/admin/mastery-plan/10-remediation-backlog.md`)
4. Decide the **Master AI Engineering** module: create `master-ai-engineering/` with the 12
   topics, or fold the content into the existing `projects/04-ai-engineering/` tracks
5. Fill the empty modules: `embeddings/`, `prompt-engineering/`, `rag-system/`
6. Write DevMate unit tests for the stats command (no test covers `cli/main.py` yet)

---

## Week 0 Success Criteria

- [x] DevMate lint/types/tests pass locally (ruff 0, mypy 0, pytest 19 → 23 pass)
- [x] `devmate stats` CLI runs and prints repository statistics (verified 2026-09-26)
- [x] `.ai` registry system validated and gated (`tests/*/validate.ps1` × 5, wired into CI)
- [ ] GitHub Actions green on `master`
- [ ] Tests exist for the stats command
- [ ] Legacy backlog R1–R7, R9 closed (reproduce + verify each fix)
- [ ] `master-ai-engineering/` decision made (created or retired)
- [ ] `embeddings/`, `prompt-engineering/`, `rag-system/` no longer empty

---

## Do Not Work On

- ❌ **Unanchored lectures** — curriculum content must trace to a DevMate concept or an
  interview answer (ADR-0006). No "tutorial for its own sake".
- ❌ Go / auth-service — paused under ADR-0004, lives in the long track
- ❌ Flutter / Next.js — paused
- ❌ Athar / Baligh — [phase 2](../roadmap/phase-2-athar-baligh.md), after A7
- ❌ RAG implementation beyond the existing scaffold — week 2, after the eval harness exists
- ❌ Classical ML / PyTorch — deferred to week 11+ (A10)
- ❌ R8 pandas renumbering + R10 CI matrix — staged follow-ups; they risk churn this window

---

## Active Milestones

| ID | Milestone | Week | Status |
| --- | --- | --- | --- |
| A1 | CI green + `devmate stats` CLI | 0 | In Progress |
| A2 | LLM layer traced and costed | 1 | Planned |
| A3 | RAG with measured eval + 2 ADRs | 2–3 | Planned |
| A4 | **Deployed at a public URL** | 4 | Planned |

Full list: [`../roadmap/milestones.md`](../roadmap/milestones.md)

---

## Next Window Preview

**Week 1** (2026-09-29 → 2026-10-05) — LLM layer. Claude API with streaming, structured
outputs, retries. **Langfuse tracing and cost tracking wired in from day one**, not at the
end. First 10 golden cases. `devmate ask "<question>"` working end to end.

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
