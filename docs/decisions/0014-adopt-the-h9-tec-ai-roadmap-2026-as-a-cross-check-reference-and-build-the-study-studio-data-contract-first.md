# ADR-0014: Adopt the h9-tec AI Roadmap 2026 as a cross-check reference and build the Study Studio data contract first

- **Status:** Proposed
- **Date:** 2026-10-22
- **Deciders:** repo owner
- **Tags:** architecture, tooling, learning, curriculum

## Context

Two separate things converged on 2026-10-22.

**First**, the h9-tec/ai-roadmap-2026 repository was read in full (five
layer READMEs, `00-start-here.md`, `resources.md`, `careers/README.md`,
`CONTRIBUTING.md`, `scripts/check-links.sh`, the file tree, and the SVG
asset conventions). It is a beginner-to-AI-engineer path in five layers
(Foundations, LLM Engineering, Agents, Evaluation, Production), one
mini-project per layer, each layer closing with an explicit "Done when"
checklist. It is published under CC BY 4.0.

The question worth asking of any external roadmap is not "does it cover
things I do not cover" but "what does it cover that I do not, measured".
Counting term occurrences across the 2,231 markdown files in this repo
gives a precise answer rather than an impression:

| Roadmap topic | Hits in this repo | Verdict |
|---|---|---|
| Sandbox execution (E2B, Modal) | 0 for E2B; 17 for "sandbox", all in quizzes and one glossary line | Gap |
| Browser agents (browser-use, Playwright MCP) | 0 | Gap |
| Voice agents (Whisper, realtime APIs) | 0 for "voice agent"; 1 incidental Whisper | Gap |
| GraphRAG | 2, both in a planning document | Gap |
| RFT / GRPO | 0 real hits (the 41 matches were `strftime`) | Gap |
| Pointwise judging | 1 against 83 pairwise | Gap |
| Cohen's kappa inside the judge topic | 0 (26 hits elsewhere) | Gap |
| Just-in-time retrieval | 0 | Gap |
| Microsoft Agent Framework | 0 | Correction needed |

The roadmap's own ordering was already independently adopted here: it
places Evaluation (layer 4) before Agents (layer 3) so every later project
ships with evals, and ADR-0004 moved the eval harness into weeks 2 to 3
for the same reason. The repos converge; there is no conflict to resolve
and no reordering to perform.

One roadmap claim is factually wrong in a way that matters here. It says
AutoGen has been archived. That is true as of the microsoft/autogen
README, which now carries an "archived and no longer maintained" notice
and points new users at Microsoft Agent Framework, with AG2 as the
community fork. This repo described AutoGen as a live option in
`projects/04-ai-engineering/agents/lectures/11-agent-loop-lecture.md`.

**Second**, a Study Studio was requested: an offline, single-file,
interactive reading environment for one chapter of a technical book, with
bilingual explanations, a word engine, interactive labs, active recall, and
concept mapping. The request arrived as a prompt that described the
wanted features but left the engineering unresolved, and it contained
several internal contradictions that would have produced a broken artifact
if followed literally (notably `display: inline-block` per word combined
with a promise of zero layout shift, and "fully offline" combined with
`SpeechRecognition`, which streams audio to a remote service).

The prompt also asked for the chapter text to be reproduced verbatim.
For a copyrighted book that cannot be committed to a public repository.

## Decision Drivers

- A studio that opens by double-clicking must not need a server. A
  `file://` page cannot `fetch()` a sibling JSON file, so data must be
  inlined at build time.
- The next chapter must cost one data file, not another engine rewrite.
- The Definition of Done must be measurable, not a list of intentions.
- Copyrighted book text must not enter a public repository.
- Book text, if it is extracted at all, must be provably unchanged.
- The roadmap's value is as a measuring instrument and a source of
  corrections, not as a curriculum to import wholesale.

## Options Considered

### Option A - Build the studio directly from the prompt
- Pros: Fastest to a first file.
- Cons: The prompt's word engine contradicts itself on layout shift, its
  nearest-word radius is geometrically wrong for multi-line text, its
  speech feature breaks the offline promise, and the data contract only
  emerges after the engine is written, which is the failure the contract
  exists to prevent.

### Option B - Write the data contract and validator first, then the engine
- Pros: The engine is written against a settled shape, so a second
  chapter is data only. Every contradiction in the request is resolved in
  writing before code depends on it. The validator becomes the gate that
  keeps later chapters honest.
- Cons: Nothing runnable exists at the end of this phase.

### Option C - Keep the repository as the curriculum source and drop the
studio
- Pros: The repo already covers the roadmap's spine and goes deeper, so
  the marginal value of another reading surface is low.
- Cons: Discards a genuine capability gap: the repo has no
  spaced-repetition or bilingual-reading layer, and it is the one place
  where the Arabic/English dual-language goal has no existing home.

## Decision

Adopt Option B, and treat the h9-tec roadmap as a cross-check instrument
rather than a curriculum to import.

Phase 0 writes the contract only:
`projects/04-ai-engineering/study-studio/schema/chapter.schema.json` (JSON
Schema 2020-12), a synthetic `schema/example-chapter.json` that exercises
every branch of it, `scripts/validate_chapter.py` (standard library only)
as the gate, `docs/STUDIO-SPEC.md` recording the settled decisions with
their reasons, and `README.md`. The engine is Phase 1.

The contract settles the contradictions rather than inheriting them.
Words are `display: inline`, not `inline-block`, so a hover transform
cannot move its neighbours; nearest-word detection weights vertical
distance three times horizontal and requires the same line band, because a
40 pixel circle at 16 pixel type reaches the lines above and below.
Popover data is curated to 150 to 250 entries per chapter instead of
every word, because a phonetic transcription is a lookup and a generated
one is a hallucination. `SpeechRecognition` is labelled as needing
network and is excluded from the offline definition of done. Chapter data
is inlined at build time because `file://` blocks the fetch. Text hashes
are compared against the source extraction at build time, because a studio
that quietly teaches something the book does not say is worse than no
studio. Every lab carries the exact string `Illustrative simulation, not
real model output.`, enforced by the validator.

Copyrighted book text stays on the learner's disk outside the repository.
What is committed is the study layer, the contract, the validator, and a
synthetic example.

From the roadmap, two things are taken now: the AutoGen archival
correction, and the measurement of nine gaps for later scheduling. The
external link checker it ships (`scripts/check-links.sh`, which detects
soft 404s where a page returns 200 but says "not found") is the most
valuable transferable artifact, because this repository holds 1,008
external links while CI verifies only relative links under `docs/`. That
becomes a separate proposal, not part of this ADR.

## Consequences

- Positive: the Studio engine will be written once against a settled
  contract, and a second chapter costs one JSON file.
- Positive: every requirement in the original request now has a written
  decision with a reason, so a future session does not re-litigate it.
- Positive: the validator is a real gate with a non-zero exit on broken
  references, proven by a deliberately broken copy that produced four
  located errors.
- Positive: nine curriculum gaps are now measured rather than guessed, so
  the next content decision rests on counts.
- Positive: the AutoGen correction removes stale advice from a lecture
  that had just been committed.
- Negative: Phase 0 delivers no runnable artifact. The value is entirely
  in the contract and the spec.
- Negative: the validator duplicates checks that JSON Schema already
  performs. It exists because referential integrity and the
  simulation-note rule are not expressible in plain JSON Schema, and
  because the gate must run with the standard library alone.
- Negative: a chapter file with a 9,000 word text and 250 glossary entries
  is roughly 300 KB of JSON, inlining to about 500 KB of HTML. Fine for a
  local file, wrong for a web page.
- Follow-ups / new ADR candidates:
  - An ADR for external link verification in CI, porting the soft 404
    detection from the roadmap's checker.
  - Scheduling decisions for the nine measured gaps, as separate content
    work rather than as new curriculum scope inside this window.
  - The Studio engine itself (Phase 1) and the build step with its hash
    comparison (Phase 1).
  - Microsoft Agent Framework as a registry node once a lecture teaches
    it.

## Links

- Related ADRs:
  - `0004-adopt-10-week-ai-engineer-track.md` - the eval-before-agents
    ordering that the roadmap independently confirms.
  - `0006-adopt-master-ai-engineering-curriculum.md` - the rule that
    curriculum content traces to a concept, which is why the roadmap is
    registered as a reference rather than adopted as content.
- Related artifacts (reviews, plans, eval reports):
  - `projects/04-ai-engineering/study-studio/` - the Phase 0 contract,
    validator, and specification.
  - `learning-sources/source-index.md#30` - the roadmap registered as a
    reference source, with the measurement that produced the gap table.
  - `projects/04-ai-engineering/agents/lectures/11-agent-loop-lecture.md`
    - the AutoGen archival correction.
