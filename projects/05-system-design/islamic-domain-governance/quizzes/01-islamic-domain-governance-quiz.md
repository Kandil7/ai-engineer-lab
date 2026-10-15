# Quiz 01: Islamic-Domain Literacy and Corpus Governance

## Topic Overview
This quiz covers the governance contract for Islamic-domain corpora: the nine textual categories and why conflating them is a category error with religious consequence; the isnad/matn structure with grades as inherited metadata; madhhab disagreement presented without adjudication; the designed refusal path for fatwa-substance questions; the provenance record with licence decisions, checksums, and per-source use policies; the redistribution line and derivative works; PII and living persons; and the audit log with a stated retention limit — all mapped to the exercise's GOV001-GOV010 rules.

---

## Questions

### Question 1
**A retrieval pool holds quranic text, hadith, tafsir passages, and fiqh rulings as undifferentiated chunks. What is the core failure this lecture names?**

- A) Index size grows slower than the corpus
- B) A category error with religious consequence: the system can answer from one category while citing another
- C) Vector similarity degrades on Arabic diacritics
- D) Embedding cost scales with the number of categories

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The categories differ in who speaks and with what authority — revelation, prophetic report, commentary, derived ruling. An undifferentiated pool lets the model blend a commentator's paraphrase into a quranic quote or present a school's fiqh as "the ruling." That is not a stylistic slip; it is a category error with religious consequence, and GOV004 catches it by requiring tags on every passage.
</details>

---

### Question 2
**What are the two parts of a hadith report, and what must survive chunking?**

- A) Title and body; the title must survive
- B) Arabic and translation; both must survive
- C) Isnad (chain of narration) and matn (report text); the linkage between them must survive even when they land in different chunks
- D) Grade and commentary; the grade must survive

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The isnad is who narrated from whom; the matn is the report itself. A fixed-size chunker may split them, but the matn chunk must carry an `isnad_link` to the chunk holding the chain — otherwise the system serves a report whose narrators it can no longer name. That orphaned matn is GOV006.
</details>

---

### Question 3
**A hadith passage in the corpus carries `"grade": "sahih"` with no grader field. What is wrong, and what does the exercise require?**

- A) Nothing; "sahih" is a complete grade
- B) The grade must be stored as an integer score instead
- C) The string is fine but should be uppercase
- D) The grade must be inherited metadata with grader attribution (value plus named grader); an anonymous verdict is the system adopting a ruling it has no authority to issue

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Grades are inherited from named graders who sometimes disagree with each other. The field shape is `{value, grader, note}` with an explicit "the system does not re-grade" note. A bare string hides who made the judgment, and GOV005 rejects hadith passages with no grade field at all — the design rule additionally rejects grades without graders.
</details>

---

### Question 4
**Which question is fatwa-substance and must trigger the refusal path?**

- A) "What does the Hanafi school say about X in book B?"
- B) "What are the positions on X recorded in these sources?"
- C) "Is X permissible for me in my situation?"
- D) "Which pages of the tafsir discuss surah 112?"

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Fatwa-substance means personal, context-bound, and actionable: a ruling for the asker's own case. Options A, B, and D are extractable — the corpus can answer with attributed positions and coordinates. C asks the system to issue a fatwa, which it is not authorized to do; the designed refusal states the boundary, cites what the corpus can, and hands off to a named trustworthy target (GOV008).
</details>

---

### Question 5
**What does a checksum of a retrieved source artifact buy you, and what does it not buy?**

- A) It proves the text's content is religiously correct
- B) It buys reproducibility — a research claim pinned to bytes that provably existed — but not licensing, correctness, or authenticity
- C) It buys the right to redistribute the source
- D) It replaces the licence decision

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Online corpora drift; a URL that resolved last year may serve different bytes today. The sha256 checksum pins the artifact so anyone can re-fetch, re-hash, and prove they worked from the same bytes (GOV002 requires one per source). It says nothing about what the licence permits, whether the text is accurate, or whether the tradition's grading is right.
</details>

---

### Question 6
**Which statement about the four Sunni schools is the correct engineering stance?**

- A) The system should determine which school is correct and present that
- B) The system should merge the schools into one synthetic position
- C) Positions are presented side by side with school attribution; the system explains, extracts, and compares but never adjudicates
- D) Only the most-populated school's positions need to be indexed

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Ikhtilaf — recorded scholarly disagreement — is a legitimate feature of the tradition. The system's job is attributed side-by-side presentation: school, scholar, coordinates. Choosing a winner, synthesizing a position, or presenting one school as "the ruling" is adjudication, which is outside the system's authority by design.
</details>

---

### Question 7
**The fatwa-archive source's terms of use state: "No bulk extraction; no republication of answers." The passage is in the corpus with a checksum. What delivery mode is compliant?**

- A) Verbatim serving, because the text is in the corpus
- B) Verbatim serving, because a citation is attached
- C) Reference-only: attribution and coordinates without the verbatim text — holding the bytes is not the right to republish them
- D) No delivery mode is compliant; the passage must be deleted

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The lecture's redistribution rule: you may hold a text without the right to republish it, and a RAG system that returns verbatim passages is publishing. The GOOD fixture keeps the fatwa-archive passage with provenance (checksum, licence decision) but sets `served_verbatim: false` — reference-only. GOV003 fires when a no-redistribution source's passage is served verbatim; deletion is not required, only compliant delivery.
</details>

---

### Question 8
**A tafsir passage discusses an ayah, and the generated answer writes: "Allah says: the Living, the Self-Subsisting, who does not need anything..." — blending revelation with the commentator's explanation under the quran's citation. Which discipline prevents this?**

- A) Higher embedding dimensions
- B) Category tags checked at retrieval, quran quoted verbatim with coordinates, commentary introduced as commentary with its own coordinates
- C) Lowering the temperature
- D) Removing tafsir from the index

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** This is failure mode 4: ayah blended with commentary. The fixes are mechanical, not stylistic: GOV004 requires categories, quranic text is quoted verbatim from the display copy with surah:ayah (GOV010 validates the coordinate), and tafsir is introduced with its own work/volume/page. Removing tafsir or lowering temperature treats symptoms; the category discipline treats the cause.
</details>

---

### Question 9
**What belongs in the governance audit log, and what is the retention stance?**

- A) Full user identity, conversation history, and derived profiles, retained forever for training
- B) Question, retrieved chunk ids, model version, refusal flag, and feedback — under a stated retention limit with automated purge
- C) Only aggregate metrics, per question
- D) The model's chain of thought, retained indefinitely

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The log is a governance receipt: enough to reconstruct what the system served and on what basis (chunk ids join back to category and provenance ledgers; model version pins the generator). GOV009 requires chunk ids and model version. An unbounded log of users' religious questions is a surveillance archive, so the GOOD fixture sets a 90-day retention with purge — defensible without being surveillant.
</details>

---

### Question 10
**A modern fatwa archive contains a personal question with health details asked by a real individual. What does the handling ladder prescribe?**

- A) Serve it verbatim like any other passage
- B) Strip the health details but keep serving the full answer verbatim
- C) Detect it at ingestion, classify it modern-personal, restrict delivery (reference-only at minimum), and never feed it into generation prompts as general fiqh reference
- D) Anonymize the mufti's name

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Historical scholarly biography is heritage; a living person's private case is not. The ladder: detect (fatwa-archive sources are flagged in their source record), classify (modern-personal), restrict delivery, and keep it out of generation prompts — otherwise the model paraphases someone's private case into a public answer. Stripping one detail or hiding the mufti's attribution misaddresses both the privacy and the attribution problems.
</details>

---

### Question 11
**What must a citation carry before it counts as scholar-checkable?**

- A) The book's title alone
- B) The title plus a URL
- C) Work plus volume/page, an equivalent locator (hadith number, entry id), or surah:ayah
- D) The author's kunya

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** "It is in Sunan al-X" is decoration; no one — scholar or skeptic — can find and verify the passage. GOV007 requires coordinates a scholar would actually check: volume and page, a locator like a hadith number, or surah:ayah for quranic text. The exercise's BAD tafsir chunk names its work and nothing else, and trips GOV007 exactly for that reason.
</details>

---

### Question 12
**Why is the category set closed (quran, hadith, athar, tafsir, fiqh, fatwa, qawaid, usul, shawahid, taqrid) rather than free-text "topics"?**

- A) Closed sets are faster to parse in JSON
- B) Open vocabulary would let the retrieval pool re-flatten authority distinctions the moment a new importer runs; the closed set is what GOV004 can actually check
- C) The categories are a historical artifact with no engineering use
- D) Free-text tags cannot be stored in Qdrant

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** GOV004 is only mechanically checkable against a closed set: every passage is tagged with one of the defined categories or it fails validation. An open "topics" vocabulary re-creates the undifferentiated pool with prettier labels — the importer decides what to call things, and the authority distinctions this lecture exists to protect disappear again.
</details>

---

### Question 13
**A chunk is tagged `hadith`, carries no isnad, and has `isnad_link: null` while a neighboring chunk holds only the chain. Which rule fires, what is the severity, and what is the fix?**

- A) GOV005, warning; add a grade
- B) GOV006, critical; set `isnad_link` on the matn chunk to the id of the chunk holding the chain
- C) GOV007, critical; add volume and page
- D) GOV010, warning; validate the surah:ayah

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The matn is orphaned from its isnad: no chain present, no link to the chunk that has one. GOV006 is critical because the report's chain of custody — who narrated what from whom — is exactly what the system can no longer name. The fix is linkage, not deletion: the GOOD fixture's `good-p-matn` carries `isnad_link: "good-p-isnad"` while staying a separate chunk.
</details>

---

### Question 14
**The source's terms forbid redistribution. A designer proposes: "We embed the passages for retrieval, never show them verbatim, and cite coordinates — so embedding is safe." What does the lecture's conservative stance say?**

- A) Embeddings are definitely not redistribution, by definition
- B) Embeddings are definitely redistribution, so the source must be deleted
- C) Treat embedding storage as potentially redistributive: record the licence decision per source, default to no-embed from no-redistribution sources until a licence reading says otherwise, and keep the passage reference-only
- D) Embeddings are safe if the vector database is hosted in the same country as the publisher

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Whether an embedding is a derivative work under a given licence is genuinely unsettled, which is precisely why the decision lives in the per-source record instead of a project-wide hope. The conservative default: no embed until the licence reading supports it; the passage may still be held with provenance and served reference-only. "Definitely safe" and "definitely forbidden" both skip the per-source decision the checklist requires.
</details>

---

### Question 15
**A release candidate has: category tags on all passages, grades with graders, linked isnad/matn, scholar-checkable coordinates, a configured refusal path, an audit log with 90-day retention — but three sources have no licence decision and two have no checksum. What is the correct release call?**

- A) Release; the category ledger is complete, which is what matters
- B) Release with a warning; licence decisions can be backfilled
- C) Block release: the checklist requires every source to have a licence decision and a checksum before any of its passages ship — GOV001 is critical and GOV002 is a reproducibility debt that must still be closed
- D) Release only the passages from sources that have checksums, and leave the rest undocumented

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The release checklist is a gate, not a dashboard. A missing licence decision (GOV001, critical) means the corpus cannot say what it may do with those bytes; a missing checksum (GOV002) means its citations from those sources are claims about artifacts no longer provably in hand. Both are per-source and both block until recorded — the whole point of deciding licences per source rather than per project.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Easy | | |
| 5 | Easy | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Hard | | |
| 14 | Hard | | |
| 15 | Hard | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 6 | C | 11 | C |
| 2 | C | 7 | C | 12 | B |
| 3 | D | 8 | B | 13 | B |
| 4 | C | 9 | B | 14 | C |
| 5 | B | 10 | C | 15 | C |

---

*Generated for AI Engineer Lab System Design Track - Quiz 01 of the Islamic-Domain Governance lane*
