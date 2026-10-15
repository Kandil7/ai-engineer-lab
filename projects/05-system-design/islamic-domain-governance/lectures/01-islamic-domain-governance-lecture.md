# Lecture 01: Islamic-Domain Literacy and Corpus Governance

## Topic Overview

A retrieval system over Islamic texts fails in two ways that ordinary RAG systems never face, and in this domain the two failures are one discipline. The first is categorical: the same retrieval pool serves revelation, prophetic reports, companion reports, exegesis, jurisprudence, and a scholar's context-bound answer, and a system that answers from one category while citing another commits a category error with religious consequence, not a stylistic slip. The second is legal and archival: the texts are ancient, but the copies you hold are modern artifacts with licences, terms of use, checksums, and living people inside them, and a RAG system that returns verbatim passages is publishing them. This lecture teaches both halves as a single governance contract: every passage carries a category ledger (what the text is, with inherited grades and citation coordinates) and a provenance ledger (where the artifact came from, under what licence, pinned by checksum, served under what delivery policy). The lecture is for system builders: it teaches recognition, extraction, comparison, and refusal — never jurisprudence. Grades quoted here are inherited metadata attributed to named graders; positions of the schools are presented as disagreement, because that is what they are. The companion exercise audits a corpus manifest against ten executable rules (GOV001-GOV010) whose BAD pack trips every rule and whose GOOD pack must raise zero.

**Duration:** 4-5 hours
**Difficulty:** Advanced
**Prerequisites:** Arabic NLP 01 (text fundamentals), Arabic NLP 02 (normalization and the two-text discipline), basic RAG concepts; the Arabic NLP 08 entity-resolution lecture helps but is not required

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Distinguish** the nine textual categories (quran, hadith, athar, tafsir, fiqh, qawa'id, usul, fatwa, shawahid, taqrid) and say what breaks when two of them collapse into one pool
2. **Explain** the isnad/matn structure of a report and design chunking that never orphans a matn from its chain without leaving a linkage
3. **Carry** hadith grades as inherited metadata with grader attribution, and never emit a grade as the system's own verdict
4. **Recognize** the transmission vocabulary (mutawatir, ahad, mursal, mu'allaq, qira'a, riwaya, ikhtilaf, ijtihad, taqlid) on sight, so a misreading pipeline can be caught before it ships
5. **Present** two schools' positions side by side with attribution, without adjudicating, and without ever framing one as "the ruling"
6. **Refuse** well: detect fatwa-substance questions, state the boundary, cite what the corpus can support, and hand off to a named trustworthy source or scholar — as a designed, tested response, not an error
7. **Record** per-source provenance: origin, licence decision, terms of use as they actually read, retrieval date, checksum, transformations, and a licence-compatible use policy
8. **Apply** the licence families: public-domain classical text, modern critical edition, open corpus, redistribution-forbidden site, restricted API — and enforce that holding a text is not the right to republish it
9. **Judge** chunking, embedding, and indexing as potential derivative works, recording the decision per source rather than per project
10. **Operate** the governance release checklist: licences and checksums decided, passages traced, grades inherited, categories checked, refusal tested, audit log retained under a stated limit

---

## Key Concepts

### 1. The Governance Contract: Two Ledgers, One Discipline

Every passage in a governed Islamic corpus carries two ledgers, and a release is defensible only when both are complete:

```text
                        ┌──────────────────────────────────────┐
                        │            passage record            │
                        └───────────────┬──────────────────────┘
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
   ┌─────────────────────────────┐             ┌─────────────────────────────┐
   │  CATEGORY LEDGER            │             │  PROVENANCE LEDGER          │
   │  what the text IS           │             │  where the artifact CAME    │
   │  • category tag             │             │  FROM and under what terms  │
   │  • inherited grade (+grader)│             │  • source record (GOV001/2) │
   │  • isnad/matn linkage       │             │  • licence decision         │
   │  • citation coordinates     │             │  • checksum, retrieval date │
   └─────────────────────────────┘             │  • use policy (GOV003)      │
   blocks: category errors, silent            └─────────────────────────────┘
   grade flattening, uncheckable cites        blocks: silent republication,
                                              irreproducible claims
```

The ledgers are one discipline because the same act — careless ingestion — breaks both: a fixed-size chunker that splits an isnad from its matn (category ledger) is usually the same chunker that dropped the source's terms-of-use page (provenance ledger). The lecture teaches them together, and the exercise audits them together.

**FACT in this repository.** Athar's learning copy already enforces the *location* half of provenance from day one: `SourceLocation` is a frozen dataclass whose `__post_init__` rejects an empty `book_id` and any `page < 1` (`projects/04-ai-engineering/athar-lab/contracts.py:33-46`), and `Passage` enforces the two-text discipline — verbatim `original` for display and citation, normalized `searchable` for matching — at `contracts.py:59-75`. What Athar's stage-1 contracts do not yet carry is the category ledger (category tags, inherited grades, isnad linkage) and the licence half of the provenance ledger. This lecture specifies both; the exercise's GOOD manifest is shaped like the records Athar would grow into.

### 2. The Textual Categories: A Taxonomy That Must Not Collapse

The corpus holds texts of nine kinds. They differ in *who speaks*, *in what capacity*, and *with what authority shape* — and those differences are exactly what a retrieval system flattens when it treats every Arabic passage as "a chunk."

| Category | What it is | Who speaks | Citation coordinates | Serving consequence |
|---|---|---|---|---|
| **quran** | Divine revelation, the primary text | Allah, via the Prophet's recitation | surah:ayah (validated, GOV010) | Never paraphrased as "the quran says (paraphrase)"; verbatim serving is the norm |
| **hadith** | Prophetic report: what the Prophet said/did/approved | The Prophet, through narrators | book + hadith number (or edition locator) | Must carry its inherited grade; never served unattributed |
| **athar** | Companion or successor report | A companion/successor, through narrators | book + entry locator | Same chain discipline as hadith; do not upgrade a companion's word to a prophecy |
| **tafsir** | Exegesis: a scholar's reading of an ayah or passage | A named exegete | work + volume/page, plus the ayah discussed | The commentator's paraphrase is never served as the quranic text |
| **fiqh** | Jurisprudence: a school's or scholar's derived rulings | A school or its authors | work + volume/page | A school's ruling is that school's, not "the ruling" |
| **qawa'id / usul** | Legal theory and maxim scholarship | Theorists | work + volume/page | Theory is not fatwa; a maxim is not a verdict on your case |
| **fatwa** | A scholar's answer to a specific question, in a context | A named mufti, at a time and place | work + volume/page + question identity | Context-bound by construction; reference-only delivery by default |
| **shawahid** | Supporting evidence cited *inside* another work | Whichever source the citing author quoted | the citing work's coordinates | Do not detach a shahid from the argument it supports and re-serve it as a freestanding proof |
| **taqrid** | A scholar's endorsement of a position (e.g., a hadith's grading or a book's approval) | The endorser | endorser + work + page | An endorsement travels as attributed metadata, never as anonymous consensus |

**Why conflation is the failure that matters.** Answer a question about an ayah by serving a tafsir passage while the citation line reads "Quran 2:255" and you have attributed a commentator's words to revelation. Serve a fiqh passage from one school under the prompt "What is the ruling?" and you have erased the disagreement the tradition itself records. These are not "slightly wrong" answers; they are category errors with religious consequence, and the users who cannot audit them are precisely the ones least equipped to catch them. The pipeline rule is mechanical: **category tags are set at ingestion, checked at retrieval, and displayed at answer time** — a passage without a tag never enters the pool (GOV004).

### 3. Isnad and Matn: The Anatomy of a Report

A hadith or athar report has two physically separable parts, and the corpus must keep them connected even when chunking separates them:

```text
  ISNAD (سند)                                MATN (متن)
  the chain of narration                     the report text itself
  ┌────────────────────────────────┐         ┌────────────────────────────┐
  │  A  ←  B  ←  C  ←  companion   │ ──────► │  what was reported:        │
  │  (each link: named narrator,   │  feeds  │  saying / action / approval│
  │   with rijal metadata)         │         │  of the Prophet            │
  └────────────────────────────────┘         └────────────────────────────┘
         │                                            │
         └──────────── grading applies to BOTH ───────┘
                     (the report, not the sentence)
```

Real-shaped example from the exercise's fixtures (the chain is the well-known Companion-level hearing; grades shown are *inherited* from the edition, not this system's judgment):

```text
isnad:  عَنْ عُمَرَ بْنِ الْخَطَّابِ رضي الله عنه، قَالَ: سَمِعْتُ رَسُولَ
        اللَّهِ صلى الله عليه وسلم يَقُولُ:
matn:   «إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى...»
```

The engineering consequences:

- **The isnad is data, not preamble.** It answers *who narrated this from whom* — the same question a provenance record answers for the digital artifact. A pipeline that strips it as "boilerplate before the real text" deletes the report's chain of custody.
- **Chunking may split them; linkage must survive.** A fixed-size chunker that lands the isnad in chunk 7 and the matn in chunk 8 must leave an `isnad_link` on the matn chunk pointing at the chunk that holds the chain. An orphaned matn is GOV006 — a report whose narrators the system can no longer name.
- **Grading attaches to the report, not the fragment.** The grade, when present, belongs to the (isnad + matn) pair as evaluated by a grader. Carrying it on one chunk of a split report and not the other — or dropping it because "this chunk is only the chain" — is the defect GOV005 exists to catch.

### 4. Grading as Inherited Metadata

Grading (taʿyīn) is the tradition's own quality apparatus: named scholars evaluated reports over centuries and left their verdicts in the editions. A corpus *inherits* that apparatus; it does not reinvent it.

| Grade (common labels) | What the label asserts in the tradition | Serving rule |
|---|---|---|
| **sahih** (sound) | The report meets the classical conditions of acceptance | Served with grade and grader visible |
| **hasan** (good) | Slightly weaker chain or a defect tolerated for virtue of the report | Served with grade and grader visible |
| **daʿif** (weak) | A chain defect or shortcoming; not used as proof by the tradition's own standards | Never served adjacent to a sahih report without the distinction visible |
| **mawduʿ** (fabricated) | Attributed to the Prophet falsely, per the grader's judgment | Flagged and fenced; a retrieval system has no business surfacing it as a live proof |

Two facts a builder must internalize:

1. **Graders disagree.** The same report can carry different grades in different schools' apparatus and different modern collections. Disagreement about a grade is itself part of the inherited record. A system that "picks a grade" has adjudicated; a system that *stores every grade it inherited, each with its grader* has recorded.
2. **The grade is data attached to the passage, never the system's verdict.** The model does not grade, does not upgrade, and does not launder a weak report's serving with confident prose. The grade travels as a field, displayed when relevant:

```json
{
  "grade": {
    "value": "sahih",
    "grader": "the source edition's own grading apparatus",
    "note": "inherited metadata; the system does not re-grade"
  }
}
```

That JSON shape is what the exercise's GOOD pack carries and what GOV005 demands of every passage tagged `hadith`. The `grader` field is mandatory: a grade without an attributed grader is an anonymous verdict, and anonymous verdicts are exactly what this tradition's own methodology refuses to accept from humans — a system has no exemption.

### 5. Transmission Vocabulary the Builder Must Recognize

You will never *issue* rulings with this vocabulary. You need it to notice when the pipeline is misreading a passage — because the vocabulary marks the passage's own self-description, and a pipeline that ignores it will serve a mursal report with the confidence of a mutawatir one.

| Term | Recognition cue | What a naive pipeline does wrong |
|---|---|---|
| **mutawatir** | Mass-transmitted; many narrators at every link | Serves it identically to an ahad report; loses the strength signal |
| **ahad** | Single-chain report at some link | Serves it as if its standing were unqualified |
| **mursal** | Chain missing a Companion link ("so-and-so said") | Renders as a complete chain by silently closing the gap |
| **muʿallaq** | Chain suspended at its head (book cites without "heard from") | Renders as fully connected |
| **maqtuʿ** | Chain deliberately ended at a companion/successor | Upgrades a companion's report to prophetic voice |
| **qiraʾa / riwaya** | A reading or transmission variant of a text | Picks one variant silently and displays it as *the* text |
| **ikhtilaf** | Recorded scholarly disagreement | Collapses to one position "for simplicity" |
| **ijtihad** | Independent legal reasoning by a qualified scholar | Presents a derived ruling as a transmitted one |
| **taqlid** | Following a school's settled position | Presents one school's settled position as the universal norm |
| **usul al-fiqh** | The theory: sources, methods, objectives | Treats a theory chapter as case law |
| **hadith qudsi** | Prophetic report whose content is from Allah, words are the Prophet's | Merges into quran citations or into ordinary hadith without distinction |
| **sunnah** | The Prophet's established path (sayings, actions, approvals) | Used as a vague synonym for "islamically good" |

The rule of use: **extract and preserve, never adjudicate.** When a source's own apparatus labels a report mursal, the passage record keeps that label; the answer layer never "completes" the chain to make it look stronger.

### 6. Madhhab and Ikhtilaf: Presenting Disagreement Without Adjudicating

The four Sunni schools — Hanafi, Maliki, Shafi'i, Hanbali — are living legal traditions with continuous scholarship, and their recorded disagreements (ikhtilaf) are a legitimate, documented feature of the discipline, not a bug to be resolved by a language model. Where the schools agree, the tradition itself records ijmaʿ (consensus); where they differ, each position comes with its derivation, its evidence, and its school.

**The system's job is three things, and only three:**

```text
  EXPLAIN      what position P of school S says, in its own terms
  EXTRACT      the passage(s) the corpus holds that support P, attributed
  COMPARE      show P and Q side by side, each with its attribution

  never:  ADJUDICATE — "the ruling is P", "the correct view is Q",
          "scholars agree" (when the corpus shows they do not),
          or a synthesized fatwa wearing a citation mask
```

**Any question that is a fatwa in substance must be refused or routed.** Fatwa-substance means: personal, context-bound, actionable — "Is X permissible for me, in my situation, now?" A corpus question ("What does school S say about X?" / "What are the positions on X in these books?") is extractable. The difference is not stylistic; it is the difference between the corpus's contents and a ruling for a case the system cannot see (and is not authorized to issue). This is a **hard system requirement**: the refusal path of section 7 is configured (GOV008), tested before release, and its refusals are logged (section 14). A system that "helpfully" answers fatwa-substance questions is not being useful; it is issuing fatwas with a retrieval citation for decoration.

**The design rule in one sentence:** present two positions without adjudicating by giving each position its own attributed block — school, scholar, source coordinates — and letting the user see the disagreement the tradition itself records.

### 7. The Refusal Path as a Designed Response

Refusal is not an error page. It is a designed response with three parts, and the exercise's GOOD pack ships the template:

1. **Boundary statement** — what this system does and does not do (it displays texts with their chains and attributions; it does not issue fatwas).
2. **Cite what the corpus can** — point at the extractable material: the relevant passages with coordinates, the positions as recorded.
3. **Handoff** — name where the question belongs: a named trustworthy reference collection, a school's official fatwa board, a qualified scholar. The handoff target is configuration, not improvisation (GOV008).

```text
  user question
       │
       ▼
  fatwa-substance detector ──── no ───► normal retrieval + governed answer
       │ yes
       ▼
  refusal template
  ├── boundary: "this system does not issue fatwas"
  ├── citations: what the corpus *can* support, with coordinates
  └── handoff: configured trustworthy target
       │
       ▼
  audit log: refusal flag = true (section 14)
```

A worked rendering, straight from the exercise demo (`exercises/01-islamic-domain-governance.py`, `_demo_refusal`): the template opens by stating the boundary in Arabic — the system displays texts with their chains and attributions and does not fatwa — names the question as personal fatwa-substance, points at the reference material the corpus holds, and hands off to the deployment's configured scholar or fatwa board. Three test cases ship with any release: a clearly extractable question (must answer), a clearly fatwa-substance question (must refuse), and a boundary case (must refuse; when unsure, refuse and explain why).

**The never-list, restated as product requirements.** These are not tone guidelines; each is a line the release gate holds:

1. **Never issue a fatwa** — not softened, not hedged with "scholars generally say," not dressed in citations. Fatwa-substance questions meet the refusal path, full stop.
2. **Never adjudicate between schools** — no "the correct view is," no synthesized position, no silent majority-vote across the four schools' manuals.
3. **Never re-grade a report** — the grade field carries the source apparatus's judgment with its grader; the system does not upgrade, downgrade, or average.
4. **Never complete a chain** — a mursal report stays mursal; a muʿallaq chain stays suspended; the labels are data.
5. **Never blend categories in one citation line** — quran quoted verbatim with surah:ayah; tafsir introduced as tafsir with its own coordinates; fiqh named with its school.
6. **Never serve no-redistribution text verbatim** — reference-only is the compliant mode, recorded, not improvised.
7. **Never present one school as the default** — "the ruling" without a school or scholar attached is not a phrase this system produces.
8. **Never answer a modern-personal question from a fatwa archive's text** — the private case stays private; the handoff carries the user's need, not the archive's contents.

A refusal that observes all eight is not a failure of the product; it is the product.

### 8. Category Discipline in the Pipeline: Five Failure Modes

These five failures are the ones this domain actually ships. Each is caught by a rule in the exercise.

**Failure 1 — the chunk boundary splits a matn from its isnad, silently.** The user asks about a report; the system serves the matn with no chain and no link; the user cannot see who narrated it. *Catch:* GOV006 — every hadith/athar passage either carries its isnad or links to the chunk that does.

**Failure 2 — the citation names a book but not the coordinates a scholar would check.** "It is in Sunan al-X" is not a citation; "Sunan al-X, book of Y, hadith number Z, edition W" is. Without volume/page or an equivalent locator, no one — scholar or skeptic — can verify the passage, and the citation is decoration. *Catch:* GOV007.

**Failure 3 — a weak report is served next to a sound one with no distinction.** The generator sees two Arabic passages of similar length and writes "scholars mention that..." — flattening the inherited grade distinction into a single confident sentence. *Catch:* GOV005 (the grade field must exist) plus the presentation rule (grades are displayed, not smoothed).

**Failure 4 — an ayah is blended with a commentator's paraphrase.** The retrieval pulls quran + tafsir chunks; the model's answer merges them: "Allah says, the Living, the Self-Subsisting, who does not need anything..." — half revelation, half exegesis, attributed wholly to the quran. *Catch:* GOV004 (categories exist and are checked) plus generation-side discipline: quranic text is quoted verbatim with its coordinate; commentary is introduced as commentary, with its own coordinates. Athar's two-text discipline (`contracts.py:65-66`: verbatim `original` for display, normalized `searchable` for matching) is the display half of this rule.

**Failure 5 — one school's ruling is presented as "the ruling."** The prompt says "What is the ruling on X?", the retrieval is dominated by one school's fiqh manual (because that is what was digitized), and the answer says "The ruling is..." *Catch:* the refusal path for fatwa-substance (section 6-7), and for extractable comparison questions, attributed side-by-side presentation — never the definite article without a school name attached.

### 9. The Provenance Record

One record per source, every passage tracing back to it. The exercise's `SourceRecord` is the schema:

| Field | What it holds | Why it exists |
|---|---|---|
| `source_id` | Stable identifier for this source in this corpus | The join key every passage cites |
| `origin` | Site, collection, edition, mirror — where the artifact came from | "The internet" is not an origin |
| `licence_decision` | How the licence and terms *actually read*, decided by a human | GOV001; absence blocks release |
| `terms_of_use` | The terms as they actually read, quoted or summarized faithfully | The licence decision must be checkable against them |
| `retrieved_at` | Date the artifact was retrieved | Changelog anchor |
| `checksum` | sha256 of the retrieved artifact | GOV002; the reproducibility pin (section 10) |
| `use_policy` | What *this corpus* decided it may do: `redistribution-ok`, `no-redistribution`, ... | GOV003's input; a per-source decision, not a project-wide assumption |

The exercise implements the record as a frozen dataclass, so the schema you audit against is the schema the detector checks — not a slide:

```python
@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    origin: str
    licence_decision: str | None  # None trips GOV001 (critical)
    terms_of_use: str
    retrieved_at: str  # ISO date; changelog anchor
    checksum: str | None  # None trips GOV002 (warning)
    use_policy: str  # "redistribution-ok" | "no-redistribution" | ...


@dataclass(frozen=True)
class Passage:
    chunk_id: str
    source_id: str
    category: str  # closed set; "missing" trips GOV004 (critical)
    original: str  # verbatim — display and citation come from here
    searchable: str  # normalized — matching only (two-text discipline)
    grade: dict | None  # {"value", "grader", "note"}; hadith without it trips GOV005
    isnad_present: bool
    isnad_link: str | None  # matn with neither chain nor link trips GOV006
    citation: "Citation"
    served_verbatim: bool
```

A filled GOOD record, the shape your review should expect from any importer:

```json
{
  "source_id": "src-open-quran",
  "origin": "open quran corpus, edition W, mirror M, retrieved via HTTPS export",
  "licence_decision": "CC0 1.0 universal; verified 2026-09-12 against the mirror's LICENSE file",
  "terms_of_use": "CC0 1.0: no conditions; attribution appreciated, not required",
  "retrieved_at": "2026-09-12",
  "checksum": "sha256:7e94ec9dd9e975ce...",
  "use_policy": "redistribution-ok"
}
```

Note what the licence decision is *not*: it is not "public domain because old" and not "open because it was free to download." It is a named human's recorded reading of how *these terms actually read for this artifact*, dated, checkable against the `terms_of_use` field beside it.

```text
  passage ──► source_id ──► SourceRecord ──► licence_decision + checksum
      │                            │
      │                            └──► use_policy ──► delivery mode
      │                                 (verbatim | summary | reference-only)
      └──► category ledger (section 2-4)
```

**FACT in this repository.** Pipeline-level provenance — versioning and lineage for data pipelines generally — is taught at `projects/00-core-foundations/data-engineering/06-provenance-versioning/`; Athar's `SourceLocation` (with its `path` field reserved "for provenance", `contracts.py:40`) is the corpus-side seed. This lecture's contribution is the *licence-and-category* half those two do not cover: the decision record that says what you may do with the bytes, and the ledger that says what the bytes are.

### 10. Checksums: Making a Citation a Research Claim

Online corpora drift. A page that resolved last year may serve different bytes today — a corrected typo, a different edition scan, a silently re-generated export, or a domain that changed hands. A citation that points at a URL without a checksum is a claim about *a thing that no longer provably exists*.

```python
import hashlib


def artifact_checksum(payload: bytes) -> str:
    """Pin a retrieved artifact: sha256 is deterministic across machines."""
    return "sha256:" + hashlib.sha256(payload).hexdigest()
```

- **What the checksum buys:** reproducibility. A research claim becomes (checksum, transformation log): anyone can re-fetch, re-hash, and prove they worked from the same bytes. The exercise demo hashes the same fixture twice and shows the digests identical — determinism is the point.
- **What it does not buy:** licensing (section 11), correctness of the content, or authenticity of the tradition's grading — it pins *your artifact*, nothing more.
- **The release rule:** every source has a checksum before any of its passages ship (GOV002). A missing checksum is a warning-severity finding, not critical, precisely because it is a reproducibility debt rather than a rights violation — but it is still a finding, and a release that accumulates them has no defensible citations left.

### 11. Licence Families and the Redistribution Line

The classical age is public domain; your copies are not automatically so. The families a builder will actually meet:

| Family | What is held | What it typically permits | Serving rule |
|---|---|---|---|
| **Public-domain classical text** (old editions, open scans) | The text itself, long out of copyright | Store, embed, quote, redistribute | Verbatim serving fine; record the decision anyway |
| **Modern critical edition** (publisher-held) | Editorial apparatus, introduction, typography — sometimes the text's specific digital form | Often: personal/academic use; sometimes quotation limits; digital redistribution unclear | Verbatim serving risky; prefer citation + short quotation; get the decision in writing per source |
| **Open corpus, open licence** (CC0/CC-BY-style terms) | Text + metadata under stated terms | As the licence says; attribution if required | Verbatim fine within the licence's terms |
| **Site with terms forbidding redistribution** | The site's compilation; sometimes thin claims over the underlying text | Reading on-site; **no republication, sometimes no bulk extraction** | Reference-only or summary; never verbatim serving (GOV003) |
| **API with extraction terms** | Programmatic access under a developer agreement | Often: rate-limited access; sometimes: no derived redistribution, no model-training use | Read the agreement; the retrieval date and terms version go in the record |

**The rule, stated once:** *you may hold a text without the right to republish it, and a RAG system that returns verbatim passages is publishing.* Holding = you stored the bytes for processing. Publishing = a user received the passage's content from your service. The distance between the two is exactly the `use_policy` field, decided per source (GOV003 fires when `no-redistribution` meets `served_verbatim: true`). Note the discipline the exercise models: the fatwa archive source in the GOOD pack is still *held* (its passages are in the manifest, with checksums) but served `reference-only` — the corpus keeps its provenance without committing republication.

**Writing a licence decision you can defend.** GOV001 accepts no vibes. A defensible decision names the artifact, the terms as read, the reader, the date, and the resulting use policy — a short paragraph a reviewer can re-check without asking you anything:

```text
source_id:     src-web-archive
artifact:      fatwa archive export, 2026-03-02 snapshot (sha256 recorded)
terms as read: "No bulk extraction; no republication of answers."
                (archive footer, retrieved 2026-03-02; terms page version 2025-11)
decision:      terms forbid republication. An export held for research is not
                republished; a RAG service returning answer text would be.
                Decision: no-redistribution. Reader: <name>, 2026-03-05.
use_policy:    no-redistribution  →  delivery: reference-only (attribution +
                coordinates; never served_verbatim)
embedding:     deferred — embedding-as-derivative unsettled under these terms;
                default no-embed per section 12 until a licence reading says otherwise
```

Compare the anti-patterns GOV001's detector cannot see but a reviewer should: "the text is ancient, so public domain" (no terms were read); "the site said free to read, so we can serve it" (free to read is not a licence to republish); "we decided project-wide that academic use is fair" (the decision is per source, and this source's terms speak for themselves). The worked decision above names the artifact, quotes the terms, and lands on a policy the delivery layer can enforce mechanically.

### 12. Derivatives: Chunks, Embeddings, and Indexes

Does chunking create a derivative work? Does embedding a passage into a vector store? Does a lexical index? There is no universal answer across licence families — and that is exactly why the decision belongs in the per-source record, not in a project-wide hope.

The conservative engineering stance this track teaches:

1. **Chunking** re-formats the text's boundaries; treat it as a transformation that must be logged (it is, in the transformation ledger) and whose output inherits the source's use policy.
2. **Embedding storage** is a lossy but real representation of the text. Treat it as *potentially* redistributive: a licence that forbids republication may or may not reach embeddings, but you do not get to decide that unilaterally per project — the decision is per source, recorded, and defaults to "do not embed from no-redistribution sources" until a licence reading says otherwise.
3. **Verbatim retrieval** is the clear redistribution line (section 11); indexes that return snippets are on the publishing side of it.
4. **The per-source rule:** the same corpus can hold a CC0 quran text (embed and serve verbatim) and a modern fatwa archive (reference-only, no embedding) side by side, because the decision travels with the source record, not with the deployment.

### 13. PII and Living Persons

Biographical data about historical scholars is heritage, not PII. Two other corpus contents are not:

- **Living people's names** appear in modern compilations — editors, contemporary narrators in live chains, respondents in archives. Their presence in a published corpus is a decision, not a default.
- **Modern fatwa archives contain personal questions**: health details, family disputes, financial specifics, asked by real individuals. A question archived with its answer may identify or re-identify its asker years later.

The handling ladder, cheapest first:

1. **Detect** at ingestion: fatwa-archive sources are flagged in their source record; date-and-name heuristics surface modern-era personal material for review.
2. **Classify**: historical (heritage), modern-public (a living scholar's published work — attribution is usually *wanted*), modern-personal (an individual's question — restrict).
3. **Restrict delivery**: modern-personal material is reference-only at minimum, and often excluded. The GOOD pack's fatwa chunk demonstrates the delivery control: present, attributed, never served verbatim to end users.
4. **Never** feed personal fatwa-archive text into a generation prompt as if it were general fiqh reference — the model will paraphrase someone's private case into a public answer.

### 14. Audit Logging That Is Defensible Without Being Surveillance

When a user asks a question about, say, a weak report and the system answers, someone will eventually ask: *what did the system serve, and on whose authority?* The governance answer is a Q&A log with a fixed, minimal schema — and a stated retention limit, because an unbounded log of users' religious questions is a surveillance archive, not a governance artifact.

**What the log records (GOV009 requires the first three):**

| Field | Why it is in the log |
|---|---|
| Question (as asked) | What was actually requested |
| **Retrieved chunk ids** | What the system served from — the join back to category ledgers and source records |
| **Model version** | Which generator produced the prose; answers are not reproducible without it |
| Refusal flag + reason | Whether the refusal path fired, and which boundary it hit |
| User feedback (if given) | Whether the user marked the answer wrong — the governance signal that starts a review |

**What is deliberately not in the log:** user identity beyond what the deployment already requires for access, free-form profiling, anything derived from the question beyond the retrieval trace. **Retention:** a stated limit (the exercise's GOOD pack sets 90 days) with an automated purge; the log exists so a disputed answer can be reconstructed during the retention window, not so a population's questions can be studied for years. This lecture owns the log's *contents and retention policy*; the mechanics of log pipelines, alerting, and incident response belong to the security track's monitoring lecture (`projects/04-ai-engineering/security/lectures/10-security-monitoring-lecture.md`) and are not repeated here.

### 15. Worked Scenario: One Question Through the Governed Pipeline

A user asks: "What is the ruling on X for someone in my situation?" — fatwa-substance by construction.

```text
 t=0    question arrives
 t=1    fatwa-substance detector fires (personal, actionable)
        │  extractable fallback: "what do the sources say about X?"
 t=2    retrieval runs with category filters over tagged chunks only
        │  hits: quran 2:255 (GOV010-valid coordinates),
        │        tafsir vol.1 p.45 (attributed), fiqh school-S vol.1 p.42,
        │        fatwa chunk — flagged no-redistribution → reference-only
 t=3    answer layer: quran quoted verbatim with coordinate;
        │  tafsir introduced as commentary with its own coordinates;
        │  fiqh position named with its school — never "the ruling";
        │  fatwa chunk contributes attribution only, not verbatim text
 t=4    refusal fires: boundary stated, citations listed, handoff named
 t=5    audit log: question + chunk ids + model version + refusal flag=true
 t=90d  retention job purges the log entry per policy
```

Every line maps to a rule or a section: category filtering (GOV004, section 8), coordinates (GOV007/010, section 8), inherited grades displayed not smoothed (GOV005, section 4), redistribution policy enforced at delivery (GOV003, section 11), refusal (GOV008, section 7), log (GOV009, section 14), retention (section 14).

**The release checklist this track ends on:**

| # | Gate | Rule |
|---|---|---|
| 1 | Every source has a licence decision and a checksum | GOV001, GOV002 |
| 2 | Every passage traces to a source record | section 9 |
| 3 | Grades are attached as inherited metadata with graders | GOV005 |
| 4 | Category tags are set and checked | GOV004, GOV010 |
| 5 | Isnad/matn linkage survives chunking | GOV006 |
| 6 | Citations carry scholar-checkable coordinates | GOV007 |
| 7 | Refusal is implemented, configured, and tested | GOV008 |
| 8 | Audit log is in place with retention stated | GOV009 |
| 9 | Redistribution policy enforced at delivery | GOV003 |

A corpus that passes all nine is not "approved by this system as religiously correct" — it is *governed*: its categories are honest, its grades are inherited and attributed, its citations are checkable, its licences are decided, and its refusals are designed. That is the whole claim this track makes, and it is the only claim a system may make.

**The same question, ungoverned.** Run the same user question through the pipeline as most teams actually ship it — undifferentiated chunks, no source records, no refusal path — and the difference is not subtle:

```text
 t=0    question arrives: "What is the ruling on X for someone in my situation?"
 t=1    no fatwa-substance detector; retrieval treats it like any query
 t=2    top-k over one pooled index:
        │  chunk: matn of a daʿif report   (no grade stored)
        │  chunk: tafsir paraphrase of 2:255 (no category tag)
        │  chunk: fatwa-archive answer, verbatim (no use policy recorded)
        │  chunk: one school's fiqh position (no school field)
 t=3    generator composes, with no discipline holding it back:
        │  "The ruling is that X is permissible. Allah says: the Living,
        │   the Self-Subsisting [.. blended paraphrase ..]. A hadith
        │   confirms this [.. orphaned matn, no narrators named ..].
        │   As for the weakness mentioned in some narrations, the
        │   report is in fact sahih [.. system re-graded, silently ..]."
 t=4    user receives a fatwa: definite article, blended revelation,
        │  invented grade, a private fatwa-archive answer paraphrased
        │  into public fiqh, and zero coordinates anyone could check
 t=5    nothing is logged; six months later nobody can reconstruct
        │  which chunks produced this answer or which licence
        │  forbade serving one of them verbatim
```

Every line of the failure traces to a missing gate: GOV004 (no tags → category blend), GOV005 (no grade field → silent re-grade), GOV006 (orphaned matn → narrators vanishing), GOV007/GOV010 (no checkable coordinates), GOV003 (verbatim from an unlicensed pool), GOV008 (no refusal → fatwa issued), GOV009 (no log → unreconstructable). The governed pipeline does not answer this question with a ruling — it refuses, cites, hands off, and logs. That refusal *is* the product behaving correctly.

### Rule Map: GOV001–GOV010 Against This Lecture

The exercise's ten rules, their home sections, and the fixture that trips them in the BAD pack — the one-page index to run the whole lecture against:

| Rule | Severity | Lecture section | What it demands | BAD fixture that trips it |
|---|---|---|---|---|
| GOV001 | critical | 9, 11 | Every source carries a licence decision before any passage ships | `src-classical` — classical text, no decision recorded |
| GOV002 | warning | 10 | Every source carries a sha256 checksum of the retrieved artifact | `src-web-archive` — retrieved, never hashed |
| GOV003 | critical | 11, 12 | No-redistribution sources are never served verbatim | `bad-p-fatwa` — archive chunk, `served_verbatim: true` |
| GOV004 | critical | 2, 8 | Every passage carries one of the ten closed-set categories | `bad-p-untagged` — `category: "missing"` |
| GOV005 | critical | 4 | Every hadith passage carries inherited grade metadata with grader | `bad-p-hadith-nograde` — grade field absent |
| GOV006 | critical | 3, 5 | Every report text has its isnad or a link to the chunk that does | `bad-p-matn` — no chain, `isnad_link: null` |
| GOV007 | warning | 8, 9 | Citations carry scholar-checkable coordinates | `bad-p-tafsir` — work named, no volume/page or locator |
| GOV008 | critical | 6, 7 | Refusal template and handoff target are configured | config — template and handoff both absent |
| GOV009 | warning | 14 | Audit log records chunk ids and model version | log entry — both fields missing |
| GOV010 | critical | 2, 8 | Quranic coordinates validate: surah 1–114, ayah in range | `bad-p-ayah` — surah 2, ayah 300 |

The GOOD pack at the bottom of the exercise file satisfies all ten and every design rule behind them; it is the reference implementation this lecture's tables describe, executable on any machine with Python 3.11+ and no network.

---

## Common Mistakes to Avoid

### 1. Storing a Grade Without Its Grader

```python
# ❌ BAD: an anonymous verdict; the system has silently adopted it
passage.grade = "sahih"

# ✅ GOOD: inherited metadata, attributed, with the system's non-verb
passage.grade = {
    "value": "sahih",
    "grader": "the source edition's own grading apparatus",
    "note": "inherited metadata; the system does not re-grade",
}
```

### 2. Fixed-Size Chunking With No Isnad Linkage

```text
❌ BAD:  chunk 7 = isnad ... | chunk 8 = matn ...   (no ids, no links)
         → GOV006: the report's chain of custody is gone

✅ GOOD: chunk 7 = isnad (isnad_present=true)
         chunk 8 = matn  (isnad_present=false, isnad_link="chunk-7")
```

### 3. A Citation That Names the Work but Not the Coordinates

```python
# ❌ BAD: unverifiable decoration
citation = Citation(work="Sunan al-X")

# ✅ GOOD: what a scholar would actually check
citation = Citation(work="Sunan al-X (verified edition)", volume=3, page=212)
# or: Citation(work="Sunan al-X (verified edition)", locator="hadith no. 4949")
```

### 4. Answering a Fatwa-Substance Question "Helpfully"

```text
❌ BAD:  "The ruling is that X is permissible in your case."  ← a fatwa,
         issued by a model, dressed in retrieved citations

✅ GOOD: refuse by design: state the boundary, cite what the corpus can
         support (positions as recorded, with coordinates), hand off to a
         configured trustworthy source or scholar — and log the refusal
```

### 5. Serving No-Redistribution Text Verbatim

```python
# ❌ BAD: the source's terms forbid republication; this is publishing
if retrieved:
    answer = f"النص كما ورد: {passage.original}"

# ✅ GOOD: delivery mode follows the source's use policy
if source.use_policy == "no-redistribution":
    answer = reference_only(passage)  # attribution + coordinates, no verbatim text
```

### 6. One Retrieval Pool for Every Category

```text
❌ BAD:  quran + hadith + tafsir + fiqh + fatwa in one undifferentiated index
         → the model blends categories and the citation line lies

✅ GOOD: category tags checked at retrieval; quran quoted verbatim with
         coordinates; commentary labeled as commentary; fiqh named with
         its school; fatwa reference-only
```

---

## Best Practices

1. **Treat category and provenance as one governance contract** — two ledgers on every passage, audited together before release
2. **Tag every passage at ingestion** from the closed category set, and refuse to index untagged text (GOV004)
3. **Validate quranic coordinates** against surah range and known ayah counts; a wrong coordinate misplaces a revelation (GOV010)
4. **Keep the isnad with the matn**, or leave an `isnad_link` when chunking splits them (GOV006)
5. **Carry grades as inherited metadata** with grader attribution and a "system does not re-grade" note (GOV005)
6. **Never smooth grade distinctions** in generated prose; display the inherited labels when juxtaposing reports
7. **Present disagreements side by side** with school/scholar attribution; never adjudicate, never definite-article a school's position into "the ruling"
8. **Detect fatwa-substance questions and refuse by design** — boundary, citations, handoff — and test all three paths before release (GOV008)
9. **Record one provenance record per source**: origin, licence decision, terms as they read, retrieval date, checksum, transformations, use policy (GOV001, GOV002)
10. **Checksum every retrieved artifact**; treat a citation without one as a claim about a thing that no longer provably exists
11. **Decide redistribution per source**, not per project; verbatim serving from a no-redistribution source is republication (GOV003)
12. **Treat embeddings and indexes as potentially redistributive**; default to "no embed" from no-redistribution sources until the licence reading says otherwise
13. **Flag modern-personal material** (fatwa-archive questions, living-person data) at ingestion and restrict its delivery
14. **Log questions, chunk ids, model version, refusals, and feedback** under a stated retention limit — defensible, not surveillant (GOV009)
15. **Quote quranic text verbatim with coordinates**; introduce commentary as commentary, with its own coordinates
16. **Run the release checklist (section 15) as a gate**, and keep the audit deterministic: the same manifest must always produce the same findings

---

## Practice Exercises

### Exercise 1: Map Every Finding to Its Section
Run `exercises/01-islamic-domain-governance.py` and take each of the ten BAD-pack findings. For each, write the lecture section that explains why it is a violation and the real-world incident shape it prevents (e.g., GOV006 → a user asking about a report and receiving a matn with no narrators). Then confirm the GOOD pack raises zero and explain why weakening a sample to clear a finding is the wrong fix.

### Exercise 2: Category-Tag a Real Page
Take one of Athar's sample pages (`projects/04-ai-engineering/athar-lab/sample_pages/book_p1.txt` through `book_p10.txt`) and tag every passage boundary you can identify with a category from the closed set. Where a single page mixes categories (a fiqh text citing shawahid, for example), write the chunking rule that would keep the tags honest.

### Exercise 3: Write a Provenance Record You Can Defend
Pick one Islamic-text source you are allowed to use. Read its terms of use as they actually are today. Fill the `SourceRecord` schema — origin, licence decision, terms, retrieval date, checksum of the file you actually downloaded, use policy — and state in one sentence what the use policy permits you to do with a verbatim excerpt.

### Exercise 4: Refusal Templates, Both Languages
Write the three-part refusal (boundary, citations, handoff) in English and in Arabic, modeled on the exercise's GOOD template. Test it against three fatwa-substance questions and three extractable questions; for each, write what the citation section would link to in *your* corpus.

### Exercise 5: Release Checklist Dry-Run Against Athar
Run the section-15 checklist against Athar's stage-1 contracts. Which gates are already structurally enforced (SourceLocation invariants, two-text discipline), which are unimplemented (category tags, grades, licences, refusal, audit), and what is the first contract change you would propose to close the cheapest gap?

---

## Summary

1. **One discipline, two ledgers.** Every passage carries what the text IS (category, inherited grade, linkage, coordinates) and where the artifact CAME FROM (source record, licence, checksum, use policy); a release is defensible only when both are complete.
2. **Categories are not labels; they are authority types.** Quran, hadith, athar, tafsir, fiqh, qawa'id/usul, fatwa, shawahid, taqrid differ in who speaks and with what standing; conflating them is a category error with religious consequence, caught mechanically by tagging and checking (GOV004, GOV010).
3. **Reports are isnad plus matn, and grading is inherited.** The chain is data, not preamble; grades travel as attributed metadata from named graders who sometimes disagree; the system never grades, upgrades, or launders (GOV005, GOV006).
4. **Disagreement is legitimate; adjudication is not the system's.** Explain, extract, compare — with school attribution, side by side — and route fatwa-substance questions through a designed, tested refusal with a named handoff (GOV008).
5. **Ancient text, modern artifact.** Licence families decide what holding buys you, and verbatim RAG serving is publishing: redistribution policy is per source, enforced at delivery (GOV003), with checksums pinning every claim (GOV002).
6. **Derivatives and persons need the same discipline.** Embeddings and indexes are potentially redistributive; modern-personal material is restricted; both decisions live in per-source records, not project-wide defaults.
7. **The audit log is the governance receipt.** Question, chunk ids, model version, refusal flag, feedback — retained under a stated limit, purged on schedule (GOV009), defensible without being surveillant.
8. **The never-list is the product's spine.** No fatwas, no adjudication, no re-grading, no chain-completing, no category-blending, no verbatim republication, no unnamed "ruling," no private-case leakage (section 7) — a refusal that observes all eight is the product behaving correctly, not a feature failure.

**Next lecture (planned):** Lecture 02 — governed ingestion in practice: wiring GOV001-GOV010 into Athar's pipeline contracts, from source acquisition through tagging, linkage, and the release gate.
