---
id: islamic_domain_governance_track_v2
reported_by: builder
created_at: 2026-10-15T09:41:23.200Z
---

BUILT: projects/05-system-design/islamic-domain-governance/ (5 files, Format B per reliability lane).
FILES + FINAL COUNTS (verified): README.md 116 lines/9617 B; lectures/01-islamic-domain-governance-lecture.md 598/52049; lectures/01-islamic-domain-governance-glossary.md 436/34998; quizzes/01-islamic-domain-governance-quiz.md 346/16000 (15 Qs: 5 Easy/7 Med/3 Hard); exercises/01-islamic-domain-governance.py 890/33605.
VERIFICATION (all green, verbatim): py_compile exit 0; demo exit 0, BAD manifest = 10 findings (GOV001-010; 7 critical/3 warning), GOOD manifest = zero findings; CRLF byte-scan = 0 pairs across all 5 files, no BOM; tests/repo-structure/validate.ps1 Passed:75 Failed:0 Warnings:0; tests/knowledge/validate.ps1 Passed:11 Failed:0.
FIXES MADE TO OWN CODE (samples never weakened): (1) demo stdout crash on cp1252 consoles fixed via getattr(sys.stdout,'reconfigure',None) wrapper — same TextIO.reconfigure LSP noise pattern exists pre-existing in arabic-nlp 09/10, not ours; (2) typo passes during writing (Vermbatim->Verbatim in glossary, attributeion->attribution) caught and fixed before final verify.
PLAN-TARGET HONESTY: plan bands were lecture 600-750 lines/35-50 KB and glossary 450-650 lines. Final: lecture 598 lines (2 short), ~50.8 KiB (slightly over 50 KB guidance); glossary 436 (14 short). Four expansion rounds done (rule map, failure replay, licence-decision worked example, never-list, grade-labels table, confused-pairs, transliteration variants, severity rationale, modern-personal classification, ten-rules entry point, review-usage). Further expansion would pad, not add content. Treat as content-complete; user may request more if bands are hard gates.
SAFETY STANCE ENCODED: system explains/extracts/attributes, never rules; grades inherited+attributed; refusal = boundary+citations+handoff (GOV008); redistribution per-source (GOV003); never-list (8 items) in lecture §7.
NEXT (planned, not started): Lecture 02 = wiring GOV001-010 into Athar pipeline contracts.
