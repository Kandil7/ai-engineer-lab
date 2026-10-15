# Software Craftsmanship — Refactoring and Testing

Refactoring is behaviour-preserving restructuring under a green suite;
testing is the executable specification that makes it safe. This track
teaches the smell catalog (including LLM-era smells), the eight-move
refactoring catalog with safety steps, small-step discipline, the test
pyramid with its LLM twist, behaviour-asserting tests, doubles at the
seam, property-based and mutation testing, and the deterministic testing
discipline DevMate enforces in CI. Every FACT claim below was verified
at the cited path before this track was written.

---

## Architecture: The Test Pyramid

```
                        /\
                       /e2e\          few, thin, slow, possibly live
                      /------\        (DevMate: excluded from default run)
                     /integr. \       behind the `integration` marker
                    /----------\      (DevMate: tests/integration/, needs services)
                   /    unit    \     many, cheap, deterministic, offline
                  /--------------\    (DevMate: tests/unit/, default gate)
                 /  static gate   \   ruff + format + mypy before pytest
                /------------------\ (DevMate: .github/workflows/ci.yml)

  width = count | height = cost, flakiness, feedback time
  LLM twist: never assert on generated prose in unit tests;
  keep the deterministic bottom wide and the live top thin.
```

Each layer catches a different failure class. The lecture teaches why
inverting the pyramid — thin unit coverage under a heavy live top —
makes every refactor a gamble.

---

## Track Contents

| File | What it covers |
|------|----------------|
| `lectures/01-refactoring-and-testing-lecture.md` | 10 sections: refactoring defined, smells incl. LLM-era, eight-move catalog, small-step discipline, root cause vs symptom, test pyramid, good tests, doubles and seams, property/mutation/coverage, the LLM pyramid in practice |
| `lectures/01-refactoring-and-testing-glossary.md` | 40-term quick-reference table plus detailed definitions, each with a DevMate or exercise example |
| `quizzes/01-refactoring-and-testing-quiz.md` | 15 questions (5 Easy, 7 Medium, 3 Hard) with inline answers and explanations, score tracking, answer key |
| `exercises/01-refactoring-and-testing.py` | Offline audit engine: 8 CRF rules over source plus 4 TQ rules over tests (BAD trips all 12, GOOD raises zero), stdlib-only, deterministic |
| `README.md` | This page |

---

## What Is Grounded (FACT)

Verified at the cited paths before this track was written:

- **DevMate's gate is lint, format, types, tests, then eval:**
  `.github/workflows/ci.yml:46-77` runs ruff check, ruff format
  `--check`, mypy on `src/`, pytest with coverage, then the offline
  eval gate (`--fail-under-hit-at-5 1.0 --fail-under-mrr 0.70`).
  `infra/scripts/local-ci.ps1:37-42` mirrors the same five DevMate
  steps for local runs.
- **Ruff and mypy config live in one file:**
  `projects/04-ai-engineering/devmate/pyproject.toml:65-67` sets
  line-length 100 and target py311; `:88-110` holds the mypy block;
  `:112-120` sets the pytest default to `-m 'not integration and
  not llm'` with the `integration` marker registered for
  service-backed tests.
- **Unit and integration tests are split by marker and directory:**
  `projects/04-ai-engineering/devmate/tests/unit/` holds files such
  as `test_chunker.py`, `test_cost.py`, `test_prompt_golden.py`,
  `test_eval_harness.py`, and `test_api_happy_path.py`, while
  `projects/04-ai-engineering/devmate/tests/integration/` holds
  `test_services.py`, which needs Qdrant and Redis running.
- **The audit is executable and deterministic:** the exercise's BAD
  pack trips all twelve CRF/TQ codes (3 critical) and the GOOD pack raises
  zero; reruns are identical, the demo needs no network, and file mode
  accepts a JSON source pack (BOM-safe).

Sources: the refactoring canon this lecture operationalizes is Martin
Fowler, *Refactoring* (2nd ed., 2018), and the testing canon is Kent
Beck, *Test-Driven Development: By Example* (2002) — named as the
canon, not vendored. No `source-index` entry exists for either book
yet; the repo-grounded claims above are the verifiable half.

---

## Complements (Not Duplicates)

This track owns **safe restructuring and the test suite that pays for
it**. Adjacent territory already taught elsewhere:

- `system-design.contracts` (knowledge-registry) — four-part component
  contracts with compatibility and migration:
  `projects/00-core-foundations/python/10-system-design/01-component-contracts`.
  Contracts state what a component promises; this track's tests prove
  the promise still holds after restructuring.
- The Reliability track (`projects/06-devops/reliability/`) —
  timeouts, retries, breakers, and idempotency as *runtime* mechanics.
  This track's integration layer is where those mechanics get their
  service-backed tests behind the `integration` marker.
- The evaluation material in DevMate (`test_eval_harness.py` and the
  offline RAGAS gate) — retrieval quality metrics. This track treats
  the eval gate as the thin top of the pyramid, not as a unit test.

---

## Verification

Run from the repository root:

```powershell
python -m py_compile projects\05-system-design\software-craftsmanship\exercises\01-refactoring-and-testing.py
python projects\05-system-design\software-craftsmanship\exercises\01-refactoring-and-testing.py
powershell -NoProfile -ExecutionPolicy Bypass -File tests\repo-structure\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests\knowledge\validate.ps1
```

Expected: compile exits 0; the demo exits 0 with the BAD pack tripping
all 12 CRF/TQ codes (3 critical) and the GOOD pack raising zero
findings; both validators exit 0. The exercise is stdlib-only, offline,
and deterministic — reruns are identical.

---

*AI Engineer Lab — System Design track, software-craftsmanship lane.*
