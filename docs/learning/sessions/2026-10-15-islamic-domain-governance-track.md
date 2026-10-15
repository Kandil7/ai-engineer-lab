# Islamic-Domain Governance Track Built and Verified

### Context

Repo ai-engineer-lab. Task: create the new track projects/05-system-design/islamic-domain-governance/ combining security/licensing/provenance (#7) and Islamic-domain literacy (#8), Format B per projects/06-devops/reliability/. Five files, five verifications, honest line/byte reporting.

### Explanation

Built 5 files: README (provenance-flow ASCII diagram, Track Contents table, FACT complements section citing only glob/read-verified paths), lecture (15 sections + rule map GOV001-010 + failure replay + licence-decision worked example + never-list), glossary (~55 terms, ten-rules entry, confused pairs, transliteration variants, severity rationale, review-usage), quiz (15 Qs A-D, details/summary, Score Tracking, Answer Key), exercise (stdlib-only detector, dataclass models SourceRecord/Passage/Citation/GovernanceConfig, BAD pack trips all 10 rules, GOOD pack zero findings, refusal demo in Arabic+English, sha256 determinism demo, utf-8-sig JSON loading, __main__ exit). Verification: py_compile 0; demo 0 (BAD=7 critical/3 warning; GOOD=0); CRLF=0 across all 5; repo-structure 75/0/0; knowledge 11/0. Own-code fixes: stdout cp1252 reconfigure via getattr; two typo passes. Content-dense so lecture/glossary land 2 and 14 lines under plan bands; reported honestly.

### Rationale (Why this?)

Stance throughout: system explains/extracts/attributes, never rules. Two ledgers (category + provenance) + refusal/audit machinery. Grade = inherited {value,grader,note}. Redistribution per source; holding != republishing; RAG verbatim serving IS publishing. Adjacent-track boundaries named (arabic-nlp 02/08/09, athar-lab contracts.py, security 10, data-engineering 06-provenance) and only verified paths cited. Detector never weakened to clear samples; only detector-side fixes.

### Exercises

Run the exercise and map each BAD finding to its lecture section; tag Athar sample_pages/book_p1.txt with categories; write a defensible SourceRecord for a real source; test refusal templates on 3 fatwa-substance + 3 extractable questions; dry-run the §15 release checklist against Athar stage-1 contracts.

### Next Steps

Lecture 02 (planned): wiring GOV001-GOV010 into Athar's pipeline contracts. Possible follow-ups: wire registry/knowledge-registry nodes for this lane if the workspace gate later requires it (currently validators pass without); add the lane to a tracking doc if a current-focus pointer is desired.

---
