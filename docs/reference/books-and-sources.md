# Books and Sources

> Annotated, with reading order and usage guidance. Source: planning conversation 2026-07-31,
> decomposed 2026-08-02.

## The rule that matters most

> **Read the chapter after you've built the thing, not before.**

Reading first produces recognition; building first produces questions, and the chapter then
answers questions you actually have. This inverts the usual course-then-project order and is
the single highest-leverage change to how the material is consumed.

Corollary: **reaching for an additional source "to be sure you understood" is a procrastination
signal.** The list below is sufficient. Go back to the code.

---

## Books

### Tier 1 — read fully

**AI Engineering: Building Applications with Foundation Models** — Chip Huyen (2025)

The single most relevant book for this target role. Written for AI engineers rather than data
scientists: RAG, fine-tuning, evaluation, agents, deployment. If only one book is read, this
is it.

*Use:* one chapter per phase of the active track, after that phase's building is done.
Chapters 1–3 in week 1; the RAG chapter in weeks 2–3; evaluation and agents in weeks 5–7.

### Tier 2 — read the relevant parts

**The LLM Engineering Handbook** — Paul Iusztin & Maxime Labonne

Bridges ML theory and production systems. More hands-on than Huyen: RAG, vector databases,
evaluation, deployment, observability, optimization. *Use:* weeks 7–8, during hardening.

Companion repo (MIT, 5.4k stars): https://github.com/PacktPublishing/LLM-Engineers-Handbook —
packed and mined 2026-09-26 (155 files). Transferable patterns, verified against source:

- RAG retriever (`llm_engineering/application/rag/retriever.py`): self-query metadata filter
  → query expansion (1→3) → ThreadPool fan-out across collections → dedupe → cross-encoder
  rerank. The metadata-filter-then-search shape matches the DevMate fold-in.
- Reranker (`application/rag/reranking.py`): cross-encoder (query, chunk) pairs, sort desc,
  keep_top_k. Direct template for the weeks 2–3 reranking step.
- Chunking (`application/preprocessing/operations/chunking.py`): two-level split (paragraph
  then token-capped), per-type sizes (posts 250/25, articles 1000–2000 chars, repos 1500/100),
  md5 content ids, sizes recorded in chunk metadata. Evidence for the chunking ADR.
- Eval (`model/evaluation/evaluate.py`): vLLM batch generation → results dataset → GPT-4o-mini
  judge (accuracy + style rubric JSON) → threaded batch eval → aggregate columns. Judge pattern
  reference for the weeks 5–6 agent eval (ours scores faithfulness/relevance, not style).
- Fine-tuning (`model/finetuning/finetune.py`): SFT + DPO pipeline reference for week 11+,
  if postings demand it. Do not open before then.

**Designing Machine Learning Systems** — Chip Huyen (2022)

System-level thinking — data engineering, feature engineering, deployment, monitoring, A/B
testing. Closes the gap between "can build a model" and "can build a system." *Use:*
post-employment, or when system-design interviews start surfacing gaps.

### Tier 3 — reference

**Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow** — Aurélien Géron

The standard practical ML text; every chapter has working code. *Use:* reference during the
deferred ML sprint (week 11+), not cover-to-cover.

**Natural Language Processing with Transformers** — Tunstall, von Werra, Wolf

By the Hugging Face team. Deep, practical treatment of transformers and fine-tuning. *Use:*
when attention internals or fine-tuning become necessary.

**Designing Data-Intensive Applications** — Martin Kleppmann

Not AI-specific and essential anyway: databases, distributed systems, message queues. *Use:*
selected chapters, post-employment.

**Deep Learning** — Goodfellow, Bengio, Courville — free at deeplearningbook.org

The academic reference. Harder than everything above; the strongest mathematical foundation
available. *Use:* only if going deep into research-adjacent work.

**Mathematics for Machine Learning** — Deisenroth, Faisal, Ong — free at mml-book.github.io

Scoped to the mathematics actually used in ML. *Use:* to close a specific gap.

---

## Courses

### For the active track

| Course | Covers | Week |
| --- | --- | --- |
| DeepLearning.AI — ChatGPT Prompt Engineering for Developers | prompting fundamentals (~1h) | 1 |
| DeepLearning.AI — Building and Evaluating Advanced RAG | RAG + evaluation (~1.5h) | 2–3 |
| Activeloop RAG courses | chunking, retrieval optimization — deepest free RAG material | 2–3 |
| **Hugging Face Agents Course** | agents end-to-end; free certificate | 5–6 |
| Docker Curriculum (docker-curriculum.com) | containerization | 4 |

DeepLearning.AI short courses are the best tool available for closing one specific gap
quickly — each is 1–2 hours and single-topic.

### Documentation (primary sources — prefer these)

| Topic | Source |
| --- | --- |
| Claude API | docs.claude.com |
| FastAPI | fastapi.tiangolo.com/tutorial — sufficient on its own; don't look for alternatives |
| Qdrant | qdrant.tech/documentation |
| LangGraph | official docs |
| MCP | modelcontextprotocol.io |
| RAGAS | docs.ragas.io |
| Langfuse | langfuse.com/docs |
| Sentence Transformers | Hugging Face docs |
| pytest | official docs — fixtures and mocking sections only |
| Prompt engineering | promptingguide.ai |

### For the deferred ML sprint

Google ML Crash Course · fast.ai · Karpathy "Neural Networks: Zero to Hero" ·
Hugging Face NLP Course · *The Illustrated Transformer* (Alammar).

### Certificates — optional

**IBM AI Engineering Professional Certificate** (Coursera) — transformers, fine-tuning
(LoRA/QLoRA, RLHF), RAG, LangChain across 7 courses, ending in a QA bot. Theory-heavy;
~48 hours over 3 months.

**DataCamp Associate AI Engineer** — deliberately avoids advanced mathematics, focused on
building LLM applications.

Neither is necessary. Portfolio and demonstrated work outweigh certificates for the roles
being targeted, particularly at startups.

---

## Ongoing

arXiv (abstracts and results, not full papers) · Papers with Code · Hugging Face blog ·
engineering blogs of companies running LLMs at scale.

Skill to develop: extracting the useful insight from a paper without reading all of it.

---

## Reading order

```text
now         AI Engineering ch. 1–3           (week 1, after building)
weeks 2-3   AI Engineering — RAG chapter
weeks 5-7   AI Engineering — agents, evaluation
weeks 7-8   The LLM Engineering Handbook     (selected chapters)
week 11+    Hands-On ML                      (reference, during ML sprint)
post-job    Designing ML Systems
post-job    Designing Data-Intensive Applications (selected chapters)
```

---

## Related

- [`../roadmap/active-track-10-week.md`](../roadmap/active-track-10-week.md) — the fixed source
  list per week
- [`ml-fundamentals-map.md`](ml-fundamentals-map.md)
- [`../../learning-sources/`](../../learning-sources/) — where source notes are filed
- [`../learning/source-summaries/`](../learning/source-summaries/) — every source studied
  produces an entry here

*Extracted 2026-08-02 from `docs/plan/archive/Python-essentials-for-AI-engineers.md`*
