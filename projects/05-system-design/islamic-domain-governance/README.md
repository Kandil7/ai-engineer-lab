# Islamic-Domain Literacy and Corpus Governance

Building RAG and LLM systems over Islamic textual corpora — Quran, hadith, fiqh, fatwa, tafsir — is not "RAG with Arabic embeddings." The categories differ in who speaks and with what authority, and a pipeline that flattens them produces outputs with religious consequence: a commentator's paraphrase served as revelation, one school's position presented as the ruling, a private fatwa recycled as general fiqh. This track teaches the governance contract that keeps such a system inside its authority: a **category ledger** over the corpus's texts, a **provenance ledger** over its sources and licenses, and a **refusal-and-audit path** for the questions the system must not answer.

The stance throughout: the system explains, extracts, and attributes — it never rules. It does not adjudicate between schools, does not re-grade hadith, does not issue fatwas, and does not present any school as "the default." Where a user needs a ruling, the designed answer is a refusal with citations and a handoff, logged as such.

**Lane:** `projects/05-system-design/islamic-domain-governance/`

---

## Why This Track Exists

Two existing priorities meet here and neither covers the whole surface on its own:

- **Security, licensing, and provenance** — `projects/04-ai-engineering/security/` covers prompt injection, privacy, monitoring, and the attack/defence mechanics; `projects/00-core-foundations/data-engineering/06-provenance-versioning/` covers pipeline lineage. Neither owns the questions that arise when the *content itself* carries authority claims: grades, chains of narration, school attribution, or licenses that forbid the very republication a RAG system performs by default.
- **Islamic-domain literacy** — `projects/04-ai-engineering/athar-lab/` (the Islamic-knowledge RAG reference project) demonstrates a faithful two-text discipline and verifiable citation contracts in practice, but it is a system, not a curriculum. Arabic NLP topics 02, 08, and 09 teach normalization, canonization, and morphology; they stop at the text and do not teach the governance layer.

This track is the curriculum for that missing layer.

---

## Provenance Flow

Every answer this system serves is the end of a two-ledger pipeline. The flow below is what the release checklist in Lecture 01 §15 operationalizes, and each stage maps to a rule in `exercises/01-islamic-domain-governance.py` (GOV001–GOV010):

```
  Source bytes                     Ingestion                      Retrieval & delivery
┌──────────────────┐   ┌─────────────────────────────┐   ┌──────────────────────────────┐
│ Publisher's site │   │ Ingest (logged):            │   │ Query classified:            │
│ Archive / library│──▶│  • parse into passages      │──▶│  extractable  ▶ retrieve     │
│                  │   │  • two-text discipline      │   │  fatwa-substance ▶ REFUSE    │
│                  │   │  • set category tag (GOV004)│   │    • boundary statement      │
└──────────────────┘   │  • attach isnad link (GOV006)│  │    • cite what corpus can    │
         │             │  • validate coordinates      │   │    • handoff target (GOV008) │
         │             │    (GOV007, GOV010)          │   └──────────────┬───────────────┘
         ▼             └──────────────┬──────────────┘                  │
┌──────────────────┐                  │                                 ▼
│ sha256 checksum  │◀─────────────────┘               ┌──────────────────────────────┐
│ (GOV002)         │   SourceRecord per source:       │ Delivery                     │
│ Licence decision │   origin, terms, checksum,       │  • use_policy = redistrib-ok │
│ (GOV001, GOV003) │   decision, use policy           │      ▶ verbatim OK           │
│ Use policy set   │                                  │  • no-redistribution         │
│ per source       │                                  │      ▶ reference-only        │
└──────────────────┘                                  │      (GOV003 blocks)         │
                                                      │  • modern-personal           │
                                                      │      ▶ restricted ladder     │
                                                      └──────────────┬───────────────┘
                                                                     ▼
                                                      ┌──────────────────────────────┐
                                                      │ Audit log (GOV009):          │
                                                      │ question, chunk ids, model   │
                                                      │ version, refusal flag,       │
                                                      │ feedback, retention limit    │
                                                      └──────────────────────────────┘
```

The GOOD fixture at the bottom of the exercise file walks this exact path end-to-end with zero findings; the BAD fixture trips every rule in one pass.

---

## Track Contents

| # | File | What it is |
|---|------|------------|
| 00 | `README.md` | This file: scope, provenance flow, verification commands |
| 01 | `lectures/01-islamic-domain-governance-lecture.md` | Full lecture: category ledger, isnad/matn, refusal path, provenance, licensing, worked release scenario |
| 02 | `lectures/01-islamic-domain-governance-glossary.md` | ~50 terms with schema fragments and rule-code cross-references |
| 03 | `quizzes/01-islamic-domain-governance-quiz.md` | 15 questions (Easy 5 / Medium 7 / Hard 3), full answer key |
| 04 | `exercises/01-islamic-domain-governance.py` | Standalone rule engine + two fixture manifests; run it to see every rule fire and pass |

---

## How to Use This Track

1. **Read the lecture first.** Every rule code in the exercise, every table entry in the glossary, and every quiz explanation points back to a lecture section.
2. **Run the exercise before trusting your intuition.** It needs only the Python 3.11+ standard library:

   ```powershell
   cd projects\05-system-design\islamic-domain-governance
   python exercises\01-islamic-domain-governance.py
   # exit 0; BAD manifest trips all ten rules; GOOD manifest prints zero findings
   ```

3. **Take the quiz open-notes on the first pass, closed-notes on the second.** The Hard questions (13–15) are the ones that separate a compliant design from a hopeful one.
4. **Use the glossary as the shared vocabulary** for reviews of any Islamic-domain corpus pipeline — including Athar's — so that "category," "grade," and "licence decision" mean the same thing across the team.

---

## FACT: What This Track Covers and What It Complements

This track owns the **governance contract** for Islamic-domain corpora. Verified adjacent material (all paths confirmed present in this repository):

| Adjacent area | Where it lives | Relationship |
|---------------|----------------|--------------|
| Arabic text mechanics (normalization, two-text discipline, morphology, canonization) | `projects/04-ai-engineering/arabic-nlp/` (topics 02, 08, 09) | Complement; this track builds the governance layer on top |
| Reference Islamic-knowledge RAG system (contracts, provenance in practice) | `projects/04-ai-engineering/athar-lab/` (`contracts.py`, `sample_pages/`) | Complement; the exercise's dataclasses mirror its discipline |
| Attack/defence, privacy, monitoring pipelines | `projects/04-ai-engineering/security/` (10 lectures) | Complement; monitoring owns alert mechanics, this track owns the refusal-and-audit schema |
| Pipeline lineage and dataset versioning | `projects/00-core-foundations/data-engineering/06-provenance-versioning/` | Complement; that topic covers machine lineage, this track covers licence and category authority |

No source-index entry currently covers Islamic-studies literature or open-source licensing analysis; where the lecture cites such knowledge, it labels it as the tradition's own vocabulary and does not pretend to a bibliography this repository does not hold.

---

## Verification (mirrors this workspace's gates)

```powershell
# Exercise compiles and runs
python -m py_compile exercises\01-islamic-domain-governance.py
python exercises\01-islamic-domain-governance.py   # exit 0

# Structural validators (from repo root)
powershell -NoProfile -ExecutionPolicy Bypass -File tests\repo-structure\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests\knowledge\validate.ps1
```

All five files in this lane are LF-only UTF-8 without BOM, English prose (Arabic appears only inside content samples and terminology), and follow the Format B conventions of `projects/06-devops/reliability/`.
