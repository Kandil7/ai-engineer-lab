# Full Learning Content — Completion Strategy (12 Axes)

> How to bring every lecture to full detail, one axis at a time, using the workspace's
> existing conventions. Companion to [`learning-strategy.md`](learning-strategy.md) (the
> study loop) and `docs/product/IMPLEMENTATION-GUIDE.md` (the lecture standard).

**Last updated:** 2026-10-01

---

## 1. What "complete" means

Two standards, applied together.

### 1a. The lecture standard (per `.md`)

A lecture is "full detail" when it follows `IMPLEMENTATION-GUIDE.md`:

```text
# <Module> NN: <Topic>
## Topic Overview              (2-3 paragraphs: what, why, what is hard)
## Learning Objectives         (5-7 bullets)
## Prerequisites               (1-3 bullets)
## 1..7. <Concept>             (each: idea, analogy, complete code, when it fails,
                               connection to the exit test; ### subsections)
## Real-World Application
## Common Mistakes             (5-7, with examples)
## Key Takeaways               (5 bullets)
## Self-Check Questions        (3-6)
## Further Reading / Connections
```

Target: **250-400 lines / at least 6.5 KB**, versus the ~90-line abbreviated form.
The physical-line proxy undercounts files whose paragraphs are unwrapped; judge by
section coverage and character count as well.

### 1b. The teaching-unit standard (per module folder)

A module is "complete" when the folder holds all four artifacts:

| Artifact | File pattern | Shape |
| --- | --- | --- |
| Lecture | `<topic>-lecture.md` | the standard above |
| Glossary | `<topic>-glossary.md` | Quick Reference Table + Alphabetical Glossary |
| Quiz | `<topic>-quiz.md` | Score Tracker + 8-10 questions (A/B/C/D) + reveal + scoring guide |
| Exercise | `<topic>.py` | runnable; `--verify` self-checks pass offline (stdlib where possible) |

The exercise's `--verify` is the proof the content is executable, not just prose.

### 1c. The verification gate

Every completed unit must pass:

```powershell
python <topic>.py --verify                 # exit 0
powershell -File tests/registries/validate.ps1   # and the other four validators
# plus: 0 broken relative links under docs/
```

---

## 2. Where the content stands (audit 2026-10-01)

There are **598 lecture files**. Every one has a glossary. Quizzes exist in **three
layouts**, so a same-folder check under-counts:

- next to the lecture: `NN-topic-quiz.md` (the expanded roadmap modules, plus `08-mlops`)
- in a sibling `quizzes/` folder: `agents`, `ai-automation`, `security` (`NN-topic-quiz.md`),
  `fastai-deep-learning` (`NN-topic.md`)
- in a sibling `challenges/` folder: `python/10-system-design` (`quiz.md`)

| Measure | Count |
| --- | --- |
| Lecture files | 598 |
| With a glossary | 598 (100%) |
| With a quiz in some layout | ~137 |
| **Complete units (lecture + glossary + quiz + exercise)** | ~137 |
| Without any quiz | ~461 (essentially all of `00-core-foundations/python`) |
| Thin lectures (< 4 KB) | 97, all in `00-core-foundations/python` |

The real gap is the **legacy `00-core-foundations/python` curriculum** (481 lectures),
where 475 lack a quiz and 97 are thin. The roadmap-critical modules and the
`agents`/`ai-automation`/`security`/`fastai`/`system-design` areas are already complete
under one of the three layouts.

Progress log:
- 2026-10-01 — `python/08-mlops` completed: 16 quizzes (`quizzes/NN-topic-quiz.md`).
- 2026-10-01 — `python/09-genai` completed: 25 quizzes (`quizzes/NN-topic-quiz.md`).

The remaining work is therefore: **expand 97 thin lectures** and **write ~461 quizzes**,
dominated by the legacy Python curriculum.

---

## 3. The 12 axes → modules → what is missing

| Axis | Modules | State | What to complete |
| --- | --- | --- | --- |
| 1 Python to production | `python/01-core-python`, `02-advanced-python` | thin subset | expand thin lectures; add quizzes |
| 2 CS / Git / Linux / SQL | `git-linux`, `ds-algo`, `python/04-databases`, `postgres-design`, `redis-cache` | mostly complete | quizzes for `python/04-databases`; networking unit is absent |
| 3 Math / ML | `python/07-machine-learning`, `applied-ml` | `applied-ml` complete | quizzes + expand thin ML lectures |
| 4 Backend for AI | `python/05-web-frameworks/fastapi`, `devmate` | thin subset | expand thin lectures; add quizzes |
| 5 Data engineering | `data-engineering`, `athar-lab` | complete | new units (versioning, manifest) |
| 6 LLM / RAG | `rag-system`, `arabic-nlp`, `embeddings`, `prompt-engineering`, `model-serving`, `fine-tuning`, `agents`, `ai-automation` | roadmap set complete | quizzes for `agents`, `ai-automation` |
| 7 Evaluation | `ai-evaluation` | complete | — |
| 8 Inference | `model-serving` | complete | benchmark unit (new) |
| 9 DevOps / MLOps | `python/08-mlops`, `06-devops` | thin subset | expand thin lectures; add quizzes |
| 10 Operations / SRE | `python/10-system-design` | lectures complete | quizzes + exercises |
| 11 Security | `python/09-genai/*safety*`, `security` | thin subset | expand thin; quizzes for `security` |
| 12 System design | `python/10-system-design` | lectures complete | quizzes + exercises |

---

## 4. How to complete one unit (the pipeline)

Run this loop for one `<axis>/<module>/` at a time.

1. **Pick the unit** by the axis order in §5. Read the existing `<topic>-lecture.md` and
   the `<topic>.py`.
2. **Expand the lecture** to the §1a standard. Preserve the existing content; add the
   missing sections (prerequisites, numbered concepts with code and failure modes,
   real-world application, common mistakes, key takeaways, self-check, further reading).
3. **Write or refresh the glossary** (`<topic>-glossary.md`) to the §1b shape, using the
   sibling modules as the format reference.
4. **Write the quiz** (`<topic>-quiz.md`) with 8-10 questions, a score tracker, reveal
   blocks, and a scoring guide. Mix difficulty; tie the hard ones to the exit test.
5. **Write or extend the exercise** (`<topic>.py`) so it runs offline with `--verify`
   assertions; or, if an existing exercise exists, add the missing assertions.
6. **Run the gate** (§1c). Fix until green.
7. **Mark progress** in `docs/roadmap/production-skills-matrix.md` if the unit closes an
   axis gap.

### Order within a unit

Lecture, then glossary, then quiz, then exercise. The quiz and exercise are derived from
the lecture's concepts, so the lecture first keeps them consistent.

---

## 5. The order of work

The gap is the legacy `00-core-foundations/python` curriculum. Work it module by module,
smallest and most roadmap-relevant first. Each module = add a quiz per lecture (matching
its existing exercise), then expand any thin lecture in it.

| Order | Module | Lectures | Thin | Note |
| --- | --- | --- | --- | --- |
| done | `python/08-mlops` | 16 | 0 | 16 quizzes added 2026-10-01 |
| 1 | `python/09-genai` | 25 | 0 | quizzes only; exercises exist |
| 2 | `python/06-data-structures-algorithms` | 20 | 1 | quizzes + 1 expansion |
| 3 | `python/02-advanced-python` | 38 | 0 | quizzes only |
| 4 | `python/07-machine-learning` | 40 | 9 | quizzes + 9 expansions |
| 5 | `python/01-core-python` | 53 | 1 | quizzes + 1 expansion |
| 6 | `python/05-web-frameworks` | 74 | 20 | quizzes + 20 expansions |
| 7 | `python/04-databases` | 73 | 31 | quizzes + 31 expansions |
| 8 | `python/03-libraries` | 137 | 35 | quizzes + 35 expansions (largest) |

After the legacy curriculum, the two **new units** the roadmap needs are axis 5
(dataset/embedding/index versioning manifest) and axis 8 (inference benchmark).

### Batching

One module (4-10 files) per batch. A batch is done when its units pass the gate and are
documented. Do not mix axes in a batch; context switching costs more than the parallelism
gains.

---

## 6. Per-unit checklist

```text
[ ] <topic>-lecture.md has all 9 sections, >= 250 lines / 6.5 KB
[ ] <topic>-glossary.md has the quick table + alphabetical entries
[ ] <topic>-quiz.md has 8-10 questions + reveal + scoring guide
[ ] <topic>.py runs offline and `--verify` exits 0
[ ] no broken relative links
[ ] five validators exit 0
[ ] skills matrix row updated if the unit closes an axis gap
```

---

## 7. Conventions

- **No frontmatter on lecture/glossary/quiz/exercise files.** They are content, not
  governed `.ai` assets.
- **Match the neighbors.** Each area has a format (e.g. `applied-ml` uses the plain
  `## Topic Overview` style; older modules may use emoji headers). Copy the nearest
  sibling rather than inventing a layout.
- **Stay grounded in the repo.** Anchor examples to Athar, DevMate, Qdrant, or the local
  hardware where the topic allows.
- **Do not fabricate measurements.** If a lecture claims a number, it must come from a run.
- The exercises self-verify; there is no repo-wide pytest collection for `projects/`, so
  `--verify` plus the validators are the gate.

---

*Created 2026-10-01. Update the audit table in §2 when a block of units completes.*
