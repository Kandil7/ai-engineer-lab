# Clean Architecture and Hexagonal Architecture

Ports and adapters for AI systems: domain and application layers that depend
inward only, ports as Protocols defined where they are used, thin adapters
for Qdrant and model runtimes, use cases such as AnswerQuestion tested
against fakes, and pipelines as explicit step lists. The worked domain is an
Islamic-corpus RAG system with Retriever, Generator, Tokenizer,
DocumentRepository, Embedder, CitationPolicy, and ExperimentTracker ports.
Every structural claim is checked by eight executable rules
(HEX001-HEX008). General guidance follows the clean and hexagonal
literature; repository paths cited below were verified before writing.

---

## Architecture: Where the Layers Live

```
                    ┌──────────────────────────────┐
                    │         interfaces           │  FastAPI, CLI, UI
                    │  (adapters driving inward)   │  calls use cases
                    └──────────────┬───────────────┘
                                   │ depends inward
                    ┌──────────────▼───────────────┐
                    │        infrastructure        │  Qdrant, torch,
                    │  (driven adapters + config)  │  MLflow, Redis
                    └──────────────▲───────────────┘
                                   │ implements port
                    ┌──────────────┴───────────────┐
                    │          application         │  AnswerQuestion,
                    │  use cases + port Protocols  │  ingest, evaluate
                    └──────────────┬───────────────┘
                                   │ depends inward
                    ┌──────────────▼───────────────┐
                    │            domain            │  entities, value
                    │  no torch, no Qdrant, no API │  objects, policies
                    └──────────────────────────────┘

  dependency rule: outer layers depend inward; domain depends on nothing.
  ports live inside; adapters live outside and implement ports.
```

Each ring blocks a different shortcut. The lecture shows why skipping any
ring pushes model names, URLs, and client objects into the use case.

---

## Track Contents

| File | What it covers |
|------|----------------|
| `lectures/01-hexagonal-architecture-lecture.md` | 10 concepts: layers, ports, AnswerQuestion end to end, SOLID, patterns, pipelines, config seam, testing, failures, decision table |
| `lectures/01-hexagonal-architecture-glossary.md` | 35-term quick table plus detailed definitions with Islamic-corpus examples |
| `quizzes/01-hexagonal-architecture-quiz.md` | 15 questions (5 Easy, 6 Medium, 4 Hard) with answers, score tracking, answer key |
| `exercises/01-hexagonal-architecture.py` | Offline checker: 8 HEX rules over module specs (BAD trips all 8, GOOD is clean) plus Retriever ports demo |
| `README.md` | This page |

---

## What Is Grounded (FACT)

Verified at the cited paths before this track was written:

- **Template structure is reused:** the section order here mirrors
  `projects/05-system-design/domain-modeling/README.md:44-52`
  and the lecture header style mirrors
  `projects/05-system-design/domain-modeling/lectures/01-domain-modeling-lecture.md:1-56`.
- **Exercise pattern is reused:** dataclass findings, marker-based lines,
  BAD versus GOOD packs, and the exit convention follow
  `projects/06-devops/reliability/exercises/01-reliability-patterns.py:1-80`.
- **The audit is executable and deterministic:** the exercise BAD pack
  trips all eight rules (5 critical, 3 warning) and the GOOD pack raises
  zero; reruns are identical, the demo needs no network or GPU, and file
  mode accepts JSON with utf-8-sig.

Sources: the hexagonal literature this track operationalizes is Alistair
Cockburn, Hexagonal Architecture (2005), and Robert C. Martin, Clean
Architecture (2017), named as canon, not vendored.

---

## Complements (Not Duplicates)

This track owns **layering and seams**. Adjacent material stays separate:

- `domain-modeling` track (knowledge-registry) — aggregates, events, and
  specifications inside the domain; this track assumes that model exists
  and keeps frameworks outside it.
- Reliability patterns (`projects/06-devops/reliability/`) — retry,
  breaker, and idempotency mechanics; this track wires them as adapters
  behind ports instead of re-teaching the state machines.
- Component contracts — interface shape between components; this track
  places those interfaces at the port boundary.

---

## Verification

Run from the repository root:

```powershell
python -m py_compile projects\05-system-design\clean-hexagonal-architecture\exercises\01-hexagonal-architecture.py
python projects\05-system-design\clean-hexagonal-architecture\exercises\01-hexagonal-architecture.py
powershell -NoProfile -ExecutionPolicy Bypass -File tests\repo-structure\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests\knowledge\validate.ps1
```

Expected: compile exits 0; the demo exits 0 with BAD tripping all 8 rules
and GOOD raising zero; both validators exit 0. Stdlib only, offline,
deterministic.

---

*AI Engineer Lab — System Design track, clean-hexagonal-architecture lane.*
