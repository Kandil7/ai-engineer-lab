---
id: islamic_domain_governance_track
reported_by: builder
task_id: islamic-domain-governance-track
created_at: 2026-10-15T08:58:59.820Z
---

Building flagship track: projects/05-system-design/islamic-domain-governance/ (5 files: README, lecture, glossary, quiz, exercise). Combines user priorities #7 (licensing/provenance) and #8 (Islamic-domain literacy).

VERIFIED CONTEXT:
- Gold standard format B: projects/06-devops/reliability/ (600-line lecture, 558-line glossary, 15-Q quiz, 704-line stdlib exercise with REL001-008, marker-based line resolution '# BAD:timeout', PACK_BAD trips all/GOOD zero).
- athar-lab exists: contracts.py:33-46 SourceLocation (book_id/page invariants), :59-75 Passage two-text discipline (original verbatim + searchable normalized).
- arabic-nlp 08 (entity resolution/canonization), 09 (morphology; display-vs-working-copy rule also in 02 lecture lines 184-187).
- security track: 10 topics (prompt injection, content moderation, input validation, output filtering, data privacy, auth, API security, model security, infra security, monitoring) — covers NONE of licensing, provenance, Islamic textual categories.
- data-engineering 06-provenance-versioning exists (pipeline-level provenance complement).
- ADR practice: docs/decisions/0001-0009, registries/decision-log.yaml.
- Valid source anchors: #28 (Chip Huyen), #25 (Arize), #16 (HF course). No licensing source entry — say so honestly like domain-modeling did.

EXERCISE DESIGN (GOV001-010):
- GOV001 critical: source licence_decision missing. GOV002 warning: source checksum missing. GOV003 critical: source use_policy=no-redistribution + passage served_verbatim. GOV004 critical: passage category missing/not in {quran,hadith,athar,tafsir,fiqh,fatwa,qawaid,usul,shawahid,taqrid}. GOV005 critical: category=hadith with no grade dict. GOV006 critical: category in {hadith,athar} + not isnad_present + no isnad_link. GOV007 warning: citation lacks work+((volume+page)|locator|(surah+ayah)). GOV008 critical: refusal config missing template or handoff. GOV009 warning: audit log missing chunk ids or model version. GOV010 critical: quran ayah citation fails surah 1-114 / ayah>=1 / per-surah count table check.
- BAD: 10 findings (7 critical, 3 warning); GOOD: zero. Models: SourceRecord, Passage, Citation, GovernanceConfig, Finding, Analysis. Marker resolution like reliability. utf-8-sig JSON file arg. Arabic samples: hadith of Umar (isnad + inherited grade attributed to edition), ayah 2:255, tafsir passage citing an ayah, fatwa-shaped meta passage (reference-only delivery). Grades ALWAYS inherited metadata with grader attribution; never system verdict. Refusal template demonstrated, never a ruling.

SAFETY RULES (non-negotiable): teach builders not jurists; no fatwa; no adjudicating schools; grades inherited; one school never 'the ruling'; disagreement shown as disagreement.

CONSTRAINTS: LF only, UTF-8 no BOM, English prose (Arabic only in samples/terminology), 5 new files only, verification = py_compile, demo run (GOOD zero), CRLF byte scan (0), repo-structure validate (75/0/0), knowledge validate (11/0).
