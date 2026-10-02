# Operating Manual — Implementation Guide

How to use the AI Learning Operating Manual in daily practice. This guide maps
the manual's principles to concrete files, commands, and standards — the
operating layer between the manual and the work.

It is the practical companion to two docs, and it does not duplicate them:

- [`ai-learning-operating-manual.md`](ai-learning-operating-manual.md) — the
  principles and the agent roles.
- [`full-content-completion-strategy.md`](full-content-completion-strategy.md) —
  the completion plan, the per-unit standard, and the audit.

**Last updated:** 2026-10-02

---

## 1. Quick Reference

| What | Where | When |
|------|-------|------|
| The manual (principles) | `docs/product/ai-learning-operating-manual.md` | Reference |
| Completion plan + per-unit standard | `docs/product/full-content-completion-strategy.md` | Before authoring content |
| Study loop | `docs/product/learning-strategy.md` | Daily |
| Scope boundaries | `docs/product/scope-definition.md` | Before adding work |
| What to work on now | `docs/tracking/current-focus.md` | Weekly (has an 8-day freshness gate) |
| Roadmap evidence scoreboard | `docs/roadmap/production-skills-matrix.md` | When a unit closes a gap |
| Agent prompts (canonical) | `.ai/prompts/` | Before each AI session |
| Workflows (canonical) | `.ai/workflows/` | Every session |
| Superseded copies | `docs/product/agents/`, `docs/product/workflows/` | Reference only — edit `.ai/` instead |
| Templates | `templates/` | When creating artifacts |
| Registries (source of truth) | `registries/` | After any prompt/workflow/registry edit |
| Teaching units | `projects/*/` (lecture + glossary + quiz + exercise) | When authoring content |
| Learning artifacts | `docs/learning/` | After learning sessions |
| Mistakes | `mistakes.md` (in project folder) | After a mistake |
| Reviews | `ai-review.md` (in project folder) | After a feature |
| Debugging | `debugging-session.md` (in project folder) | After a bug |
| Source learning | `docs/learning/source-summaries/` | After reading a source |
| ADRs | `docs/decisions/` | After a decision |

---

## 2. Session Workflow

### Starting

1. Open `.ai/workflows/feature/01-plan.md` (the canonical session entry point).
2. Fill in the Session Goal card.
3. Pick the right role from `.ai/prompts/roles/`.
4. Compose it in this order: `system/workspace-governor.md` → role → task
   (optional) → `system/output-format-rules.md` → critic or repair (optional).
   Never restate the format rules; reuse `output-format-rules.md`.
5. Start with the smallest question.

The day loop is `/quickstart` → work → `/test` → `/wrapup`. Recovery is
`/checkpoint`, `/resume`, `/status`, `/gpu`. Quick capture is `/session-log`.

### During

Follow the 7-phase workflow:

1. **Understand** — Learning Coach.
2. **Plan** — Project Planner.
3. **Write** — write the code yourself (the big block).
4. **Hints** — Pair Programmer if blocked.
5. **Review** — Code Reviewer.
6. **Debug** — Debugging Specialist if broken.
7. **Reflect** — write the artifact.

### Ending

1. Create at least one artifact.
2. Write the closing reflection.
3. Run the verification gate (§6).
4. Identify the next step.

Commit only when the user asks. Approval checkpoints: plan approved before
build, architecture approved before large implementation, review complete before
done, ADR accepted before any irreversible change.

---

## 3. Agent Selection

| Situation | Agent | Prompt location |
|-----------|-------|-----------------|
| Starting a new topic | Learning Coach | `.ai/prompts/roles/learning-coach.md` |
| Breaking down a feature | Project Planner | `.ai/prompts/roles/project-planner.md` |
| Stuck on the next step | Pair Programmer | `.ai/prompts/roles/pair-programmer.md` |
| Code works but is ugly | Code Reviewer | `.ai/prompts/roles/code-reviewer.md` |
| Something is broken | Debugging Specialist | `.ai/prompts/roles/debugging-specialist.md` |
| Reading docs/repo/article | Source Learning Agent | `.ai/prompts/roles/source-learning-agent.md` |
| Designing system boundaries | System Architect | `.ai/prompts/roles/system-architect.md` |
| Recording a decision | Principal System Designer | `.ai/prompts/roles/principal-system-designer.md` |

The seven role prompts are the canonical set. The `docs/product/agents/` copies
are superseded; edit `.ai/` and re-run `tests/prompts/validate.ps1`.

---

## 4. The Four-Level Help Model

Before asking for help, identify the level:

| Level | Symptom | What to ask |
|-------|---------|-------------|
| **1. Explain** | "I don't understand" | Explain simply + example |
| **2. Hint** | "I know X but stuck on Y" | Smallest hint, next step |
| **3. Review** | "I wrote it, check it" | Review, identify weaknesses |
| **4. Rescue** | "I tried everything" | Minimal working example |

**After rescue:** rewrite the logic from memory. If you can't, you didn't
learn it.

---

## 5. Writing Teaching Units

A teaching unit is a topic folder. It is complete only when it holds **all four**
artifacts — the lecture is not the whole unit.

### 5.1 The four artifacts

| Artifact | File pattern | Shape |
|----------|--------------|-------|
| Lecture | `<topic>-lecture.md` | §5.2 |
| Glossary | `<topic>-glossary.md` | §5.3 |
| Quiz | `<topic>-quiz.md` (or `quizzes/`, `challenges/NN/quiz.md`) | §5.4 |
| Exercise | `<topic>.py` | §5.5 |

The exercise's `--verify` is the proof the content is executable, not just prose.

### 5.2 The lecture standard

Two title forms are in use; match the module's neighbors:

- Module-first: `# Data Engineering 08: Batch vs Streaming`
- Slash form: `# 07-machine-learning — 41: CNNs — The Image Learner`

Sections are **topic-adaptive**: start from the list below and add depth where
the topic genuinely needs it (extra concepts, a worked example, history,
multi-domain coverage). Do not pad; do add where warranted.

```markdown
## Topic Overview            (2-4 paragraphs: what, why, what is hard)
## Learning Objectives       (5-8 bullets)
## Prerequisites             (a table or 1-3 bullets, with links)
## 1..N. <Concept>           (each: the idea, a real-world analogy, a complete
                             code example, when it works / when it fails,
                             the connection to the exit test)
## Real-World Application    (where this shows up in production)
## Common Mistakes to Avoid  (5-7 items, each with WRONG / CORRECT code)
## Best Practices            (8-10 numbered items)
## Complexity and Cost       (a table: operation | time | space | notes)
## AI Engineering Relevance  (a table mapping concept -> use)
## Key Takeaways             (5-7 bullets)
## Self-Check Questions      (5-8 questions)
## Summary                   (a table: concept | description)
## Quick Reference           (a table: task | idiom)
## Further Reading / Connections (links to sibling units and official docs)
## Next Steps                (the next unit, and the continuation)
```

Rules:

- **Target length:** 400+ hard-wrapped lines and at least 6.5 KB. The strategy
  doc's `250–400` band is the floor; new units run 400+. A lecture under 4 KB is
  **thin** and is a work item.
- **No frontmatter.** Lecture, glossary, quiz, and exercise are content, not
  governed `.ai` assets.
- **Hard-wrap prose at ~72 characters** to match the neighbors. Do not reindent
  code or tables.
- **Ground examples** in Athar, DevMate, Qdrant, or the local RTX 5000 where the
  topic allows; keep generic ML content generic where that is the module's style.
- **Do not fabricate measurements.** A claimed number must come from a run.

### 5.3 The glossary standard

```markdown
# <Topic> — Glossary <NN>

Companion lecture: `<topic>-lecture.md`

## Quick Reference Table        (Term | Category | One-line definition)
## Alphabetical Glossary        (### term: Definition, Example, Related)
## Key Concepts Summary
## Practice Terms              (match-the-term, with answers at the bottom)
```

### 5.4 The quiz standard

```markdown
# <Module> NN: <Topic> — Quiz

> **Topic Overview**: one line.

## Score Tracker               (Questions Answered / Correct / Score)
## Questions                   (8-10, labeled Easy/Medium/Hard)
<details><summary>Reveal Answer</summary>**B.** short rationale.</details>
## Answer Key                  (a table)
## Scoring Guide               (score band | reading)
```

Tie the hard questions to the roadmap exit test, not to trivia.

### 5.5 The exercise standard

- Runnable offline; `--verify` self-checks pass with exit code 0.
- Layout varies by area. When a library is missing, demonstrate the concept with
  what is installed and **say so in the docstring** (see the ML transfer-learning
  and JAX units).
- Print a short summary and an `ALL CHECKS PASSED` line from the verifier.

### 5.6 The per-unit authoring loop

Run this for one module (or one sub-folder) at a time.

1. **Pick the unit** and read the existing lecture and exercise.
2. **Expand the lecture** to §5.2; preserve existing content, add the missing
   sections.
3. **Refresh the glossary** to §5.3.
4. **Write the quiz** to §5.4.
5. **Confirm or extend the exercise** so it runs offline with `--verify`.
6. **Run the gate** (§6) and fix until green.
7. **Update the scoreboard** (`production-skills-matrix.md`) and the progress log
   in the strategy doc if the unit closes a gap.

Order within a unit: **lecture → glossary → quiz → exercise**. The quiz and
exercise derive from the lecture, so writing the lecture first keeps them
consistent.

Batching: one module per batch; do not mix axes. Parallelize only after the
format is locked by a first sub-batch.

### 5.7 Anti-patterns

- **Thin lecture.** Under 4 KB, missing sections, no code, no analogy.
- **Lecture-only unit.** No glossary, quiz, or `--verify` exercise.
- **Invented measurements.** A number with no run behind it.
- **Frontmatter on content files.** They are not governed `.ai` assets.
- **Inventing a layout.** Copy the nearest sibling; do not invent one.
- **Broken relative links.** Every relative Markdown link must resolve to an
  existing file.

---

## 6. The Verification Gate

A unit is done when its artifacts pass the gate. There is no repo-wide pytest for
`projects/`; the content gate is `--verify` plus the workspace validators.

### 6.1 Content gate

- Every touched exercise runs offline: `python <topic>.py --verify` exits 0.
- No broken relative links under `docs/` and in the new unit.
- `ruff check` and `ruff format --check` clean on any Python you touched.

### 6.2 DevMate gate

Working directory `projects/04-ai-engineering/devmate/`, python at
`.venv/Scripts/python.exe`:

```powershell
& .venv/Scripts/python.exe -m ruff check .
& .venv/Scripts/python.exe -m ruff format --check .
& .venv/Scripts/python.exe -m mypy src/
& .venv/Scripts/python.exe -m pytest -q --cov=devmate --cov-report=term-missing
```

`llm`-marked tests need a real key and never run in CI. Unit tests need no key.

### 6.3 Workspace validators

All five must exit 0; warnings fail the suite:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/prompts/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/workflows/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/templates/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/registries/validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests/repo-structure/validate.ps1
```

Run `tests/registries/validate.ps1` after any prompt, workflow, or registry edit.

### 6.4 Docs gates

Mirrored in CI:

- No broken relative links under `docs/` (excluding `docs/plan/archive/`).
- `docs/tracking/current-focus.md` carries a `**Last updated:**` stamp no older
  than 8 days.

### 6.5 CI jobs

`.github/workflows/ci.yml` has five jobs:

| Job | Blocking? | What it runs |
|-----|-----------|--------------|
| `devmate` | yes | ruff, ruff format, mypy, pytest |
| `workspace` | yes | the five validators |
| `docs` | yes | link check + freshness stamp |
| `integration` | disabled (`if: false`) | DevMate against Qdrant + Redis |
| `legacy-lint` | advisory (`continue-on-error`) | ruff on the legacy curriculum |

The legacy curriculum has known shadowing failures; it is advisory until
repaired. Do not treat a green `legacy-lint` as content correctness.

---

## 7. Measuring Progress

Track these weekly (habits):

- [ ] Sessions completed (target: 5/week)
- [ ] Artifacts created (target: 5/week)
- [ ] Code written by you (target: >70% of lines)
- [ ] Mistakes recorded (target: 2-3/week)
- [ ] Gaps closed (from `mistakes.md`)

But habits are not the bar. The evidence bar is the strategy doc's rule: a
roadmap section is complete only when **both** hold — the concept is taught in a
full-detail unit, **and** a proof artifact exists that the matrix can cite (a
path, a passing test, a measured number, a URL, or an ADR). Study without an
artifact is not completion; an artifact without teaching is not either.

The scoreboard is `docs/roadmap/production-skills-matrix.md`.

---

## 8. Integration with Existing Systems

| System | How it connects |
|--------|-----------------|
| `.ai/prompts/` | 21 canonical prompts in 5 layers (system, roles, tasks, critics, repair); `docs/product/agents/` copies are superseded |
| `.ai/workflows/` | 21 workflows in 5 tracks (feature, debugging, learning, architecture, evaluation) |
| `registries/` | 6 YAML inventories; the source of truth, not the docs |
| `templates/` | 16 templates registered in `template-registry.yaml` (including `mistakes`) |
| CI validators | Artifacts follow template structure; the five validators gate `.ai` and structure |
| `/session-log` | Quick capture from any session |
| `/document-project` | Full documentation sweep via the `documenter` agent |
| `/spec-*` | Spec-driven development: charter → feature spec + scorecard → verify |

After editing any config file: restart opencode, then run
`node ~/.config/opencode/scripts/validate-config.mjs`.

---

## 9. Operating Mistakes to Avoid

1. **Treating a lecture as the whole unit.** The unit is four artifacts.
2. **Skipping the gate.** Run `--verify` and the five validators before "done".
3. **Editing the superseded copies.** Edit `.ai/` and the registries, not
   `docs/product/agents/` or `docs/product/workflows/`.
4. **Hand-editing generated indexes.** `INDEX.md`, `decision-log.yaml`, and
   `review-log.yaml` are owned by their scripts.
5. **Letting `current-focus.md` go stale.** The 8-day gate will fail CI.
6. **Claiming a number you did not measure.** Label FACT, INFERENCE, and
   RECOMMENDATION honestly.
7. **Committing without being asked.** The user decides on commits and pushes.
