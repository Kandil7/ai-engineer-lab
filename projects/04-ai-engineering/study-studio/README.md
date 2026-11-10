# Study Studio

An offline, single-file reading and review environment for one chapter of
technical material, built for an Arabic-speaking AI engineer who wants to
master the chapter and read English more fluently at the same time.

Each studio is one `.html` file. Open it by double-clicking. No network,
no server, no install, no external fonts or images.

---

## What is here right now

Phase 0: **the data contract**. The engine that consumes it is Phase 1.

```
schema/chapter.schema.json      the contract, JSON Schema 2020-12
schema/example-chapter.json     a synthetic chapter that satisfies it
scripts/validate_chapter.py     the gate that keeps a chapter honest
docs/STUDIO-SPEC.md              the decisions and why they were made
```

The contract is written before the engine on purpose. A studio that
cannot express a chapter in the contract is a studio that needs a
decision, not another `if` statement in the engine.

---

## The contract in one paragraph

A chapter is one JSON object. `meta` describes the source and its
licence. `sections` holds the chapter text verbatim, plus the study aids
that sit beside it. `glossary` holds the curated vocabulary that gets a
rich popover. `conceptMap` holds the nodes and edges. `labs` holds the
simulations, each with a goal, three tasks, and a mandatory note that it
is not real model output. `figures` holds inline SVG with step
narrations and hotspots. `flashcards` and `quiz` hold the recall
material. `connections` links the chapter to earlier ones.

The engine reads this and nothing else. A new chapter is a new JSON
file.

---

## Run the gate

```powershell
cd projects/04-ai-engineering/study-studio
python scripts/validate_chapter.py schema/example-chapter.json
```

Output:

```
[PASS] schema/example-chapter.json: contract satisfied
```

Exit code 0 when every check passes, 1 when one fails, 2 when the file
cannot be read. The validator prints the location of every problem:

```
[FAIL] schema/chapter.json: 1 error(s), 0 warning(s)
  ERROR   SCHEMA_MISSING  quiz[6].answer: required key is missing
```

It checks structure (required keys, types, enums, id shapes), the
lab-simulation note, SVG safety, and referential integrity: every
`conceptId`, `labId`, `wordId`, `sectionId`, and SVG element id referenced
from anywhere must resolve to an object that exists. Standard library
only, so it runs anywhere Python does.

To see it fail on purpose, break something and re-run:

```powershell
python scripts/validate_chapter.py schema/example-chapter.json --quiet
```

---

## Add a chapter

1. Extract the chapter text to `chapter.json` following the shape in
   `schema/example-chapter.json`.
2. Fill `meta` with the real source. If the source is copyrighted, set
   `license` to `personal-study` and keep the file out of the repository.
3. Write the study aids. Everything you add gets the `AI` badge.
4. Run the validator until it exits 0.
5. Build the studio (Phase 1 command, not written yet).

The example chapter is synthetic: a short chapter on attention written
for this repo. It exists to exercise every branch of the contract, so
copy it as a shape, not as content.

---

## Boundaries

- **Chapter text is never reworded.** Study aids sit beside it.
- **Everything derived is badged.** The `AI` badge is a contract field,
  not a convention.
- **Every lab says it is a simulation.** The exact string
  `Illustrative simulation, not real model output.` is required by the
  schema and checked by the validator.
- **Book text stays out of the repository** unless the licence permits it.
  The study layer is always safe to commit.

---

## Reading order

`docs/STUDIO-SPEC.md` is the reference. Read sections 2 and 3 for the
architecture and the integrity rules, section 4 for the word engine
(the part most likely to be built wrong), and section 11 for how the
Definition of Done is measured rather than asserted.
