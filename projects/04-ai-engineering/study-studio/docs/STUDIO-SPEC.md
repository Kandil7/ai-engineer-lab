# Study Studio — Technical Specification

The contract for the offline Study Studio: one chapter of technical material,
one HTML file, bilingual reading with an interactive word layer.

This document records the decisions that are **settled**. Each one names the
problem it solves, because a spec that only states rules gets ignored the
first time it is inconvenient.

---

## 1. What this is

A single `.html` file that a learner opens by double-clicking, with no
network, no server, and no install. It holds:

- the chapter text, preserved verbatim from the source;
- a study layer: Arabic explanations, quizzes, flashcards, concept map,
  interactive labs;
- a word engine that gives meaning, pronunciation, and status for the
  vocabulary of the chapter.

The next chapter costs one data file. The engine does not change.

### Non-goals

- Not a textbook. The chapter is the textbook.
- Not an authoring tool. Chapters are JSON plus prose.
- Not multi-user, not synced, not collaborative. Progress is local.
- Not a live-model playground. Every lab is a simulation and says so.

---

## 2. Architecture

```
CHAPTER_DATA  (one JSON object, inlined at build time)
     |
     v
ENGINE        (one JS module, inlined at build time)
     |
     v
studio.html   (one file, opens from disk, no network)
```

`CHAPTER_DATA` is the only thing that changes between chapters. The engine
reads it and knows nothing about the chapter subject.

### Why the data is inlined, not fetched

A `file://` page cannot `fetch()` a sibling JSON file: the browser treats
each local file as an opaque origin and blocks the request. A studio that
loads `chapter.json` over `fetch` works on a web server and fails on
double-click, which is the whole use case.

Therefore the build step **inlines** the data into a `<script>` block:

```html
<script id="chapter-data" type="application/json">
{ ...CHAPTER_DATA... }
</script>
```

The engine reads it with `JSON.parse(document.getElementById('chapter-data').textContent)`.
No `fetch`, no CORS, no server. One file travels, and that file is the
studio.

### Why the data contract is written down first

The failure mode of "build a studio, then reuse it for chapter two" is that
chapter two reveals a field nobody thought of, and the engine grows a
special case. The schema and the validator exist to make that impossible:
a new chapter that cannot be expressed in `CHAPTER_DATA` is not a new
chapter, it is a new kind of chapter, and it needs a decision, not an
`if` statement.

---

## 3. Content integrity rules

1. **Chapter text is preserved.** Never reworded, never summarised in
   place, never omitted. Study aids sit beside the text, never inside it.
2. **Everything derived is labelled.** Arabic explanations, definitions,
   analogies, quizzes, labs, and summaries carry a small `AI` badge.
3. **Labs are labelled as simulations.** Every lab object carries
   `simulationNote` with the exact string
   `Illustrative simulation, not real model output.` The validator rejects
   a lab without it. A simulation must never look like a measurement.
4. **Book text stays out of the repository.** For a copyrighted source
   (`license: personal-study`), the extracted text lives on the learner's
   disk outside the repo, and only the study layer is committed. For a
   permissively licensed source (`CC-BY-4.0`, `public-domain`, `MIT`), the
   text can be committed with the attribution line carried in `meta`.

---

## 4. The word engine

This is the part most likely to be built wrong, so the reasoning is
recorded here.

### 4.1 Words are inline, not inline-block

The original prompt asked for `display: inline-block` on every word span
and promised zero layout shift. Those two requirements contradict each
other:

- `inline-block` gives each word its own block-level box. Text can no
  longer break naturally inside a word, justification stops working, and
  the line box grows to the tallest span on the line.
- The studio adds a glow and a scale on hover. With `inline-block`, that
  transform on a single word changes the line box height, so the words
  below it shift. That is layout shift, by construction.

**Decision:** each word is a `<span>` with `display: inline`. The hover
effect uses `transform: scale()` and `box-shadow`, both of which are
painted outside the layout and do not move siblings. The visual result is
the same and the reflow is zero.

The engine proves it rather than asserting it: the self-test measures the
container's `getBoundingClientRect()` before and after a hover and fails
if the height changed by more than one pixel.

### 4.2 The nearest word is found anisotropically

The original prompt asked for "the single nearest word within about 40
pixels". A circular radius is the wrong shape for text.

At 16px font and 1.6 line-height, the vertical gap between baselines is
about 26px, and the vertical gap between the bottom of one line box and
the top of the next is about 10px. A 40px circle centred on a word in the
middle of a line therefore reaches the words in the line above and the
line below. The highlight flickers between lines as the pointer moves,
which reads as broken.

**Decision:** the distance metric is anisotropic. Vertical distance is
weighted by 3x before comparison, and the candidate must be in the same
line band as the pointer. The effective search box is then wide
horizontally (about 40px) and narrow vertically (about 13px), which is
the shape a word actually occupies.

### 4.3 The hit-test cache is invalidated, not rebuilt, per event

`pointermove` fires far more often than the display refreshes. Two rules:

- The handler does no layout reads. It stores the pointer position and
  schedules one `requestAnimationFrame` callback.
- The callback does exactly one layout read (the cached rect list) and
  then paints. Painting happens on `transform` and `opacity` only.

The rect cache is rebuilt on `resize`, `scroll` (only when the scroll
changes layout, not on every scroll tick), `document.fonts.ready`, and a
reading-mode change. A `ResizeObserver` on the article element covers
content reflow.

### 4.4 Popover data is curated, not generated per word

The original prompt asked for pre-generated popover data for every word:
IPA, English meaning, Arabic meaning, part of speech, and an example
sentence. For a 30-page chapter that is roughly 9,000 words, so about
45,000 fields, and a phonetic transcription for every one of them.

Two problems:

- **Accuracy.** A phonetic transcription is a lookup, not a derivation. A
  model that invents them produces plausible-looking nonsense, and a
  learner who trusts a wrong IPA learns the word wrong.
- **Value.** A popover for every word is noise. The words that block
  understanding are the technical terms and the academic vocabulary, and
  there are 150 to 250 of those in a chapter.

**Decision:** rich popovers (IPA, meanings, type, example) exist for the
curated `glossary` entries. Every other word still gets a click target
that shows the paragraph's Arabic explanation. The `glossary` array is the
curated set; the engine marks those words in the running text.

IPA is optional per entry (`ipa` may be absent) precisely so that a
missing lookup is a missing field rather than an invented one.

### 4.5 Word status is a learner state, not chapter content

`new`, `learning`, `known` live in `localStorage`, keyed by chapter id,
and are never written into the chapter file. The "show only words I do not
know" toggle fades known words. If the storage is unavailable (private
mode, `file://` restrictions in some browsers), the engine falls back to an
in-memory map for the session and says so in the dashboard.

---

## 5. Bilingual layer

Four language modes: English only, English with Arabic hints, Arabic
explanations, and Test myself (Arabic hidden, used for recall).

Arabic text carries `lang="ar"` and `dir="rtl"`. English and code stay
`dir="ltr"`. A line that mixes both wraps the Arabic fragment in `<bdi>`
so the bidi algorithm does not reorder the English around it.

Arabic is a **meaning-based** explanation, not a word-for-word translation.
A literal translation of a technical paragraph produces an unreadable
sentence that looks precise and is not. The Arabic explains the same idea
in Arabic, and says less when the English is saying a lot.

The English Gym panel lists the chapter's top technical and academic
vocabulary, with fill-in-the-blank drills built from the chapter's own
sentences.

### Speech

The Web Speech API is used for pronunciation, with these rules:

- `speechSynthesis.getVoices()` is populated asynchronously. The engine
  listens for `voiceschanged` and builds the voice list when it fires,
  not on first call. A missing voice list hides the US/UK selector and
  keeps a single default voice.
- `SpeechRecognition` is a **separate, optional** feature. It is offered
  only when the browser exposes it, and it is hidden rather than
  disabled when it does not, because a visible dead button teaches the
  wrong thing.
- `SpeechRecognition` in Chrome sends audio to a remote service. The
  English Gym's "say it" drill is therefore labelled as needing network,
  and it is not part of the offline definition of done.

---

## 6. Figures

Figures are inline SVG, written by hand for the chapter. The engine adds:

- **Play / Pause / Step / Reset** over a step list, each step carrying an
  English and an Arabic narration.
- **Animated packets** flowing along edges: a `<circle>` animated with
  `offset-path` or a `stroke-dashoffset` transform, so the motion is
  transform-only and costs no layout.
- **Hotspots** on components: hover or tap shows what the part does, its
  inputs and outputs, and the common mistakes.
- **Build it yourself**: drag (or keyboard-select) components into the
  right order. The keyboard path is not a fallback bolted on, it is the
  same state machine with a different event source.

SVG ids are the join key between the figure data and the engine. The
validator checks that every `steps[].highlight` entry and every
`hotspots[].target` names an element id that exists in that figure's SVG.
A figure whose narration lights up a component that is not in the picture
is a defect, and this check makes it a build failure rather than a bug
report.

---

## 7. Labs

A lab is a small simulation with controls, three guided tasks, and a
one-line takeaway in both languages.

Controls are declared as data: `slider`, `toggle`, `select`, `text`,
with min, max, step, options, and a default. The engine builds the
widget and the update function from the declaration, so a new lab adds a
data entry, not a new form.

Every lab:

- carries `simulationNote` with the exact required string;
- has exactly three tasks, each with a prompt and a check;
- ends with `takeawayEn` and `takeawayAr`.

**Lab kinds** are a closed set in the schema: `tokenizer`, `embedding`,
`attention`, `sampling`, `rag-pipeline`, `training`, `quantization`,
`metrics`, `cost-latency`, `generic`. A new kind is a schema change and a
decision, not a silent extension.

---

## 8. Active recall

**Flashcards** use Leitner boxes in `localStorage`: box 1 to 5, intervals
1, 3, 7, 16, 35 days. A card answered correctly moves up a box, a wrong
answer moves it back to box 1 and resets its interval. "Due today" counts
cards whose next-due date has passed. Export to CSV for Anki is a plain
text join, no library.

**Quiz** items cover seven types: `mcq`, `true-false`, `order`, `match`,
`fill-code`, `spot-mistake`, `explain`. Every item has an English and an
Arabic explanation. Items marked `needsConfidence` ask for a sure/unsure
rating, and an item answered *sure* but wrong is flagged harder than one
answered unsure, because overconfidence costs more than ignorance.

**Feynman mode**: the learner writes an explanation in a text box, then
sees a checklist of key points and self-assesses. No API, no scoring
model. The checklist is data (`quiz[].answer` on an `explain` item).

**Exam sprint**: a timed mixed quiz with a per-concept report at the end.

**Export**: flashcards as CSV, notes as Markdown, one printable cheat
sheet via a print stylesheet.

---

## 9. Progress and motivation

XP, levels, daily streak, and badges are secondary. They must never block
content: a learner whose streak broke on a Tuesday still gets the full
chapter on Wednesday.

The dashboard shows sections marked understood, words learned, flashcards
due, quiz accuracy per concept, time studied, and a weekly mastery radar.
"Next best action" picks the weakest concept that has a flashcard due,
otherwise the next unread section.

---

## 10. Accessibility and performance

- Full keyboard navigation. A focused paragraph uses arrow keys to move
  between words. `Esc` closes every overlay. Focus is visible.
- Paragraphs carry the full text in `aria-label`; the per-word spans are
  `aria-hidden`, so a screen reader reads prose rather than nine thousand
  fragments.
- Touch targets are at least 44px.
- `prefers-reduced-motion` disables the glow, the scale, the packet flow,
  and the confetti, and keeps static equivalents: the highlighted word
  gets a colour change instead of a scale, the diagram steps advance
  without animation.
- `localStorage` is wrapped in try/catch everywhere, with an in-memory
  fallback.
- Only `transform` and `opacity` are animated. Nothing that triggers
  layout.
- Labs initialise lazily when scrolled into view.
- Sound is off until the first user interaction, and the mute toggle
  persists.

---

## 11. Verification

The Definition of Done must be **measurable**. The original prompt's
checklist was a list of intentions. These are the checks, and each one has
a command or a measurement behind it:

| # | Check | How it is measured |
|---|-------|--------------------|
| 1 | Chapter text present and unchanged | Hash of each paragraph against the source extraction; `scripts/extract_chapter.py` writes the hashes |
| 2 | Word highlight causes no layout shift | `getBoundingClientRect()` of the container compared before and after hover, in the in-page self-test |
| 3 | Nearest word is the one under the pointer | Self-test asserts the highlighted word's rect contains the pointer |
| 4 | Popover opens and speaks | Self-test opens a popover and asserts the element exists and the button is wired |
| 5 | Arabic modes switch | Self-test switches all four modes and asserts the Arabic content is present or absent as required |
| 6 | Figures step through | Self-test advances every figure to its last step and asserts the narration changes |
| 7 | Build-it-yourself accepts the right order | Self-test submits the correct order and asserts the success state |
| 8 | Every lab runs with no console error | Self-test initialises every lab and asserts its controls exist |
| 9 | Concept map renders and nodes resolve | Validator resolves every edge; self-test asserts the node count matches `meta.conceptCount` |
| 10 | Flashcards, quiz, Feynman work | Self-test schedules a card, answers a quiz item, and compares a Feynman answer against its checklist |
| 11 | Dashboard and exports produce files | Self-test triggers both exports and asserts the produced blob is non-empty |
| 12 | Keyboard, reduced motion, mobile | Manual pass plus the self-test's tab-order count |
| 13 | Works offline | Open with the network disconnected. Assert zero external references in the file |
| 14 | Data contract holds | `python scripts/validate_chapter.py <chapter.json>` exits 0 |

Checks 2 to 12 are implemented as an in-page self-test mode
(`studio.html?selftest=1`) that prints a pass/fail line per check. The
build refuses to publish a studio whose self-test fails.

### External reference check

A studio that opens with the network disconnected must contain **zero**
external references. The build scans the output for `http://`, `https://`,
`//cdn`, `src="//`, `@import`, and `url(http` and fails on any hit. A
chapter may cite a URL as *text*; it may not *load* one.

---

## 12. Build steps

The build is a script that takes a chapter JSON and an engine and writes
one HTML file. The order matters:

1. Load and validate the chapter (`validate_chapter.py`).
2. Extract the chapter text from the source and compare it against the
   text in the JSON, paragraph by paragraph, by hash.
3. Inline the JSON into the template.
4. Inline the CSS and the JS.
5. Run the external-reference scan.
6. Write the HTML file.
7. Optionally, run the in-page self-test in a headless browser.

Step 2 is the one that is easy to skip and expensive to skip. If the
chapter text and the extraction drift, the studio is quietly teaching
something the book does not say.

---

## 13. Repo layout

```
projects/04-ai-engineering/study-studio/
  README.md                    what this is and how to run it
  schema/
    chapter.schema.json        the data contract, JSON Schema 2020-12
    example-chapter.json       a synthetic chapter that satisfies it
  scripts/
    validate_chapter.py        contract gate, standard library only
    build_studio.py            inline + scan + emit one HTML file
  docs/
    STUDIO-SPEC.md             this document
```

Engine source (`engine/studio.js`, `engine/studio.css`) arrives with
Phase 1. Until then the contract is testable on its own, which is the
point of writing it first.

---

## 14. Known limitations of this design

- **The data file is large.** A chapter with 9,000 words of text and 250
  glossary entries is roughly 300 KB of JSON. Inlined, the HTML lands
  around 500 KB. That is fine for a local file and wrong for a web page.
- **No cross-chapter state.** Each studio is self-contained. Progress
  across chapters is tracked by the chapter id in `localStorage`, but
  there is no shared dashboard.
- **Extraction is manual per source.** A PDF chapter needs a per-source
  extraction step. The hash comparison catches drift but does not prevent
  it.
- **The word engine needs a DOM pass per section.** The engine only
  initialises the section being read, so a long chapter stays responsive,
  but the first open of a section has a visible cost.
