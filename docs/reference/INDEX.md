# Knowledge Index

> Generated from `registries/knowledge-registry.yaml` by `infra/scripts/build-knowledge-index.ps1`.
> Do not edit by hand. Run the script and commit the result. The knowledge gate fails CI when this file drifts.

**48 concepts across 11 domains.**

## python

### `python.production` - Production Python

- **Level:** core
- **Prerequisites:** none
- **Taught in:** `projects/00-core-foundations/python/02-advanced-python/35-unicode-and-arabic-text`
- **Sources:** `source-index#1`
- **Exercises:** `projects/00-core-foundations/python/02-advanced-python/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Bounded-memory batch import with typed errors naming the failing line.

### `python.testing` - Test strategy (unit to regression)

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/python/02-advanced-python/38-test-strategy-contract-regression`
- **Sources:** `source-index#1`
- **Exercises:** `projects/00-core-foundations/python/02-advanced-python/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A regression suite that reproduces a known failure and gates it.

## ai-engineering

### `llm.fundamentals` - LLM fundamentals

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `docs/curriculum/lectures/01-llm-fundamentals.md`
- **Sources:** `source-index#18`
- **Exercises:** `projects/04-ai-engineering/prompt-engineering`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Explain tokens, temperature, and context windows and defend each choice.

### `llm.streaming` - Streaming and structured outputs

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `docs/curriculum/lectures/01-llm-fundamentals.md`
- **Sources:** `source-index#18`
- **Exercises:** `projects/04-ai-engineering/devmate`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A streaming ask with typed retries and a validated structured response.

### `llm.prompt-engineering` - Prompt engineering

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/prompt-engineering/01-prompt-structure`
- **Sources:** `source-index#18`
- **Exercises:** `projects/04-ai-engineering/prompt-engineering`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Versioned templates in a running system, changed with a golden-set diff.

### `obs.tracing` - Observability and tracing

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `docs/curriculum/lectures/04-evaluation-observability.md`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/devmate`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Every LLM call appears as a span with tokens and latency.

### `obs.cost-tracking` - Cost tracking

- **Level:** core
- **Prerequisites:** `obs.tracing`
- **Taught in:** `docs/curriculum/lectures/04-evaluation-observability.md`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/devmate`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** State the dollar cost of one request from the ledger.

### `rag.embeddings` - Embeddings and model selection

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/embeddings/01-model-selection`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/embeddings`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Embed a real corpus and report a measured retrieval metric.

### `rag.chunking` - Chunking strategies

- **Level:** core
- **Prerequisites:** `rag.embeddings`
- **Taught in:** `projects/04-ai-engineering/rag-system/01-chunking-by-structure`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Three chunkers compared on a golden set with measured numbers.

### `rag.vector-store` - Vector store (Qdrant)

- **Level:** core
- **Prerequisites:** `rag.embeddings`
- **Taught in:** `projects/00-core-foundations/python/04-databases/vector-stores`
- **Sources:** `source-index#21`
- **Exercises:** `projects/00-core-foundations/python/04-databases/vector-stores`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Ingest and query the repo corpus at scale with metadata filters.

### `rag.hybrid-retrieval` - Hybrid retrieval (dense plus BM25)

- **Level:** advanced
- **Prerequisites:** `rag.vector-store`
- **Taught in:** `projects/04-ai-engineering/rag-system/02-hard-filters-retrieval`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A measured eval table showing hybrid beats dense-only.

### `rag.reranking` - Reranking

- **Level:** advanced
- **Prerequisites:** `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/rag-system/03-reranking`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Rerank top-k and show the metric delta against no rerank.

### `rag.citations-abstention` - Citations and abstention

- **Level:** advanced
- **Prerequisites:** `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/rag-system/05-abstention-citations`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Answers cite sources and abstain when evidence is missing.

### `eval.golden-datasets` - Golden datasets and annotation

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/01-gold-datasets-annotation`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A hand-graded golden set with expected sources per question.

### `eval.retrieval-metrics` - Retrieval metrics (recall, MRR)

- **Level:** core
- **Prerequisites:** `eval.golden-datasets`, `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/03-retrieval-evaluation`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A harness that prints recall@k and MRR against the golden set.

### `eval.faithfulness` - Faithfulness and citation precision

- **Level:** advanced
- **Prerequisites:** `eval.golden-datasets`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/02-faithfulness-citation-precision`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Score answers for grounding and report the failure cases.

### `eval.llm-as-judge` - LLM-as-judge

- **Level:** advanced
- **Prerequisites:** `eval.faithfulness`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/04-llm-as-judge`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A judge rubric calibrated against a hand-graded sample.

### `eval.eval-in-ci` - Evaluation in CI

- **Level:** advanced
- **Prerequisites:** `eval.retrieval-metrics`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/06-eval-in-ci`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** The eval gate fails CI when a metric regresses past a threshold.

### `agents.tool-use` - Tool use

- **Level:** core
- **Prerequisites:** `llm.streaming`
- **Taught in:** `docs/curriculum/lectures/03-agents.md`
- **Sources:** `source-index#23`
- **Exercises:** `projects/04-ai-engineering/agents/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One hand-rolled tool loop with a validated tool schema.

### `agents.react` - ReAct loop

- **Level:** advanced
- **Prerequisites:** `agents.tool-use`
- **Taught in:** `projects/04-ai-engineering/agents/lectures`
- **Sources:** `source-index#23`
- **Exercises:** `projects/04-ai-engineering/agents/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A step-capped loop with loop detection and a passing test.

### `agents.mcp` - Model Context Protocol

- **Level:** advanced
- **Prerequisites:** `agents.tool-use`
- **Taught in:** `docs/curriculum/lectures/03-agents.md`
- **Sources:** `source-index#23`
- **Exercises:** `projects/04-ai-engineering/agents/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** An MCP server reachable from a real MCP client.

### `prod.semantic-cache` - Semantic caching

- **Level:** advanced
- **Prerequisites:** `rag.hybrid-retrieval`, `databases.redis`
- **Taught in:** `projects/04-ai-engineering/rag-system/06-caching`
- **Sources:** `source-index#11`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A cache hit-rate metric from a semantic (not exact-match) cache.

### `prod.guardrails` - Guardrails and injection defence

- **Level:** advanced
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/rag-system/08-context-security`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/security`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Blocked injection attempts with evidence and a size limit.

## backend

### `backend.fastapi-service` - FastAPI service

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `docs/learning/paths/fastapi-ai-services.md`
- **Sources:** `source-index#5`
- **Exercises:** `projects/00-core-foundations/python/05-web-frameworks`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A documented API with health, streaming, and validation.

## databases

### `databases.sql-schema` - SQL schema and indexes

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/python/04-databases/sql-fundamentals`
- **Sources:** `source-index#10`
- **Exercises:** `projects/00-core-foundations/python/04-databases/sql-fundamentals`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A schema with justified indexes and a query plan that uses them.

### `databases.redis` - Redis cache and queues

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/python/04-databases/redis`
- **Sources:** `source-index#11`
- **Exercises:** `projects/00-core-foundations/python/04-databases/redis`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A cache or queue in the running system with a measured effect.

## devops

### `deploy.docker` - Docker and deployment

- **Level:** core
- **Prerequisites:** `backend.fastapi-service`
- **Taught in:** `projects/00-core-foundations/python/08-mlops`
- **Sources:** `source-index#8`
- **Exercises:** `projects/06-devops`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A multi-stage image serving the API from a public URL.

## system-design

### `system-design.contracts` - Component contracts

- **Level:** advanced
- **Prerequisites:** `backend.fastapi-service`
- **Taught in:** `projects/00-core-foundations/python/10-system-design/01-component-contracts`
- **Sources:** `source-index#26`
- **Exercises:** `projects/00-core-foundations/python/10-system-design/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A four-part contract with a compatibility and migration path.

### `system-design.failure-modes` - Failure modes and resilience

- **Level:** advanced
- **Prerequisites:** `system-design.contracts`
- **Taught in:** `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience`
- **Sources:** `source-index#26`
- **Exercises:** `projects/00-core-foundations/python/10-system-design/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Explain, with runbooks, what happens when a dependency dies.

## ml-foundations

### `ml.vectors-similarity` - Vectors and similarity

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/04-ai-engineering/applied-ml/01-vectors-and-similarity`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/applied-ml`
- **Used by:** `projects/04-ai-engineering/applied-ml`
- **Evidence:** Compute similarity by hand and explain why the metric fits the data.

### `ml.evaluation-metrics` - Precision, recall, confusion

- **Level:** core
- **Prerequisites:** `ml.vectors-similarity`
- **Taught in:** `projects/04-ai-engineering/applied-ml/03-precision-recall-confusion`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/applied-ml`
- **Used by:** `projects/04-ai-engineering/applied-ml`
- **Evidence:** Pick the right metric for an imbalanced task and defend it.

### `ml.baselines-error-analysis` - Rules vs models, error analysis

- **Level:** advanced
- **Prerequisites:** `ml.evaluation-metrics`
- **Taught in:** `projects/04-ai-engineering/applied-ml/04-rules-vs-models-error-analysis`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/applied-ml`
- **Used by:** `projects/04-ai-engineering/applied-ml`
- **Evidence:** A rules baseline and a model compared with a real error analysis.

## fine-tuning

### `fine-tuning.sft` - Supervised fine-tuning

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/01-supervised-fine-tuning`
- **Sources:** `source-index#20`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** One SFT run with a held-out loss and a sample output.

### `fine-tuning.lora-qlora` - LoRA and QLoRA

- **Level:** advanced
- **Prerequisites:** `fine-tuning.sft`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/02-lora-qlora`
- **Sources:** `source-index#20`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A 4-bit QLoRA run inside the 16 GB budget with VRAM measured.

### `fine-tuning.training-data` - Training data preparation

- **Level:** core
- **Prerequisites:** `fine-tuning.sft`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/03-training-data`
- **Sources:** `source-index#20`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A deduplicated, format-validated dataset with a data card.

### `fine-tuning.model-registry` - Model registry and versioning

- **Level:** advanced
- **Prerequisites:** `fine-tuning.sft`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/05-model-registry`
- **Sources:** `source-index#20`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A versioned checkpoint registry with eval metadata per version.

### `fine-tuning.rag-vs-ft` - RAG vs fine-tuning

- **Level:** advanced
- **Prerequisites:** `fine-tuning.sft`, `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/06-rag-vs-fine-tuning`
- **Sources:** `source-index#20`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A written decision on when to retrieve and when to fine-tune.

## arabic-nlp

### `arabic-nlp.text-fundamentals` - Arabic text fundamentals

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/01-arabic-text-fundamentals`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** Explain harakat, presentation forms, and digit folding on real text.

### `arabic-nlp.normalization` - Arabic normalization and tokenization

- **Level:** core
- **Prerequisites:** `arabic-nlp.text-fundamentals`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/02-arabic-normalization-tokenization`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** A normalizer that is idempotent and proven on a golden text set.

### `arabic-nlp.lexical-retrieval` - Arabic lexical retrieval

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.normalization`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/03-arabic-lexical-retrieval`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** A BM25 baseline on Arabic text with a measured recall.

### `arabic-nlp.embeddings` - Arabic embeddings

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.normalization`, `rag.embeddings`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/04-arabic-embeddings`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** An Arabic embedding model chosen with a measured retrieval delta.

### `arabic-nlp.hybrid-search` - Arabic hybrid search

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.embeddings`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/05-arabic-hybrid-search`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** A dense plus lexical fusion that beats each alone on Arabic.

### `arabic-nlp.ann-search` - Arabic ANN search

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.embeddings`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/06-arabic-ann-search`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** An ANN index with a recall vs latency tradeoff measured.

### `arabic-nlp.mrr-evaluation` - Arabic retrieval evaluation

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.hybrid-search`, `eval.retrieval-metrics`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/07-arabic-mrr-evaluation`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** An MRR harness on an Arabic golden set with reported numbers.

## model-serving

### `serving.model-selection` - Choosing a model

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/model-serving/01-choosing-a-model`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/model-serving`
- **Used by:** `projects/04-ai-engineering/model-serving`
- **Evidence:** A model choice defended by size, license, and task fit.

### `serving.self-hosted` - Self-hosted models

- **Level:** advanced
- **Prerequisites:** `serving.model-selection`
- **Taught in:** `projects/04-ai-engineering/model-serving/02-self-hosted-models`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/model-serving`
- **Used by:** `projects/04-ai-engineering/model-serving`
- **Evidence:** A quantized model served locally within the 16 GB VRAM budget.

### `serving.inference` - Inference serving

- **Level:** advanced
- **Prerequisites:** `serving.self-hosted`
- **Taught in:** `projects/04-ai-engineering/model-serving/03-inference-serving`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/model-serving`
- **Used by:** `projects/04-ai-engineering/model-serving`
- **Evidence:** A served endpoint with measured throughput and latency.

## security

### `security.llm-security` - LLM application security

- **Level:** advanced
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/security/lectures`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/security`, `projects/04-ai-engineering/devmate`
- **Evidence:** A blocked prompt-injection attempt from the OWASP LLM top-10.
