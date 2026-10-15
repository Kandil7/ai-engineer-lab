# Arabic NLP Topic 09 Written and Verified

### Context

Arabic-nlp track continuation in ai-engineer-lab. Wrote topic 09 (Morphology, Tokenization & Surface Variation) — 4 files in projects/04-ai-engineering/arabic-nlp/09-arabic-morphology-tokenization/ — matching the topic 08 depth bar (lecture ~683 lines/36 KB, glossary 601, quiz 15 Q, stdlib exercise with BAD/GOOD packs).

### Explanation

Exercise ships a display-preserving normalizer, conservative clitic segmenter (R1-R5 with length floors and guards for الله/وجه/علي/موسی/كتب), 3-tokenizer harness, and MOR001-MOR007 auditor. One real bug surfaced on first run: the segmenter's stem-length invariant crashed on the 2-char Levantine negator مش, because the invariant treated every non-clitic part as an extracted stem. Fixed by applying the >= 3-char rule only to split results (len(parts) > 1); unsplit short words are whole lexical items. This distinction is now taught in lecture section 3 and quiz Q13. Verified: py_compile exit 0; run exit 0 (BAD=7 findings one-per-rule, GOOD=0, fidelity 18/18); CRLF=0 on all files; repo-structure validator 75 passed; knowledge validator 11 passed. Known LSP false positive (sys.stdout.reconfigure under hasattr) matches topics 07/08; left in place.

### Rationale (Why this?)

Create-only rule respected: no existing file modified. Quiz uses correct relative ../08 link where 08's own footer has broken bare filenames. Lecture cites only measured harness numbers and repo-verified model names (no invented benchmarks). Topic 10 (NER/entity linking) is the declared next gap and was not touched.

### Next Steps

Topic 10 (Arabic NER & Entity Linking) is the other half of the declared gap. If writing it, reuse this topic's variety-decision string and StoredText contracts; do not overlap the morphology scope. The segmenter invariant lesson (unsplit short words vs extracted stems) generalizes to any future Arabic segmentation work.

---
