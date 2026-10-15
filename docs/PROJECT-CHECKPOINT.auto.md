# Auto Checkpoint (pre-compaction snapshot)

- Time: 2026-10-15T09:21:19.773Z
- Session: ses_ec14079fdffeuNgx3FcuRJYAcA
- Project: D:\AI\Projects\ai-engineer-lab

## Recent user messages (tail)
- **user**: You are writing flagship educational content for `D:\AI\Projects\ai-engineer-lab` (public repo, English content). Topic: **Domain-Driven Design & Domain Modeling** — a declared gap with currently ZERO content (the folder `projects/05-system-design/` holds only three loose design docs). You WILL write 5 files.

## STEP 1 — Read the exact format to match (mandatory, read completely)
Format is **B** (topic folder with `lectures/`, `quizzes/`, `exercises/` subfolders plus a `README.md`). Gold standard — read all five:
- `projects/06-devops/reliability/README.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-lecture.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-glossary.md`
- `projects/06-devops/reliability/quizzes/01-reliability-patterns-quiz.md`
- `projects/06-devops/reliability/exercises/01-reliability-patterns.py`
(The reliability track was written this week and is the current depth bar — ~600 lecture lines / ~48 KB, 15-question quiz, stdlib-only exercise with BAD/GOOD packs and a zero-findings good pack.)

## STEP 2 — Read the real domain and the repo's decision machinery (verify every path first)
- `projects/04-ai-engineering/athar-lab/` — the Islamic-knowledge domain this track runs on as its worked example. Read what is actually there; do not invent its contents.
- `projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/` — topic 08 already taught entity resolution and the canonization model (`EntityId`, `MergeCandid
- **user**: You are writing flagship educational content for `D:\AI\Projects\ai-engineer-lab` (public repo, English content). Topic: **Software Craftsmanship — Refactoring & Testing Depth** — a declared gap with currently ZERO content (the folder `projects/05-system-design/` holds only three loose design docs). You WILL write 5 files.

## STEP 1 — Read the exact format to match (mandatory, read completely)
Format is **B** (topic folder with `lectures/`, `quizzes/`, `exercises/` subfolders plus a `README.md`). Gold standard — read all five:
- `projects/06-devops/reliability/README.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-lecture.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-glossary.md`
- `projects/06-devops/reliability/quizzes/01-reliability-patterns-quiz.md`
- `projects/06-devops/reliability/exercises/01-reliability-patterns.py`
(The reliability track is this week's depth bar — ~600 lecture lines / ~48 KB, 15-question quiz, stdlib-only exercise with BAD/GOOD packs and a zero-findings good pack. Match it.)

## STEP 2 — Read the repo's REAL testing practice (verify every path first)
This repo has a genuine, gating test suite — ground your examples in it rather than inventing a codebase:
- `projects/04-ai-engineer-lab` root `AGENTS.md` (the DevMate gate: ruff, mypy, pytest with coverage, the RAG eval gate)
- `projects/04-ai-engineering/devmate/` — read its `pyproject.toml`, and the real tests under `tests/` (unit and integration marker
- **user**: أهم حاجة ناقصة بعد الخطة التقنية هي **مهارات التشغيل والإنتاج**: data engineering، evaluation، observability، أمان، وإدارة الإصدارات. المشروع مش “تدريب موديل” فقط؛ هو نظام بيانات + تدريب + استرجاع + خدمة + مراقبة. خطط AI Engineering الحديثة تضع Evaluation وRAG وDataset Engineering وInference Optimization وObservability ضمن المهارات الأساسية. [dataskew](https://dataskew.io/roadmaps/ai-engineering/)
## أولويات التعلم

| الأولوية | المجال | لماذا تحتاجه |
|---|---|---|
| 1 | Data engineering | الشاملة والقرآن والحديث يحتاجون pipeline نظيف وقابل للتكرار |
| 2 | Transformer & training internals | عشان تفهم الـ loss والـ tokenizer والـ checkpoints بجد |
| 3 | Evaluation | بدون تقييم، لن تعرف هل التحسين تحسين فعلًا |
| 4 | RAG engineering | أساس أي منتج تراثي موثوق |
| 5 | LLMOps | تشغيل، مراقبة، إصدارات، وتكلفة |
| 6 | Arabic NLP | normalization، tokenization، تشكيل، ولهجات |
| 7 | Security & licensing | حماية النظام وحقوق النصوص |
| 8 | Islamic-domain literacy | لتقييم جودة المخرجات ومنع أخطاء منهجية |

## 1) Data Engineering

هذه أعلى أولوية. تعلّم:

- ETL/ELT: extract، transform، load.
- JSONL/Parquet وschema validation.
- DuckDB أو Polars لمعالجة ملايين الصفوف محليًا.
- Deduplication: exact hash وMinHash.
- Data versioning: DVC أو LakeFS.
- Data quality checks: Great Expectations أو checks مكتوبة يدويًا.
- Incremental processing: لا تعيد معالجة 19GB كل مرة.

الممارسات الجيدة في MLOps تشمل الأتمتة والمراقبة في كل مراحل بناء النظام: integration، testing
- **user**: عشان تبني المشروع **بإيدك سطر بسطر** وتطوّر تفكيرك الهندسي، محتاج تتعلم أربع طبقات معًا: **domain modeling، clean architecture، design patterns، وsystem design للـ LLM**. وأهم قرار: لا تكتب “سكربت تدريب”؛ اكتب **نظامًا** له domain layer وapplication layer وinfrastructure layer وinterfaces layer.
## 1) خريطة المعرفة الكاملة

| المجال | ما تحتاجه فعليًا | الأولوية |
|---|---|---|
| Python engineering | typing، dataclasses/Pydantic، protocols، context managers، async، packaging | عالية جدًا |
| Clean code | naming، functions صغيرة، error handling، tests، refactoring | عالية جدًا |
| SOLID | فصل المسؤوليات والاعتماد على abstractions | عالية جدًا |
| Design patterns | Repository، Strategy، Factory، Pipeline، Adapter، Observer | عالية جدًا |
| Clean/Hexagonal architecture | فصل domain عن infrastructure وAPI | عالية جدًا |
| Data engineering | ETL، schemas، dedup، versioning، quality gates | عالية جدًا |
| LLM internals | tokenizer، attention، training loop، checkpointing | عالية |
| RAG system design | chunking، retrieval، reranking، grounding، citations | عالية جدًا |
| LLMOps | experiment tracking، registry، monitoring، deployment | عالية |
| Testing | unit، integration، contract، evaluation tests | عالية جدًا |
| Security | auth، prompt injection، PII، licensing، audit | عالية |
| Domain knowledge | حدود الشرح والفتوى ومنهج عرض الخلاف | عالية |

## 2) المعمارية المقترحة: Clean / Hexagonal

استخدم **Hexagonal Architecture** أو Clean Architecture، لأنها تجعل م
- **user**: You are writing flagship educational content for `D:\AI\Projects\ai-engineer-lab` (public repo, English content). Topic: **Arabic NER & Entity Linking** — a declared gap with ZERO content. A previous attempt at this task failed and produced nothing; you are starting from scratch. You WILL write 4 files.

## STEP 1 — Read the exact format to match (mandatory, read completely)
Format is **A** (one numbered topic folder holding all 4 files). Template — read all four:
- `projects/04-ai-engineering/arabic-nlp/09-arabic-morphology-tokenization/09-arabic-morphology-tokenization-lecture.md`
- `.../09-arabic-morphology-tokenization-glossary.md`
- `.../09-arabic-morphology-tokenization-quiz.md`
- `.../09-arabic-morphology-tokenization.py`
(Topic 09 was written this week and is the current depth bar: ~683 lecture lines / 36 KB, ~1,105-line stdlib-only exercise with BAD/GOOD packs. Match or exceed it.)

Also read `projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/` (all four files) — 08 owns resolution/merging/canonization; YOUR topic owns detection and linking INTO that canon. They must complement, never overlap.

## STEP 2 — Read so you position correctly
- `projects/04-ai-engineering/arabic-nlp/01-...` through `09-...` — skim titles/overviews to avoid overlap
- `projects/04-ai-engineering/athar-lab/` — the Islamic-knowledge domain this serves; verify it exists before citing
- `registries/knowledge-registry.yaml` (the `arabic-nlp.*` nodes)
- `learning-sources/source-ind
- **user**: You are writing flagship educational content for `D:\AI\Projects\ai-engineer-lab` (public repo, English content). Topic: **Software Craftsmanship — Refactoring & Testing Depth** — a declared gap with ZERO content. A previous attempt at this task failed and produced nothing; you are starting from scratch. You WILL write 5 files.

## STEP 1 — Read the exact format to match (mandatory, read completely)
Format is **B** (topic folder with `lectures/`, `quizzes/`, `exercises/` subfolders plus a `README.md`). Gold standard — read all five:
- `projects/06-devops/reliability/README.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-lecture.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-glossary.md`
- `projects/06-devops/reliability/quizzes/01-reliability-patterns-quiz.md`
- `projects/06-devops/reliability/exercises/01-reliability-patterns.py`
(The reliability track is the current depth bar — ~600 lecture lines / ~48 KB, 15-question quiz, stdlib-only exercise with BAD/GOOD packs and a zero-findings good pack. Match it.)

## STEP 2 — Read the repo's REAL testing practice (verify every path first)
This repo has a genuine, gating test suite — ground your examples in it rather than inventing a codebase:
- `AGENTS.md` at the repo root (the DevMate gate: ruff, mypy, pytest with coverage, the RAG eval gate)
- `projects/04-ai-engineering/devmate/` — read its `pyproject.toml` and the real tests under `tests/` (unit and integration markers, the coverag
- **user**: You are writing flagship educational content for `D:\AI\Projects\ai-engineer-lab` (public repo, English content). Topic: **Clean / Hexagonal Architecture for LLM Systems** — a declared gap with ZERO content (the folder `projects/05-system-design/` holds three loose design docs, a `domain-modeling/` track, and nothing else on architecture layering). You WILL write 5 files.

This track is the direct companion to `projects/05-system-design/domain-modeling/`, which already taught ubiquitous language, bounded contexts, aggregates, invariants, and domain events. Your track teaches the LAYERING that lets those primitives live free of PyTorch, Qdrant, FastAPI, and Hugging Face. Read the domain-modeling lecture first so you build on its vocabulary rather than restating it.

## STEP 1 — Read the exact format to match (mandatory, read completely)
Format is **B** (topic folder with `lectures/`, `quizzes/`, `exercises/` subfolders plus a `README.md`). Gold standard — read all five:
- `projects/05-system-design/domain-modeling/README.md`
- `projects/05-system-design/domain-modeling/lectures/01-domain-modeling-lecture.md`
- `projects/05-system-design/domain-modeling/lectures/01-domain-modeling-glossary.md`
- `projects/05-system-design/domain-modeling/quizzes/01-domain-modeling-quiz.md`
- `projects/05-system-design/domain-modeling/exercises/01-domain-modeling.py`
(Also worth skimming: `projects/06-devops/reliability/lectures/01-reliability-patterns-lecture.md` for the section-order conventio
- **user**: You are writing flagship educational content for `D:\AI\Projects\ai-engineer-lab` (public repo, English content). Topic: **Islamic-Domain Literacy & Corpus Governance** — a declared gap with ZERO content. It is the user's stated priority #7 (security, licensing, provenance) and #8 (Islamic-domain literacy) combined into one governance track, because in this domain they are the same discipline: you cannot responsibly publish an Islamic corpus without knowing both what the text is and where it came from under what licence. You WILL write 5 files.

## STEP 1 — Read the exact format to match (mandatory, read completely)
Format is **B** (topic folder with `lectures/`, `quizzes/`, `exercises/` subfolders plus a `README.md`). Gold standard — read all five:
- `projects/06-devops/reliability/README.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-lecture.md`
- `projects/06-devops/reliability/lectures/01-reliability-patterns-glossary.md`
- `projects/06-devops/reliability/quizzes/01-reliability-patterns-quiz.md`
- `projects/06-devops/reliability/exercises/01-reliability-patterns.py`
(The reliability track is the current depth bar — ~600 lecture lines / ~48 KB, 15-question quiz, stdlib-only exercise with BAD/GOOD packs and a zero-findings good pack. Match it.)

## STEP 2 — Read the domain and the existing security track so you complement, not duplicate
- `projects/04-ai-engineering/athar-lab/` — verify it exists before citing; it is the Islamic-knowledge project thi
- **user**: https://arxiv.org/html/2604.17458v2
- **user**: add to chunking v2

> Regenerate a curated checkpoint with /checkpoint.