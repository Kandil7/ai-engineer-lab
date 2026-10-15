# Learning Path: Production AI Systems Engineering

**Last updated:** 2026-10-14

**Goal:** cover the layers that make an AI system trustworthy and able to grow: data
engineering, reliability, security, Arabic NLP depth, training fundamentals, inference
engineering, and product thinking. The aim is not expertise in everything. It is knowing
when to decide, when to collaborate, and when to defer complexity.

**Primary project:** `projects/04-ai-engineering/devmate`
**Application target:** Athar and Baligh (external repos)

This path is the second half of a pair. The first,
`docs/learning/paths/adr-driven-ai-systems.md`, covers architecture, design patterns as
decisions, and system design. This one covers the operating layer underneath them.

**Most of this path is already materialized in the repo.** The registry maps every
priority below to an existing directory. The work here is sequencing and application,
not new content authoring.

---

## Priority order

| # | Domain | Why now | Where it already lives |
| --- | --- | --- | --- |
| 1 | Evaluation harness | Protects every later decision | `projects/04-ai-engineering/ai-evaluation/` |
| 2 | Data contracts and idempotency | Foundation of Athar and Baligh | `projects/00-core-foundations/data-engineering/` |
| 3 | Arabic entity resolution | Improves RAG and GraphRAG | `projects/04-ai-engineering/arabic-nlp/` |
| 4 | Reliability patterns | Makes the system production-ready | `projects/00-core-foundations/python/10-system-design/` |
| 5 | Security and prompt injection | Required before any public launch | `projects/04-ai-engineering/security/` |
| 6 | Inference optimization | Improves cost and latency | `projects/04-ai-engineering/model-serving/` |
| 7 | Training fundamentals | Supports Baligh correctly | `projects/04-ai-engineering/fine-tuning/` |
| 8 | Product metrics | Turns a project into a product | `docs/learning/paths/adr-driven-ai-systems.md` |
| 9 | Advanced distributed systems | Only on real growth | `projects/05-system-design/` |
| 10 | Advanced Kubernetes | Not now | `projects/06-devops/` |

---

## Milestones

### 1. Data Engineering (Week 1-2)

The most important layer after RAG itself, because data quality determines the ceiling
of both Athar and Baligh before any model is involved.

- **Data modeling:** normalized versus denormalized, event sourcing, append-only logs,
  soft deletes
- **Data contracts:** schema versioning, backward and forward compatibility, validation
  at boundaries
- **Idempotency:** re-running a job neither duplicates nor corrupts data
- **Checkpointing:** resuming a pipeline from the last successful point
- **Deduplication:** content hash, canonical IDs, fuzzy matching
- **Data lineage:** where every chunk, claim, and citation came from
- **Batch versus streaming:** when batch suffices and when CDC or streaming is required
- **Data quality:** completeness, validity, consistency, freshness, uniqueness
- **Backfills:** processing a million old pages after the schema or chunker changes

**Study order, matching the existing material:**

1. `data-engineering/01-etl-fundamentals` and `09-elt-and-cdc`
2. `data-engineering/02-schemas-and-contracts`
3. `data-engineering/03-idempotency` and `04-checkpointing`
4. `data-engineering/11-data-quality` and `05-deduplication`
5. `data-engineering/06-provenance-versioning` and `14-data-versioning-lineage`
6. `data-engineering/08-batch-vs-streaming`, `07-parquet-object-storage`,
   `15-storage-and-databases`

**Application to Athar.** Every stage must be resumable and versioned:

```text
Shamela page -> raw snapshot -> parsed section -> normalized text
             -> chunk -> embedding -> graph node or edge
```

Changing the chunker must not blindly reprocess everything. Carry `chunker_version`,
`embedding_version`, and `graph_schema_version` on every row, so a schema change is a
targeted backfill rather than a full re-run.

**Artifact:** one Athar stage that survives a kill and resume with no duplicated rows and
no lost progress.

### 2. Reliability and Distributed Systems (Week 3-4)

Advanced Kubernetes is not needed now. Correct distributed-systems thinking is.

- **CAP trade-offs:** consistency versus availability under network partition
- **Idempotent APIs:** a repeated request produces no double effect
- **At-least-once versus exactly-once:** queues are usually at-least-once, so design
  consumers to be idempotent
- **Retries** with exponential backoff and jitter
- **Timeouts** on every external call
- **Circuit breaker:** stop hammering a failing vLLM or external API
- **Bulkheads:** separate resource pools so one failure does not take everything down
- **Backpressure:** do not accept ingestion faster than it can be processed
- **Dead-letter queues:** keep failed messages for investigation
- **Graceful shutdown:** stop workers without losing jobs
- **Rate limiting** by user, IP, endpoint, and model
- **Caching:** embedding cache, retrieval cache, prompt and response cache

**The operational rule.** Every external dependency carries all five:

```text
timeout + retry + circuit breaker + fallback + metrics
```

**Study order:** `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience`,
then `08-mlops`, then the caching and context-security topics in the RAG track.

**Artifact:** one DevMate dependency wrapped with the full five-tuple, with a test that
proves the breaker opens and the fallback engages.

### 3. Security and Privacy (Week 4)

Not deferrable, especially for a religious or knowledge system that may run publicly.

- **Authentication:** OAuth2 or OIDC, short-lived JWT, refresh tokens
- **Authorization:** RBAC or ABAC, not a binary logged-in check
- **API security:** rate limiting, correct CORS, input validation, request size limits
- **Secrets:** `.env` for development only, then Vault or a managed secret store in
  production
- **Prompt injection:** separate system instructions from user content and retrieved
  sources
- **Data privacy:** never send sensitive data to an external LLM provider without a
  stated policy
- **Audit logs:** who asked what, which sources were used, which model answered, who
  approved a publication
- **Supply chain:** pin dependencies, scan vulnerabilities, never run an untrusted model
  or dataset
- **Content safety:** for Islamic content especially, respect the boundaries of legal
  opinion, legitimate scholarly disagreement, and context

**The golden rule:**

```text
A source is not an instruction.
A user is not an instruction.
Only system policy is an instruction.
```

**Study order:** `projects/04-ai-engineering/security/lectures`, then the
`08-context-security` topic in the RAG track.

**Artifact:** one injection attempt against the DevMate prompt assembly path that the
system rejects, with a regression test.

### 4. Advanced Arabic NLP (Week 5-6)

The real competitive advantage. Ready-made embeddings are not enough.

- **Normalization layers:** always keep the original alongside a normalized copy
- **Diacritics:** when to strip, when to keep, and the effect on retrieval and TTS
- **Orthographic variants:** alef forms, alef-maqsura versus ya, ta marbuta versus ha,
  hamza forms
- **Morphology:** roots, patterns, derivation
- **Tokenization:** the enclitic attachment problem
- **Named entity recognition:** persons, books, countries, schools of thought, terms
- **Entity resolution:** the same name in different forms, and similar names that are
  genuinely different people
- **Arabic retrieval:** lexical, semantic, hybrid, and query expansion by root and synonym
- **Dialect versus MSA:** keep them separate in datasets and in evaluation
- **Transliteration:** foreign names, proper nouns, and technical terms
- **RTL UI:** not a cosmetic detail; it changes how citations and references render

**Study order:** `arabic-nlp/01-arabic-text-fundamentals` through
`07-arabic-mrr-evaluation`, in numeric order.

**Athar priority.** Start with **Entity Resolution v1**: authors and books first, then
narrators and terminology. This is the foundation of any serious GraphRAG or citation
graph.

**Artifact:** an entity resolution pass over the Athar author table that reports a
precision and recall number, not a vibe.

### 5. LLM Training Fundamentals (Week 7-8)

No need to become a research scientist. Need to understand what actually happens inside
training.

- Tokenization and vocabulary
- Attention and transformer blocks
- Context length and KV cache
- Loss functions and optimizer states
- Learning rate schedules and warmup
- Gradient accumulation
- Mixed precision: fp16 versus bf16
- LoRA, QLoRA, and full fine-tuning
- SFT versus DPO versus RLHF
- Dataset mixture and deduplication
- Catastrophic forgetting
- Overfitting versus underfitting
- Evaluation before and after training
- Model merging, and when it is actually useful

**The engineering rule.** Do not ask which LoRA configuration is best. Ask: what is the
specific failure in the baseline I am fixing, and what metric will prove the improvement?
That is the difference between someone who tries models and someone who builds a system
that learns.

**Study order:** `fine-tuning/01-supervised-fine-tuning`, `02-lora-qlora`,
`03-training-data`, `05-model-registry`, `06-rag-vs-fine-tuning`.

### 6. Inference Engineering (Week 8-9)

- **Serving:** vLLM, SGLang, TGI
- **Quantization:** AWQ, GPTQ, FP8, INT4, and when each is acceptable versus damaging
- **Batching:** continuous and dynamic batching
- **Prefix caching:** especially valuable for RAG and for personas
- **KV cache:** its effect on VRAM and concurrency
- **Speculative decoding:** when it genuinely helps
- **Structured output:** JSON schema and grammar-constrained decoding
- **Model routing:** small model for simple tasks, large model for analysis
- **Fallbacks:** local model, then cloud model, then degraded response
- **Cost, latency, and quality:** never optimize for latency alone

**Routing example:**

```text
Classify the user question      -> small local model or a classical classifier
Generate a cited religious answer -> stronger model + RAG + citations
Summarize a paragraph           -> mid-size model + caching
```

**Study order:** `model-serving/01-choosing-a-model`, `02-self-hosted-models`,
`03-inference-serving`.

### 7. Product Thinking (Week 9)

A senior engineer does not only ask how to build it. They ask whether it is worth
building, for whom, and what proves success.

- User personas and jobs to be done
- A real MVP, not a miniature of every idea
- A north-star metric
- Anti-metrics: what must not grow
- User feedback loops
- Feature flags
- A/B testing once volume allows it
- Cost per successful query
- Time to first value
- Trust metrics: citation coverage, correction rate, return usage

**Athar example.** Replace a vague goal such as "the best Islamic RAG" with:

```text
North-star metric:
  the share of questions that receive a useful, cited answer in under 10 seconds

Anti-metrics:
  hallucination rate
  citation mismatch rate
  unjustified refusal rate
  time-to-answer
```

**Artifact:** one north-star metric and three anti-metrics written into the Athar
roadmap, each with a way to measure it.

---

## Senior judgment

More important than any tool:

- **Locate the bottleneck:** is the problem in data, retrieval, prompt, model, or UX?
- **Measure before changing:** improve nothing that is not measured
- **Simplify first:** the simplest solution that meets the goal usually wins
- **Separate risk:** do not couple an easily reversed decision to a hard-to-reverse one
- **State uncertainty:** say "this is an assumption" or "this needs measurement"
- **Think about failure:** what if the model fails? the database? the source?
- **Think about cost:** GPU time, API cost, storage, human review
- **Think about time:** what can be deferred without harming the architecture?

---

## Weekly executive exercise: Evaluation Harness v0

Build an evaluation harness for Athar.

1. Collect 50 real Arabic questions.
2. For each question record the expected source, the question type (direct,
   multi-source, or unanswerable), and a short golden answer.
3. Run the current system.
4. Record: did it retrieve the correct source? is the citation correct? is the answer
   faithful? exactly where did it fail?
5. Produce a small report: retrieval hit rate, citation precision, hallucination rate,
   and the dominant failure patterns.

This exercise tells you precisely whether you need to improve chunking, embedding,
reranking, prompt, or model. It is what turns a builder into a production AI systems
engineer.

**Status note.** For DevMate this harness already exists and is the reference
implementation: `evaluations/rag/datasets/`, `evaluations/rag/reports/`, and
`src/devmate/eval/run_ragas.py`. The Athar version is the open item, and DevMate is the
template to copy.

---

## Definition of done

The project is done when it runs from a clean machine, every new source enters through an
adapter, every chunk and embedding carries a version, every answer has verifiable
citations, every change passes the eval suite, every important decision has an ADR, every
failure has a log, a metric, and an alert, and the system can be explained without
opening the code.

---

## Links

- Companion path: `docs/learning/paths/adr-driven-ai-systems.md`
- Data engineering: `projects/00-core-foundations/data-engineering/`
- Arabic NLP: `projects/04-ai-engineering/arabic-nlp/`
- Fine-tuning: `projects/04-ai-engineering/fine-tuning/`
- Model serving: `projects/04-ai-engineering/model-serving/`
- Security: `projects/04-ai-engineering/security/`
- Evaluation: `projects/04-ai-engineering/ai-evaluation/`
- Reliability: `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience`
- Reference harness: `evaluations/rag/`, `projects/04-ai-engineering/devmate/src/devmate/eval/`
- Registry mapping all of the above: `registries/knowledge-registry.yaml`
