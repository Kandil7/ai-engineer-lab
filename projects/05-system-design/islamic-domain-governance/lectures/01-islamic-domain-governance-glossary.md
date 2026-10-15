# Glossary: Islamic-Domain Literacy and Corpus Governance

Quick-reference table of every term used in Lecture 01, followed by detailed definitions with the schema fragments, fixture shapes, or rule codes you will actually meet in `exercises/01-islamic-domain-governance.py` and in Athar's contracts. Where a discipline boundary matters, the definition says which adjacent track owns the rest: Arabic NLP owns text mechanics and entity canonization, the security track owns attack and privacy mechanics, the data-engineering track owns pipeline lineage — this glossary owns the governance vocabulary that sits on top of them.

## The Ten Rules in Ten Lines

A one-viewport entry point before the full table; each line is the exercise's rule in its own words, with the full definition below:

1. **GOV001** — no licence decision recorded, no passage from that source ships.
2. **GOV002** — no sha256 of the retrieved artifact, the citation is not reproducible.
3. **GOV003** — no-redistribution source served verbatim, the service is publishing.
4. **GOV004** — no closed-set category tag, the pool is an authority error waiting to happen.
5. **GOV005** — hadith without inherited grade metadata, the system has silently re-graded.
6. **GOV006** — matn without its isnad or a link to it, the chain of custody is gone.
7. **GOV007** — citation without scholar-checkable coordinates, the reference is decoration.
8. **GOV008** — refusal template or handoff unconfigured, fatwa-substance questions get answered.
9. **GOV009** — audit log missing chunk ids or model version, a disputed answer is unreconstructable.
10. **GOV010** — surah:ayah outside validated range, a revelation is misattributed.

## Quick Reference Table

| Term | Definition | Lecture section |
|------|------------|-----------------|
| Ahad | Single-chain report at some link; the transmission-strength axis's other pole from mutawatir | 5 |
| Athar | Companion or successor report, same isnad/matn discipline as hadith | 2 |
| Audit Log (governance) | Q&A receipt: question, chunk ids, model version, refusal flag, feedback, retention-limited | 14 |
| Ayah | One verse of the quran; citation coordinate paired with its surah | 2 |
| Category Tag | Closed-set label (quran/hadith/athar/tafsir/fiqh/fatwa/...) set at ingestion, checked at retrieval | 2 |
| Checksum | sha256 of the retrieved artifact; pins a citation to bytes that provably existed | 10 |
| Citation Coordinates | Work plus volume/page, equivalent locator, or surah:ayah — what a scholar would check | 8 |
| Corpus Manifest | The audited description: sources, passages, governance config | 15 |
| Daʿif | "Weak" grade label in the inherited apparatus; never served beside a sahih report undistinguished | 4 |
| Derivative Work | Chunk/embedding/index output treated as potentially inheriting the source's restrictions | 12 |
| Fatwa | A named mufti's answer to a specific question in a specific context | 2 |
| Fatwa-Substance | Personal, context-bound, actionable ruling question — the refusal trigger | 6 |
| Fiqh | Jurisprudence: a school's or scholar's derived rulings | 2 |
| Grade (inherited) | {value, grader, note} metadata inherited from the source's apparatus; never the system's verdict | 4 |
| Grader | The named scholar/collection whose judgment a grade is attributed to | 4 |
| Hadith | Prophetic report: saying, action, or approval, through a chain of narrators | 2 |
| Hadith Qudsi | Report whose content is from Allah with the Prophet's wording; its own category of care | 5 |
| Hanafi / Maliki / Shafi'i / Hanbali | The four Sunni schools; their ikhtilaf is legitimate and recorded | 6 |
| Handoff Target | Configured trustworthy destination for refused fatwa-substance questions | 7 |
| Hasan | "Good" grade label, slightly below sahih in the classical apparatus | 4 |
| Ijmaʿ | Consensus where the tradition itself records it; never asserted by the system | 6 |
| Ikhtilaf | Recorded scholarly disagreement; presented side by side, never adjudicated | 6 |
| Independent Legal Reasoning | See Ijtihad | 5 |
| Ijtihad | Qualified independent legal reasoning; a derived ruling is not a transmitted one | 5 |
| Isnad | The chain of narration: who reported from whom, back to its origin | 3 |
| Madhhab | A school of law with continuous scholarship and settled positions | 6 |
| Matn | The report text itself, the content the isnad transmits | 3 |
| Maqtuʿ | Chain deliberately ended at a companion or successor; do not upgrade it to prophecy | 5 |
| Mawduʿ | "Fabricated" grade label per a named grader's judgment; fenced, not surfaced as live proof | 4 |
| Muʿallaq | Chain suspended at its head; do not render it as fully connected | 5 |
| Mursal | Chain missing a Companion link; do not silently close the gap | 5 |
| Mutawatir | Mass-transmitted report; strength signal a naive pipeline flattens away | 5 |
| Provenance Record | Per-source: origin, licence decision, terms, retrieval date, checksum, use policy | 9 |
| Qawa'id | Legal maxims scholarship; theory, not case law | 2 |
| Qiraʾa / Riwaya | A reading or transmission variant; never silently canonicalized away | 5 |
| Quran | Divine revelation; quoted verbatim with surah:ayah coordinates | 2 |
| Redistribution Line | Holding bytes is not republishing them; verbatim RAG serving crosses the line | 11 |
| Reference-Only Delivery | Attribution plus coordinates without verbatim text; the no-redistribution default | 11 |
| Retention Limit | Stated purge window for the audit log; unbounded logs are surveillance archives | 14 |
| Rijal ('ilm al-rijal) | The biographical science behind isnad evaluation; the inherited apparatus's evidence base | 3 |
| Sahih | "Sound" grade label in the classical apparatus; served with grader visible | 4 |
| Sanad | Variant spelling of isnad | 3 |
| Served-Verbatim | Delivery flag: the user receives the passage's verbatim text | 11 |
| Shahid / Shawahid | Supporting evidence quoted inside another work; do not detach and re-serve freestanding | 2 |
| Sunnah | The Prophet's established path (sayings, actions, approvals) | 5 |
| Surah | A chapter of the quran; the first half of the ayah coordinate | 2 |
| Taqrid | A scholar's endorsement of a position; travels as attributed metadata | 2 |
| Tafsir | Exegesis: a named scholar's reading of a text; never served as the quran itself | 2 |
| Taqlid | Following a school's settled position; one school is never "the default" | 5 |
| Two-Text Discipline | Verbatim original for display/citation, normalized copy for matching (Arabic NLP 02; Athar contracts) | 8 |
| Usul al-Fiqh | Legal theory: the sources and methods of derivation | 2 |
| Use Policy | Per-source decision: redistribution-ok, no-redistribution, ... — GOV003's input | 11 |
| Verbatim Serving | Returning the passage's exact text to the user; publishing under section 11's rule | 11 |

## Detailed Definitions

### Isnad

The chain of narration (also spelled sanad): the sequence of named narrators through whom a report reached the book you are holding. Each link asserts "X heard/received from Y," and the tradition's own biographical science (`ilm al-rijal`) evaluates those names. The isnad is the report's chain of custody, and a corpus that strips it as preamble deletes exactly the metadata the tradition used to evaluate the text.

```text
isnad:  عَنْ عُمَرَ بْنِ الْخَطَّابِ رضي الله عنه، قَالَ: سَمِعْتُ رَسُولَ
        اللَّهِ صلى الله عليه وسلم يَقُولُ:
        └── one Companion-level link; longer chains name each narrator
```

In the exercise, every hadith/athar passage either carries its isnad (`isnad_present: true`) or links to the chunk that does (`isnad_link: "<chunk-id>"`); an orphaned matn is GOV006.

### Matn

The report text itself — the saying, action, or approval being transmitted. Grading applies to the (isnad + matn) pair as evaluated by a grader, not to either half alone. A chunker may place matn and isnad in different chunks, but the linkage must survive; see the exercise fixtures `good-p-isnad` and `good-p-matn` for the linked shape.

### Grade (Inherited Metadata)

The tradition's quality label (sahih, hasan, daʿif, mawduʿ, among others), carried in the corpus as data inherited from the source's apparatus. The system stores it, displays it when relevant, and never issues one:

```json
{
  "grade": {
    "value": "sahih",
    "grader": "the source edition's own grading apparatus",
    "note": "inherited metadata; the system does not re-grade"
  }
}
```

The `grader` field is what keeps the grade honest: graders disagree, and disagreement is part of the inherited record. A grade without attribution is an anonymous verdict — GOV005 rejects a hadith passage without the field entirely, and the design rule rejects a grade without its grader.

### Grade Labels: Sahih, Hasan, Daʿif, Mawduʿ

The four labels a builder will meet most often in Sunni hadith apparatus. They are *inherited* values the corpus stores, never values the system assigns:

| Label | What the apparatus means by it | What the pipeline must not do |
|---|---|---|
| **sahih** | Sound: the report meets the classical conditions (continuous chain, reliable narrators, no hidden defect) | Serve it without showing the grader's attribution; treat "sahih" as a universal verdict across graders |
| **hasan** | Good: sound but with a lesser defect in chain or narrator — still usable as evidence in the tradition's own terms | Flatten it to sahih "for simplicity," or drop the distinction when juxtaposing with a sahih report |
| **daʿif** | Weak: fails one or more classical conditions | Serve it beside a sahih report with identical framing; let the generator write "scholars mention that..." with no distinction |
| **mawduʿ** | Fabricated: judged by a named scholar as not authentic to its claimed origin | Serve it as live proof of anything; it stays in the corpus as an object of study, fenced by its inherited label |

A corpus may carry multiple grades per report, one per grader, because graders disagree about the same text. The system's display shows the attributed set; it never picks a winner, and it never upgrades a daʿif report's serving with confident prose.

### Grader

The named scholar or collection whose judgment a grade is attributed to. Because graders disagree about the same report, a corpus may legitimately carry multiple inherited grades per passage, each with its grader; the system's job is to display the attributed set, not to pick a winner.

### Mutawatir and Ahad

The transmission-strength axis. Mutawatir reports are mass-transmitted at every link; ahad reports have a single chain at some link. A naive pipeline serves both identically and loses the signal the tradition's own usage depends on. Preserve whatever strength label the source's apparatus carries; never invent one.

### Mursal, Muʿallaq, Maqtuʿ

Three chain shapes whose names are warnings: mursal (a Companion link missing), muʿallaq (the chain suspended at its head, often because the book cites without its "heard from"), maqtuʿ (deliberately ended at a companion or successor). The pipeline preserves the label and never silently completes or extends a chain — doing so would upgrade the report's apparent authority beyond what its transmitters claimed.

### Qiraʾa / Riwaya

A reading or transmission variant. Where sources differ in wording, the corpus preserves each variant with its attribution; the display layer never collapses variants into one "clean" text. This intersects with Arabic NLP 09's display-versus-working-copy rule: the display copy keeps the source form; only the matching key is normalized.

### Isnad Vocabulary in One Line

`isnad` → who; `matn` → what; `rijal` → the biographical science of the who; `qiraʾa/riwaya` → which variant; `sunnah` → the Prophet's path the reports transmit; `hadith qudsi` → content from Allah in the Prophet's wording, its own category of care.

### Quran

Divine revelation, the primary text of the corpus. Two mechanical rules: quoted **verbatim** (the display copy is the text, never a paraphrase presented as the text) and cited by **surah:ayah** with validation (GOV010: surah 1..114, ayah within the surah's known count). A tafsir passage discussing an ayah carries its own category and coordinates; the commentator's words are never blended into the quranic quote.

### Surah and Ayah

A surah is a chapter; an ayah is a verse. The coordinate pair (surah, ayah) is the quran's citation system, and it is the one coordinate type the exercise validates numerically:

```python
AYAH_COUNTS = {1: 7, 2: 286, 103: 3, 112: 4, 113: 5, 114: 6}
# surah 2, ayah 300 → GOV010: outside the count; a coordinate error, not a dispute
```

### Hadith

A prophetic report: what the Prophet said, did, or approved, transmitted through narrators. In the corpus it is a category (`hadith`), it carries the isnad/matn discipline, and every passage so tagged must carry its inherited grade (GOV005).

### Athar

A companion or successor report — same chain discipline as hadith, different speaker. The category tag prevents the pipeline's most embarrassing upgrade: serving a companion's word in the Prophet's voice. GOV006 applies to athar exactly as to hadith.

### Hadith Qudsi

A report whose content is from Allah delivered in the Prophet's wording — a category the tradition keeps distinct from both quran and ordinary hadith. In a corpus it must never be filed under `quran` (its wording is not revelation in the quranic sense) nor served without its distinct label.

### Sunnah

The Prophet's established path: sayings, actions, and approvals, as transmitted through the hadith and athar collections. In conversation, builders reach for "sunnah" as a vague synonym for "islamically good"; in the corpus it is the *content domain* the hadith category serves, not a quality label. A passage is not "more sunnah" because it is shorter or more fluent — the transmission record is what establishes standing, and the system preserves that record rather than improvising from tone.

### Tafsir

Exegesis: a named scholar's or school's reading of a text. Retrieval loves tafsir because it is fluent and explanatory — which is exactly why blending it into quranic quotes is failure mode 4. Rule: tafsir passages carry their own category, their own coordinates (work + volume/page), and are introduced as commentary.

### Fiqh

Jurisprudence: derived rulings of a school or scholar. In the corpus, a fiqh passage is always *somebody's* fiqh; the presentation rule attaches the school or author, and the definite article "the ruling" is never used without that attribution.

### Qawa'id and Usul al-Fiqh

Legal maxims and legal theory — the scholarship about how rulings are derived, not case law. A maxim quoted without its theory context is as misleadable as a ruling without its school; tag these as their own categories (`qawaid`, `usul`) so they do not surface as answers to case questions.

### Shahid / Shawahid

Supporting evidence quoted *inside* another work — a fiqh manual citing hadiths to support a position, a tafsir quoting reports about an ayah. The shawahid passage in the manual is not the hadith collection's entry; it is the manual's quotation of it. The category tag (`shawahid`) keeps the two distinct, and the rule is: never detach a shahid from its quoting work and re-serve it freestanding as if it were the primary source — the chain, edition, and grading may differ from the primary collection's, and the citation must name the work actually held.

### Taqrid

A scholar's endorsement of a recorded position — a note that so-and-so accepted a given ruling, traveling as attributed metadata. In the corpus it is its own category (`taqrid`) because it is neither the original ruling nor independent evidence: it is a named scholar's thumbs-up, and it is displayed with that attribution.

### Fatwa

A named mufti's answer to a specific question, at a specific time, about a specific situation. Context-bound by construction. In the corpus it is tagged `fatwa`, typically served reference-only, and its personal-question content triggers the section-13 handling ladder when modern.

### Fatwa-Substance

The refusal trigger: a question that, whatever its wording, asks for a ruling for the asker's own case. "Is X permissible for me?" is fatwa-substance; "What does school S say about X in book B?" is extractable. The detector errs toward refusal on ambiguity, and the refusal is logged.

### Madhhab

A school of law. The four Sunni schools — Hanafi, Maliki, Shafi'i, Hanbali — are named after their founding scholars in the tradition's own shorthand, each with continuous scholarship and codified positions. The corpus records which school a position belongs to; it never merges them into a synthetic "Islamic view."

### Ikhtilaf

Recorded scholarly disagreement. The system's presentation rule: side-by-side, each position with its school, scholar, and coordinates. Never adjudicated, never smoothed into consensus the sources do not claim.

### Ijmaʿ

Consensus where the tradition itself records it. The system may extract a source's claim of ijmaʿ (attributed to that source); it may never assert consensus on its own authority.

### Ijtihad and Taqlid

Ijtihad is qualified independent legal reasoning; taqlid is following a school's settled position. A derived ruling (ijtihad) and a transmitted report are different objects in the corpus: never present a derivation with the confidence of a transmission.

### Hanafi / Maliki / Shafi'i / Hanbali

The four Sunni schools as named in the tradition. Their positions on a question may differ, and the corpus presents the differences it actually holds — attributed, side by side — as section 6's design rule requires.

### Refusal Path and Refusal Template

The designed response to fatwa-substance questions: (1) boundary statement, (2) citations of what the corpus can support, (3) handoff to a configured trustworthy target. The template is configuration (GOV008 requires template and handoff both present), rendered by the exercise's `render_refusal`, and its refusals are audit-logged with a refusal flag.

### Handoff Target

The named destination for refused questions: a trusted reference collection, a school's official fatwa board, or a qualified scholar — chosen per deployment, not improvised per request. Missing handoff is part of GOV008.

### Category Tag

The closed-set label applied at ingestion and checked at retrieval:

```text
quran | hadith | athar | tafsir | fiqh | fatwa | qawaid | usul | shawahid | taqrid
```

Missing or out-of-set is GOV004. The set is closed on purpose: open-vocabulary "topics" would let the pool reflatten the moment a new importer ran.

### Citation Coordinates

What a scholar would check: work plus volume/page, an equivalent locator (hadith number, entry id), or surah:ayah. Book-title-only citations are GOV007 — decoration, not verification.

```python
Citation(work="Sunan al-X (verified edition)", volume=3, page=212)
Citation(work="Sunan al-X (verified edition)", locator="hadith no. 4949")
Citation(work="al-Quran al-Karim", surah=2, ayah=255)
```

### Provenance Record (SourceRecord)

The per-source governance record — origin, licence decision, terms of use as they actually read, retrieval date, checksum, use policy. Every passage joins to one via `source_id`; a passage whose source has no licence decision is unshippable (GOV001).

### Checksum

sha256 of the retrieved artifact. It pins a research claim to bytes that provably existed; online corpora drift, and a citation without a checksum is a claim about something no longer provably there (GOV002). It buys reproducibility, nothing more — not licensing, not correctness.

### Licence Decision and Terms of Use

The licence decision is a human's recorded reading of how the terms *actually* read for this source (not "the text is ancient"); the terms-of-use field preserves what was read so the decision is checkable. Missing decision is GOV001; the families and their consequences are lecture section 11.

### Use Policy and Redistribution Line

`use_policy` is what *this corpus* decided it may do with this source: `redistribution-ok`, `no-redistribution`, and so on. The line: holding bytes is not republishing them, but a RAG answer that returns verbatim text *is* publishing. GOV003 fires when a `no-redistribution` source's passage is served verbatim; the GOOD fixture instead stores the fatwa-archive passage reference-only.

### Reference-Only Delivery

Attribution plus coordinates without verbatim text. The default for no-redistribution sources and for modern-personal material: the user learns the passage exists and where to check it, without your service republishing its content.

### Derivative Work (Chunks, Embeddings, Indexes)

Output that re-forms or re-encodes the source. Chunking is a logged transformation inheriting the source's use policy; embedding storage is treated as potentially redistributive; verbatim-retrieval indexes sit on the publishing side of the redistribution line. The decision is recorded per source — one corpus may hold CC0 material served verbatim beside no-redistribution material served by reference.

### Two-Text Discipline

The verbatim `original` for display/citation and normalized `searchable` copy for matching — taught in Arabic NLP 02 (`projects/04-ai-engineering/arabic-nlp/02-arabic-normalization-tokenization/`, lines 184-187) and enforced in Athar's `Passage.__post_init__` (`projects/04-ai-engineering/athar-lab/contracts.py:59-75`). This track's category ledger depends on it: the quranic quote and the displayed matn come from the original, always.

### Served-Verbatim (Delivery Flag)

`passage.served_verbatim` records whether the user receives the passage's exact text. It is the flag GOV003 checks against the source's use policy, and the flag the section-13 ladder flips to false for modern-personal material.

### Audit Log (Governance Receipt)

The Q&A log with a fixed minimal schema: question, retrieved chunk ids, model version, refusal flag, optional user feedback — retained under a stated limit (the GOOD fixture sets 90 days) and purged on schedule. Missing chunk ids or model version is GOV009; unbounded retention is the surveillance anti-pattern section 14 names.

### Retention Limit

The stated purge window for governance logs. Long enough to reconstruct a disputed answer during review; short enough that the log never becomes an archive of users' religious questions. It is configuration, and stating it is part of the release checklist.

### Modern-Personal Classification

One of the three labels the section-13 handling ladder assigns at ingestion, the one that triggers delivery restriction:

| Label | What it covers | Delivery default |
|---|---|---|
| **historical** | Classical scholarship and biographies of deceased scholars — heritage data | Verbatim within use policy |
| **modern-public** | A living scholar's published work, encyclopedic entries, public lectures | Verbatim within use policy; attribution usually *wanted* |
| **modern-personal** | An individual's fatwa-archive question, private correspondence, case details | Reference-only at minimum; often excluded; never fed to generation prompts as general reference |

The classification lives on the passage (or is inherited from a source-level flag like "this is a personal-question fatwa archive"), and GOV003's delivery check plus the section-13 ladder enforce it alongside the licence-driven use policy. A source can be licence-clean and still carry modern-personal passages: the two ledgers are independent, and both must pass.

## Severity Rationale: Why Critical vs Warning

The detector's severities are not arbitrary weightings; each maps to what fails if the finding ships:

| Finding | Severity | What breaks if it ships |
|---|---|---|
| GOV001 no licence decision | critical | The corpus cannot say what it may do with the bytes; every downstream use is legally unfounded |
| GOV003 verbatim from no-redistribution | critical | Your service is publishing text its terms forbid — a rights violation, live, per request |
| GOV004 missing category tag | critical | Category errors with religious consequence become possible in every answer that touches the chunk |
| GOV005 hadith without grade field | critical | The system implicitly adopts a grading it has no authority to issue; weak reports pass as ungraded |
| GOV006 orphaned matn | critical | The report's chain of custody is gone; the user cannot see who narrated what |
| GOV008 refusal path unconfigured | critical | Fatwa-substance questions get "helpfully" answered — the system issues rulings |
| GOV010 invalid quranic coordinate | critical | A revelation is misattributed to a location it does not occupy |
| GOV002 no checksum | warning | Citations from that source are unverifiable claims about drifting bytes; reproducibility debt, rights intact |
| GOV007 citation without coordinates | warning | Verification is decorated away; the citation misleads a scholar or skeptic trying to check it |
| GOV009 audit log incomplete | warning | A disputed answer cannot be reconstructed; governance review is blind for that Q&A |

The pattern: **critical** = something the system is currently *doing wrong* to the user or to the tradition's authority structure (publishing, ruling, misattributing, erasing chains). **Warning** = something the system is currently *unable to prove or reconstruct* (drifting artifacts, unchecked citations, blind logs). Both block a clean release — the checklist treats all ten as gates — but the severity tells the repair queue what is on fire versus what is accruing debt.

### Corpus Manifest

The audited input: sources, passages, and governance config, as the exercise's `PACK_BAD`/`PACK_GOOD` (or a JSON file with the same shape) express it. File mode loads it with `utf-8-sig` so Windows editors' BOMs do not break the parse.

### Served-Verbatim vs Summary vs Reference-Only

The delivery ladder: verbatim (full text), summary (your words about its content), reference-only (attribution + coordinates). The source's use policy and the passage's sensitivity choose the rung; the choice is recorded, not implicit.

### Frequently Confused Pairs

The distinctions that most often collapse in a builder's first pass — each pair is a category or authority boundary, not a stylistic nicety:

| Pair | The distinction | What happens when they blur |
|---|---|---|
| **hadith vs athar** | Prophetic report vs companion/successor report — different speakers, same chain discipline | A companion's word served in the Prophet's voice; the category tag is the only mechanical defense |
| **sunnah vs hadith** | The Prophet's path as a domain vs the transmitted reports that carry it | "Sunnah" used as a quality label ("this is more sunnah") instead of a content domain |
| **quran vs tafsir** | Revelation vs a named scholar's commentary on it | The failure-mode-4 blend: revelation and paraphrase served under one citation |
| **fiqh vs fatwa** | A school's codified jurisprudence vs one mufti's context-bound answer | A personal ruling generalized into public fiqh, or codified positions treated as disposable |
| **ijmaʿ vs ikhtilaf** | Recorded consensus vs recorded disagreement | A system asserting "scholars agree" when the corpus it holds shows they do not |
| **taqrid vs primary evidence** | A scholar's endorsement of a position vs the position itself | The endorsement detached from its endorser and served as independent proof |
| **shawahid vs primary hadith** | Supporting quotations inside a work vs the hadith collections themselves | A fiqh manual's quotation re-served freestanding, losing the primary chain and grading |
| **grade vs verdict** | Inherited metadata from a named grader vs the system's own judgment | GOV005's whole reason to exist: anonymous grades are system verdicts wearing a tradition's clothes |
| **isnad vs bibliography** | The chain of narration *within* the tradition's evaluative apparatus vs external citation metadata | Chains stripped as "preamble" while a volume/page is kept — the discipline inverted |

## Transliteration and Spelling Variants

The same term arrives spelled differently across editions, websites, and previous sessions' notes. The corpus normalizes *matching* (Arabic NLP 02's `searchable`) but preserves the display form; for builder vocabulary, the common variants:

| Canonical here | Also seen | Note |
|---|---|---|
| isnad | sanad, esnad, إسناد | Same term; this track's files use **isnad** |
| matn | maten, matn text, متن | The report text; avoid "content" in schemas |
| hadith | hadis, ḥadīth, حديث | Diacritized forms appear in scholarly sources |
| sunnah | sunna, سنة | No hard `a` in this track's prose |
| madhhab | madhab, مذهب | School of law |
| ikhtilaf | ikhtelaf, اختلاف | Scholarly disagreement |
| fatwa | fetva, فتوى | Context-bound answer |
| tafsir | tafseer, تفسير | Exegesis |
| quran | qur'an, koran, قرآن | This track uses **quran** in code and prose; quote sources' own spellings in citations |
| sahih | saheeh, صحيح | Grade label |
| daʿif | daif, ضعيف | Grade label |
| muʿallaq | muallaq | Suspended chain |

Rule for schemas: pick one canonical spelling per field value, record the variants only in a display-glossary layer, and never let two spellings of the same category value into the closed set — GOV004's check would treat `Hadith` and `hadith` as different tags, and the pool would quietly split.

## Worked Example: A Governed Hadith Passage

One GOOD-pack-shaped passage record, every governance field in place — the target shape any importer of hadith material should produce before the release gate (lecture §15) is even consulted:

```json
{
  "chunk_id": "good-p-matn",
  "source_id": "src-classical",
  "category": "hadith",
  "original": "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى ...",
  "searchable": "انما الامال بالنيات، وانما لكل امرى ما نوى ...",
  "grade": {
    "value": "sahih",
    "grader": "the source edition's own grading apparatus",
    "note": "inherited metadata; the system does not re-grade"
  },
  "isnad_present": false,
  "isnad_link": "good-p-isnad",
  "citation": {
    "work": "collection name (verified edition)",
    "locator": "hadith no. 1",
    "surah": null,
    "ayah": null,
    "volume": null,
    "page": null
  },
  "served_verbatim": true
}
```

Three things to notice: the matn chunk links to its isnad chunk rather than silently orphaning it; the grade carries its grader and the system's non-verb; the citation uses a locator a scholar would check rather than a bare work title. The source this passage joins must independently pass its own gates — licence decision (GOV001), checksum (GOV002), use policy permitting verbatim (GOV003) — before any of this is shippable.

## GOV Rule Cross-Reference

The ten rule codes, in one place, each pointing at where the lecture and this glossary define it:

| Rule | Severity | Glossary terms | Lecture section |
|---|---|---|---|
| GOV001 | critical | Licence Decision, Provenance Record | 9, 11 |
| GOV002 | warning | Checksum | 10 |
| GOV003 | critical | Use Policy, Redistribution Line, Reference-Only, Served-Verbatim | 11, 12 |
| GOV004 | critical | Category Tag | 2, 8 |
| GOV005 | critical | Grade, Grader, Grade Labels, Sahih/Hasan/Daʿif/Mawduʿ | 4 |
| GOV006 | critical | Isnad, Matn, Mursal/Muʿallaq/Maqtuʿ | 3, 5 |
| GOV007 | warning | Citation Coordinates, Shahid/Shawahid | 8, 9 |
| GOV008 | critical | Refusal Path, Handoff Target, Fatwa-Substance | 6, 7 |
| GOV009 | warning | Audit Log, Retention Limit | 14 |
| GOV010 | critical | Quran, Surah, Ayah | 2, 8 |

## Adjacent Tracks Boundary

Where this glossary stops, and who owns the rest:

- **Arabic NLP** (`projects/04-ai-engineering/arabic-nlp/`) — text normalization, tokenization, entity canonization, morphology; the two-text discipline's matching half lives in topic 02 (lines 184-187) and topic 09's display-versus-working-copy rule.
- **Athar** (`projects/04-ai-engineering/athar-lab/`) — the reference implementation of the contracts this glossary's schema mirrors: `SourceLocation` at `contracts.py:33-46`, `Passage` two-text discipline at `contracts.py:59-75`.
- **Security** (`projects/04-ai-engineering/security/`) — attack and defence mechanics, privacy pipelines, monitoring infrastructure; this glossary owns only the audit log's contents and retention schema, not the log pipeline itself.
- **Data engineering** (`projects/00-core-foundations/data-engineering/06-provenance-versioning/`) — machine lineage and dataset versioning generally; this glossary's provenance record adds the licence-and-category half.

## Summary

The quick-reference table is the map; the detailed definitions are the terrain. Three families run through Lecture 01: the category ledger (tags, grades with graders, isnad linkage, checkable coordinates), the provenance ledger (source records, licence decisions, checksums, per-source use policies), and the refusal/audit machinery that keeps the system inside its authority. Every definition above either points at a rule code in `exercises/01-islamic-domain-governance.py` or at a verified contract in this repository; where an adjacent track owns the mechanics — Arabic NLP's two-text discipline, the security track's monitoring pipelines — the definition says so and stops at the governance boundary.

## Using This Glossary in a Review

When reviewing any Islamic-domain corpus pipeline — Athar's, a new importer, a vendor's export — walk the glossary in this order:

1. **Start at the ten-rules list** above. Every review finding should eventually name one of those rules, or be filed as a design-rule issue (adjudication, smoothing, blending) the lecture's never-list covers.
2. **Check the two ledgers per passage**: category ledger (tag, grade-with-grader, isnad linkage, coordinates) and provenance ledger (source record, licence decision, checksum, use policy). A passage missing either half is not reviewable as "mostly done."
3. **Use the confused-pairs table** when a schema or a generated answer feels off: hadith-vs-athar and fiqh-vs-fatwa account for most first-pass category bugs.
4. **Check spelling canonicalization** against the variants table before trusting any tag-based filter — one importer writing `Hadith` and another `hadith` splits the pool invisibly.
5. **Run the exercise** (`exercises/01-islamic-domain-governance.py`) against the candidate's real manifest shape; the GOOD/BAD fixtures are the executable version of everything in this file.
