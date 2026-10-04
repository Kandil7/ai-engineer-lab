# 🏗️ Phase 10: System Design

> **The architecture layer** — contracts between components, queues and
> workflows, consistency and staleness, failure modes and resilience, and
> Architecture Decision Records. Every topic is built around the Athar-style
> question-and-answer pipeline so the theory lands on a real system.

---

## Why this phase exists

The other phases teach components (Python, databases, APIs). This phase teaches
the **agreements and failure stories between them**:

- What the importer *promises* the indexer (component contracts).
- What happens when the embedder is slow and jobs back up (queues).
- What "the index is older than the source" means and how it recovers
  (consistency).
- What happens when a worker dies mid-job (failure modes).
- Why PostgreSQL is the source of truth and the vector index is not backed up
  (ADRs).

The skills-map mastery criterion: **you can explain what happens if a worker
fails or the index becomes older than the source** — as a designed story with
detections and runbooks, not a shrug.

---

## Topics

| # | Topic | Core question | Mastery proof |
|---|-------|---------------|---------------|
| **01** | `01-component-contracts/` | What do producer and consumer promise each other? | a producer-side contract test fails at CI when the schema drifts |
| **02** | `02-queues-and-workflows/` | How does slow work survive crashes without duplicating? | redelivered job is a no-op; poison job reaches the DLQ |
| **03** | `03-consistency-and-staleness/` | What is truth, what is derived, and what happens when they disagree? | drift is a number; rebuild restores healthy; late updates are rejected |
| **04** | `04-failure-modes-and-resilience/` | What happens when each component breaks? | FMEA table + the designed answer to the mastery question |
| **05** | `05-architecture-decision-records/` | How do decisions survive the people who made them? | a validated ADR with alternatives and an enforcement link |

**Recommended order:** 01 → 02 → 03 → 04 → 05. Topic 04 answers the mastery
question using 02 and 03; topic 05 records the decisions 01–04 produce.

---

## Challenge sets

Every topic has a Bronze/Silver/Gold practice set in `challenges/`:

| Challenge | Measured guard that separates naive from correct |
|---|---|
| `01-component-contracts` | pairwise field comparison is O(n²) — fails the budget |
| `02-queues-and-workflows` | per-job result histories blow the 8 MB ceiling |
| `03-consistency-and-staleness` | arrival-order apply lets old overwrite new |
| `04-failure-modes-and-resilience` | run-then-check timeouts invoke the handler |
| `05-architecture-decision-records` | per-action deep copies blow the 8 MB ceiling |

Run each with `python -m pytest challenges/<name>/test_challenge.py -q` (starter
fails with `NotImplementedError` until solved) and validate the reference with
`$env:CHALLENGE_USE_SOLUTION = "1"` first.

---

## Mastery criteria

| Question | Where answered | Evidence you can produce |
|---|---|---|
| What do producer and consumer promise? | topic 01 | a producer-side contract test fails at CI on schema drift |
| How does slow work survive crashes without duplicating? | topic 02 | redelivered job is a no-op; poison job reaches the DLQ |
| What happens when truth and index disagree? | topic 03 | drift is a number; rebuild restores healthy; late updates rejected |
| What happens when a worker fails / the index goes stale? | topic 04 | the designed story: detections, blast radii, runbooks |
| How do decisions survive the people who made them? | topic 05 | a validated ADR with alternatives and an enforcement link |

The master answer to the Athar question — *what happens if a worker fails or the
index becomes older than the source* — is `04-failure-modes-and-resilience`
section 7 of the lecture, backed by the state machine in topic 03.

---

## Each topic directory contains

- `NN-topic-name.py` — self-contained exercise (run `python NN-topic-name.py`,
  verify with `--verify`)
- `NN-topic-name-lecture.md` — detailed lecture with real use cases and
  best-practice checklists
- `NN-topic-name-glossary.md` — quick-reference table + detailed definitions

All exercises run on the standard library only — no server, no network.

---

## How this phase connects to the rest

| Phase | Connection |
|---|---|
| `02-advanced-python` | topics 35–38 (Unicode, SoC, review, test strategy) feed topics 01–04 |
| `04-databases` | migrations (11) and backup (07) provide the truth/derived mechanics |
| `05-web-frameworks` | FastAPI resilience, caching, background jobs are the implementation layer |
| `08-mlops` / `09-genai` | end-to-end pipelines where these contracts apply |

See `SKILLS_MASTERY_MAP.md` at the module root for the full cross-reference.

---

*Part of the AI Engineer Lab — `projects/00-core-foundations/python/`*
