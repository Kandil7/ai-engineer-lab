# Knowledge Index

> Generated from `registries/knowledge-registry.yaml` by `infra/scripts/build-knowledge-index.ps1`.
> Do not edit by hand. Run the script and commit the result. The knowledge gate fails CI when this file drifts.

**78 concepts across 15 domains.**

## python

### `python.production` - Production Python

- **Level:** core
- **Prerequisites:** none
- **Taught in:** `projects/00-core-foundations/python/02-advanced-python/35-unicode-and-arabic-text`
- **Sources:** `source-index#1`
- **Exercises:** `projects/00-core-foundations/python/02-advanced-python/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Bounded-memory batch import with typed errors naming the failing line.
- **Target:** 7/10
- **Evidence required:** `test`, `pr`
- **Verified:** 2026-10-10, review every 0 days

### `python.testing` - Test strategy (unit to regression)

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/python/02-advanced-python/38-test-strategy-contract-regression`
- **Sources:** `source-index#1`
- **Exercises:** `projects/00-core-foundations/python/02-advanced-python/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A regression suite that reproduces a known failure and gates it.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

## ai-engineering

### `llm.fundamentals` - LLM fundamentals

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `docs/curriculum/lectures/01-llm-fundamentals.md`
- **Sources:** `source-index#18`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/prompt-engineering`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Explain tokens, temperature, and context windows and defend each choice.
- **Target:** 7/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `llm.streaming` - Streaming and structured outputs

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `docs/curriculum/lectures/01-llm-fundamentals.md`
- **Sources:** `source-index#18`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/devmate`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A streaming ask with typed retries and a validated structured response.
- **Target:** 7/10
- **Evidence required:** `test`, `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `llm.prompt-engineering` - Prompt engineering

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/prompt-engineering/01-prompt-structure`
- **Sources:** `source-index#18`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/prompt-engineering`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Versioned templates in a running system, changed with a golden-set diff.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `obs.tracing` - Observability and tracing

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `docs/curriculum/lectures/04-evaluation-observability.md`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/devmate`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Every LLM call appears as a span with tokens and latency.
- **Target:** 6/10
- **Evidence required:** `test`, `deployment`
- **Verified:** 2026-10-10, review every 0 days

### `obs.cost-tracking` - Cost tracking

- **Level:** core
- **Prerequisites:** `obs.tracing`
- **Taught in:** `docs/curriculum/lectures/04-evaluation-observability.md`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/devmate`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** State the dollar cost of one request from the ledger.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `rag.embeddings` - Embeddings and model selection

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/embeddings/01-model-selection`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/embeddings`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Embed a real corpus and report a measured retrieval metric.
- **Target:** 6/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 90 days

### `rag.chunking` - Chunking strategies

- **Level:** core
- **Prerequisites:** `rag.embeddings`
- **Taught in:** `projects/04-ai-engineering/rag-system/01-chunking-by-structure`
- **Sources:** `source-index#21`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Three chunkers compared on a golden set with measured numbers.
- **Target:** 7/10
- **Evidence required:** `eval_report`, `adr`
- **Verified:** 2026-10-10, review every 0 days

### `rag.vector-store` - Vector store (Qdrant)

- **Level:** core
- **Prerequisites:** `rag.embeddings`
- **Taught in:** `projects/00-core-foundations/python/04-databases/vector-stores`, `projects/03-databases/qdrant-rag`
- **Sources:** `source-index#21`
- **Exercises:** `projects/00-core-foundations/python/04-databases/vector-stores`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Ingest and query the repo corpus at scale with metadata filters.
- **Target:** 7/10
- **Evidence required:** `eval_report`, `test`
- **Verified:** 2026-10-10, review every 90 days

### `rag.hybrid-retrieval` - Hybrid retrieval (dense plus BM25)

- **Level:** advanced
- **Prerequisites:** `rag.vector-store`
- **Taught in:** `projects/04-ai-engineering/rag-system/02-hard-filters-retrieval`
- **Sources:** `source-index#21`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A measured eval table showing hybrid beats dense-only.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `rag.reranking` - Reranking

- **Level:** advanced
- **Prerequisites:** `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/rag-system/03-reranking`
- **Sources:** `source-index#21`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Rerank top-k and show the metric delta against no rerank.
- **Target:** 7/10
- **Evidence required:** `eval_report`, `adr`
- **Verified:** 2026-10-10, review every 0 days

### `rag.citations-abstention` - Citations and abstention

- **Level:** advanced
- **Prerequisites:** `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/rag-system/05-abstention-citations`
- **Sources:** `source-index#21`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Answers cite sources and abstain when evidence is missing.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `eval.golden-datasets` - Golden datasets and annotation

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/01-gold-datasets-annotation`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A hand-graded golden set with expected sources per question.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `eval.retrieval-metrics` - Retrieval metrics (recall, MRR)

- **Level:** core
- **Prerequisites:** `eval.golden-datasets`, `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/03-retrieval-evaluation`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A harness that prints recall@k and MRR against the golden set.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `eval.faithfulness` - Faithfulness and citation precision

- **Level:** advanced
- **Prerequisites:** `eval.golden-datasets`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/02-faithfulness-citation-precision`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Score answers for grounding and report the failure cases.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `eval.llm-as-judge` - LLM-as-judge

- **Level:** advanced
- **Prerequisites:** `eval.faithfulness`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/04-llm-as-judge`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A judge rubric calibrated against a hand-graded sample.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `eval.eval-in-ci` - Evaluation in CI

- **Level:** advanced
- **Prerequisites:** `eval.retrieval-metrics`
- **Taught in:** `projects/04-ai-engineering/ai-evaluation/06-eval-in-ci`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/ai-evaluation`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** The eval gate fails CI when a metric regresses past a threshold.
- **Target:** 7/10
- **Evidence required:** `test`, `deployment`
- **Verified:** 2026-10-10, review every 0 days

### `agents.tool-use` - Tool use

- **Level:** core
- **Prerequisites:** `llm.streaming`
- **Taught in:** `docs/curriculum/lectures/03-agents.md`
- **Sources:** `source-index#23`
- **Exercises:** `projects/04-ai-engineering/agents/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One hand-rolled tool loop with a validated tool schema.
- **Target:** 7/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `agents.react` - ReAct loop

- **Level:** advanced
- **Prerequisites:** `agents.tool-use`
- **Taught in:** `projects/04-ai-engineering/agents/lectures`
- **Sources:** `source-index#23`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/agents/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A step-capped loop with loop detection and a passing test.
- **Target:** 7/10
- **Evidence required:** `test`, `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `agents.mcp` - Model Context Protocol

- **Level:** advanced
- **Prerequisites:** `agents.tool-use`
- **Taught in:** `docs/curriculum/lectures/03-agents.md`
- **Sources:** `source-index#23`
- **Exercises:** `projects/04-ai-engineering/agents/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** An MCP server reachable from a real MCP client.
- **Target:** 6/10
- **Evidence required:** `test`, `deployment`
- **Verified:** 2026-10-10, review every 0 days

### `agents.multi-agent` - Multi-agent orchestration

- **Level:** advanced
- **Prerequisites:** `agents.react`
- **Taught in:** `projects/04-ai-engineering/ai-automation/lectures/08-multi-agent-lecture.md`
- **Sources:** `source-index#22`
- **Exercises:** `projects/04-ai-engineering/ai-automation/quizzes/08-multi-agent-quiz.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Two agents with distinct roles and a handoff whose failure mode is stated.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `prod.semantic-cache` - Semantic caching

- **Level:** advanced
- **Prerequisites:** `rag.hybrid-retrieval`, `databases.redis`
- **Taught in:** `projects/04-ai-engineering/rag-system/06-caching`
- **Sources:** `source-index#11`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/rag-system`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A cache hit-rate metric from a semantic (not exact-match) cache.
- **Target:** 5/10
- **Evidence required:** `test`, `benchmark`
- **Verified:** 2026-10-10, review every 0 days

### `prod.guardrails` - Guardrails and injection defence

- **Level:** advanced
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/rag-system/08-context-security`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Blocked injection attempts with evidence and a size limit.
- **Target:** 6/10
- **Evidence required:** `test`, `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `prod.ai-safety` - AI safety and harm review

- **Level:** advanced
- **Prerequisites:** `prod.guardrails`
- **Taught in:** `projects/04-ai-engineering/ai-automation/lectures/09-ai-safety-lecture.md`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/ai-automation/quizzes/09-ai-safety-quiz.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A harm taxonomy for the product with one mitigation traced to a code change.
- **Target:** 6/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-14, review every 0 days

## backend

### `backend.fastapi-service` - FastAPI service

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `docs/learning/paths/fastapi-ai-services.md`
- **Sources:** `source-index#5`
- **Exercises:** `projects/00-core-foundations/python/05-web-frameworks`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A documented API with health, streaming, and validation.
- **Target:** 7/10
- **Evidence required:** `test`, `deployment`
- **Verified:** 2026-10-10, review every 0 days

## databases

### `databases.sql-schema` - SQL schema and indexes

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/python/04-databases/sql-fundamentals`, `projects/03-databases/postgres-design`
- **Sources:** `source-index#10`
- **Exercises:** `projects/00-core-foundations/python/04-databases/sql-fundamentals`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A schema with justified indexes and a query plan that uses them.
- **Target:** 6/10
- **Evidence required:** `test`, `adr`
- **Verified:** 2026-10-10, review every 0 days

### `databases.redis` - Redis cache and queues

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/python/04-databases/redis`, `projects/03-databases/redis-cache`
- **Sources:** `source-index#11`
- **Exercises:** `projects/00-core-foundations/python/04-databases/redis`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A cache or queue in the running system with a measured effect.
- **Target:** 5/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

## data-engineering

### `data.etl-pipelines` - ETL/ELT and ingestion pipelines

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/00-core-foundations/data-engineering/01-etl-fundamentals`, `projects/00-core-foundations/data-engineering/09-elt-and-cdc`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering/01-etl-fundamentals`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** An ingest job that runs end to end and records what it loaded.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `data.contracts` - Schemas and data contracts

- **Level:** core
- **Prerequisites:** `data.etl-pipelines`
- **Taught in:** `projects/00-core-foundations/data-engineering/02-schemas-and-contracts`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering/02-schemas-and-contracts`
- **Used by:** `projects/00-core-foundations/data-engineering`
- **Evidence:** A producer and a consumer agreeing on a schema that fails loudly on drift.
- **Target:** 6/10
- **Evidence required:** `test`, `adr`
- **Verified:** 2026-10-14, review every 0 days

### `data.reliability` - Idempotency and checkpointing

- **Level:** core
- **Prerequisites:** `data.etl-pipelines`
- **Taught in:** `projects/00-core-foundations/data-engineering/03-idempotency`, `projects/00-core-foundations/data-engineering/04-checkpointing`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering/03-idempotency`
- **Used by:** `projects/00-core-foundations/data-engineering`
- **Evidence:** A job killed mid-run and retried without duplicating or losing rows.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `data.quality` - Data quality and deduplication

- **Level:** core
- **Prerequisites:** `data.contracts`
- **Taught in:** `projects/00-core-foundations/data-engineering/11-data-quality`, `projects/00-core-foundations/data-engineering/05-deduplication`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering/11-data-quality`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A quality check that quarantines bad rows instead of silently passing them.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `data.lineage` - Provenance, versioning and lineage

- **Level:** advanced
- **Prerequisites:** `data.reliability`
- **Taught in:** `projects/00-core-foundations/data-engineering/06-provenance-versioning`, `projects/00-core-foundations/data-engineering/14-data-versioning-lineage`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering/14-data-versioning-lineage`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Trace a field in the output back to the exact source file and transform.
- **Target:** 6/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-14, review every 0 days

### `data.streaming-storage` - Batch vs streaming and storage layout

- **Level:** advanced
- **Prerequisites:** `data.etl-pipelines`
- **Taught in:** `projects/00-core-foundations/data-engineering/08-batch-vs-streaming`, `projects/00-core-foundations/data-engineering/07-parquet-object-storage`, `projects/00-core-foundations/data-engineering/15-storage-and-databases`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering/08-batch-vs-streaming`
- **Used by:** `projects/00-core-foundations/data-engineering`
- **Evidence:** Defend a batch or streaming choice and a storage format against the workload.
- **Target:** 6/10
- **Evidence required:** `adr`, `benchmark`
- **Verified:** 2026-10-14, review every 0 days

### `data.lakehouse` - Lakehouse table layout

- **Level:** advanced
- **Prerequisites:** `data.streaming-storage`
- **Taught in:** `projects/00-core-foundations/data-engineering/10-lakehouse`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering`
- **Used by:** `projects/00-core-foundations/data-engineering`
- **Evidence:** A bronze, silver, gold layout defended by who reads each layer and how often.
- **Target:** 5/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-14, review every 0 days

### `data.feature-stores` - Feature stores and feature pipelines

- **Level:** advanced
- **Prerequisites:** `data.lakehouse`
- **Taught in:** `projects/00-core-foundations/data-engineering/12-feature-stores`, `projects/00-core-foundations/data-engineering/13-feature-pipelines`
- **Sources:** `source-index#29`
- **Exercises:** `projects/00-core-foundations/data-engineering`
- **Used by:** `projects/00-core-foundations/data-engineering`
- **Evidence:** One feature computed both offline and online with the same definition and no drift.
- **Target:** 5/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

## devops

### `deploy.docker` - Docker containerization for AI services

- **Level:** core
- **Prerequisites:** `backend.fastapi-service`
- **Taught in:** `projects/06-devops/docker/lectures/01-containerization-lecture.md`, `projects/00-core-foundations/python/08-mlops`
- **Sources:** `source-index#8`, `source-index#9`
- **Exercises:** `projects/06-devops/docker/exercises/01-containerization.py`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A multi-stage image that passes a Dockerfile analyzer with zero findings.
- **Target:** 6/10
- **Evidence required:** `deployment`
- **Verified:** 2026-10-14, review every 0 days

### `deploy.ci-cd` - CI/CD pipelines and quality gates

- **Level:** core
- **Prerequisites:** `deploy.docker`
- **Taught in:** `projects/06-devops/ci-cd/lectures/01-ci-cd-pipelines-lecture.md`
- **Sources:** `source-index#8`
- **Exercises:** `projects/06-devops/ci-cd/exercises/01-ci-cd-pipelines.py`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A workflow analyzer that flags unpinned actions and missing timeouts on the repo's own ci.yml.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `deploy.strategies` - Deployment strategies and Kubernetes fundamentals

- **Level:** core
- **Prerequisites:** `deploy.docker`
- **Taught in:** `projects/06-devops/deployment/lectures/01-deployment-strategies-lecture.md`
- **Sources:** `source-index#8`
- **Exercises:** `projects/06-devops/deployment/exercises/01-deployment-strategies.py`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A manifest analyzer that rejects mutable tags, missing probes, and unset resource limits.
- **Target:** 6/10
- **Evidence required:** `deployment`
- **Verified:** 2026-10-14, review every 0 days

### `deploy.llmops` - LLMOps lifecycle for production LLM systems

- **Level:** advanced
- **Prerequisites:** `deploy.docker`, `llm.fundamentals`
- **Taught in:** `projects/06-devops/llmops/lectures/01-llmops-lifecycle-lecture.md`
- **Sources:** `source-index#28`
- **Exercises:** `projects/06-devops/llmops/exercises/01-llmops-lifecycle.py`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A prompt-registry auditor plus per-query cost budget that gate a model change.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-14, review every 0 days

## system-design

### `system-design.contracts` - Component contracts

- **Level:** advanced
- **Prerequisites:** `backend.fastapi-service`
- **Taught in:** `projects/00-core-foundations/python/10-system-design/01-component-contracts`
- **Sources:** `source-index#26`
- **Exercises:** `projects/00-core-foundations/python/10-system-design/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A four-part contract with a compatibility and migration path.
- **Target:** 6/10
- **Evidence required:** `adr`, `test`
- **Verified:** 2026-10-10, review every 0 days

### `system-design.failure-modes` - Failure modes and resilience

- **Level:** advanced
- **Prerequisites:** `system-design.contracts`
- **Taught in:** `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience`
- **Sources:** `source-index#26`
- **Exercises:** `projects/00-core-foundations/python/10-system-design/challenges`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Explain, with runbooks, what happens when a dependency dies.
- **Target:** 6/10
- **Evidence required:** `adr`, `test`
- **Verified:** 2026-10-10, review every 0 days

## ml-foundations

### `ml.vectors-similarity` - Vectors and similarity

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/04-ai-engineering/applied-ml/01-vectors-and-similarity`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/applied-ml`
- **Used by:** `projects/04-ai-engineering/applied-ml`
- **Evidence:** Compute similarity by hand and explain why the metric fits the data.
- **Target:** 5/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `ml.evaluation-metrics` - Precision, recall, confusion

- **Level:** core
- **Prerequisites:** `ml.vectors-similarity`
- **Taught in:** `projects/04-ai-engineering/applied-ml/03-precision-recall-confusion`
- **Sources:** `source-index#12`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/applied-ml`
- **Used by:** `projects/04-ai-engineering/applied-ml`
- **Evidence:** Pick the right metric for an imbalanced task and defend it.
- **Target:** 5/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `ml.baselines-error-analysis` - Rules vs models, error analysis

- **Level:** advanced
- **Prerequisites:** `ml.evaluation-metrics`
- **Taught in:** `projects/04-ai-engineering/applied-ml/04-rules-vs-models-error-analysis`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/applied-ml`
- **Used by:** `projects/04-ai-engineering/applied-ml`
- **Evidence:** A rules baseline and a model compared with a real error analysis.
- **Target:** 5/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `ml.neural-net-foundations` - Neural network foundations

- **Level:** core
- **Prerequisites:** `ml.vectors-similarity`
- **Taught in:** `projects/04-ai-engineering/fastai-deep-learning/lectures/03-neural-net-foundations-lecture.md`
- **Sources:** `source-index#13`, `source-index#15`
- **Exercises:** `projects/04-ai-engineering/fastai-deep-learning/quizzes/03-neural-net-foundations.md`
- **Used by:** `projects/04-ai-engineering/fastai-deep-learning`
- **Evidence:** A small network trained from scratch whose loss curve and failure modes you can explain.
- **Target:** 5/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-14, review every 0 days

### `ml.nlp-foundations` - NLP foundations

- **Level:** core
- **Prerequisites:** `ml.neural-net-foundations`
- **Taught in:** `projects/04-ai-engineering/fastai-deep-learning/lectures/04-nlp-lecture.md`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/fastai-deep-learning/quizzes/04-nlp.md`
- **Used by:** `projects/04-ai-engineering/fastai-deep-learning`
- **Evidence:** A classification baseline whose errors are grouped by cause, not by count.
- **Target:** 5/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-14, review every 0 days

### `ml.transformers` - Transformers and the attention mechanism

- **Level:** core
- **Prerequisites:** `ml.neural-net-foundations`
- **Taught in:** `projects/00-core-foundations/python/07-machine-learning/deep-learning/40-transformers-from-scratch/40-transformers-from-scratch-lecture.md`
- **Sources:** `source-index#13`, `source-index#17`
- **Exercises:** `projects/00-core-foundations/python/07-machine-learning/deep-learning/40-transformers-from-scratch/40-transformers-from-scratch.py`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Implement scaled dot-product attention and explain why the cost is quadratic in sequence length.
- **Target:** 6/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-14, review every 0 days

## fine-tuning

### `fine-tuning.sft` - Supervised fine-tuning

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/01-supervised-fine-tuning`
- **Sources:** `source-index#20`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** One SFT run with a held-out loss and a sample output.
- **Target:** 6/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-10, review every 0 days

### `fine-tuning.lora-qlora` - LoRA and QLoRA

- **Level:** advanced
- **Prerequisites:** `fine-tuning.sft`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/02-lora-qlora`
- **Sources:** `source-index#20`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A 4-bit QLoRA run inside the 16 GB budget with VRAM measured.
- **Target:** 6/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-10, review every 90 days

### `fine-tuning.training-data` - Training data preparation

- **Level:** core
- **Prerequisites:** `fine-tuning.sft`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/03-training-data`
- **Sources:** `source-index#20`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A deduplicated, format-validated dataset with a data card.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `fine-tuning.model-registry` - Model registry and versioning

- **Level:** advanced
- **Prerequisites:** `fine-tuning.sft`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/05-model-registry`
- **Sources:** `source-index#20`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A versioned checkpoint registry with eval metadata per version.
- **Target:** 5/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-10, review every 0 days

### `fine-tuning.rag-vs-ft` - RAG vs fine-tuning

- **Level:** advanced
- **Prerequisites:** `fine-tuning.sft`, `rag.hybrid-retrieval`
- **Taught in:** `projects/04-ai-engineering/fine-tuning/06-rag-vs-fine-tuning`
- **Sources:** `source-index#20`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/fine-tuning`
- **Used by:** `projects/04-ai-engineering/fine-tuning`
- **Evidence:** A written decision on when to retrieve and when to fine-tune.
- **Target:** 6/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-10, review every 0 days

## arabic-nlp

### `arabic-nlp.text-fundamentals` - Arabic text fundamentals

- **Level:** core
- **Prerequisites:** `python.production`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/01-arabic-text-fundamentals`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** Explain harakat, presentation forms, and digit folding on real text.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-10, review every 0 days

### `arabic-nlp.normalization` - Arabic normalization and tokenization

- **Level:** core
- **Prerequisites:** `arabic-nlp.text-fundamentals`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/02-arabic-normalization-tokenization`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** A normalizer that is idempotent and proven on a golden text set.
- **Target:** 6/10
- **Evidence required:** `test`, `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `arabic-nlp.lexical-retrieval` - Arabic lexical retrieval

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.normalization`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/03-arabic-lexical-retrieval`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** A BM25 baseline on Arabic text with a measured recall.
- **Target:** 6/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `arabic-nlp.embeddings` - Arabic embeddings

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.normalization`, `rag.embeddings`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/04-arabic-embeddings`
- **Sources:** `source-index#16`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** An Arabic embedding model chosen with a measured retrieval delta.
- **Target:** 6/10
- **Evidence required:** `eval_report`, `adr`
- **Verified:** 2026-10-10, review every 90 days

### `arabic-nlp.hybrid-search` - Arabic hybrid search

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.embeddings`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/05-arabic-hybrid-search`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** A dense plus lexical fusion that beats each alone on Arabic.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `arabic-nlp.ann-search` - Arabic ANN search

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.embeddings`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/06-arabic-ann-search`
- **Sources:** `source-index#21`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** An ANN index with a recall vs latency tradeoff measured.
- **Target:** 6/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-10, review every 90 days

### `arabic-nlp.mrr-evaluation` - Arabic retrieval evaluation

- **Level:** advanced
- **Prerequisites:** `arabic-nlp.hybrid-search`, `eval.retrieval-metrics`
- **Taught in:** `projects/04-ai-engineering/arabic-nlp/07-arabic-mrr-evaluation`
- **Sources:** `source-index#25`
- **Exercises:** `projects/04-ai-engineering/arabic-nlp`
- **Used by:** `projects/04-ai-engineering/arabic-nlp`, `projects/04-ai-engineering/athar-lab`
- **Evidence:** An MRR harness on an Arabic golden set with reported numbers.
- **Target:** 7/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-10, review every 0 days

## model-serving

### `serving.model-selection` - Choosing a model

- **Level:** core
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/model-serving/01-choosing-a-model`
- **Sources:** `source-index#12`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/model-serving`
- **Used by:** `projects/04-ai-engineering/model-serving`
- **Evidence:** A model choice defended by size, license, and task fit.
- **Target:** 6/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-10, review every 90 days

### `serving.self-hosted` - Self-hosted models

- **Level:** advanced
- **Prerequisites:** `serving.model-selection`
- **Taught in:** `projects/04-ai-engineering/model-serving/02-self-hosted-models`
- **Sources:** `source-index#12`
- **Exercises:** `projects/04-ai-engineering/model-serving`
- **Used by:** `projects/04-ai-engineering/model-serving`
- **Evidence:** A quantized model served locally within the 16 GB VRAM budget.
- **Target:** 6/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-10, review every 90 days

### `serving.inference` - Inference serving

- **Level:** advanced
- **Prerequisites:** `serving.self-hosted`
- **Taught in:** `projects/04-ai-engineering/model-serving/03-inference-serving`
- **Sources:** `source-index#12`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/model-serving`
- **Used by:** `projects/04-ai-engineering/model-serving`
- **Evidence:** A served endpoint with measured throughput and latency.
- **Target:** 6/10
- **Evidence required:** `benchmark`
- **Verified:** 2026-10-10, review every 90 days

## security

### `security.llm-security` - LLM application security

- **Level:** advanced
- **Prerequisites:** `llm.fundamentals`
- **Taught in:** `projects/04-ai-engineering/security/lectures`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/security`, `projects/04-ai-engineering/devmate`
- **Evidence:** A blocked prompt-injection attempt from the OWASP LLM top-10.
- **Target:** 6/10
- **Evidence required:** `test`, `eval_report`
- **Verified:** 2026-10-10, review every 0 days

### `security.data-privacy` - Data privacy and retention

- **Level:** advanced
- **Prerequisites:** `security.llm-security`
- **Taught in:** `projects/04-ai-engineering/security/lectures/05-data-privacy-lecture.md`
- **Sources:** `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A data-flow note naming what leaves the trust boundary and under what policy.
- **Target:** 6/10
- **Evidence required:** `adr`, `test`
- **Verified:** 2026-10-14, review every 0 days

### `security.auth-authorization` - Authentication and authorization

- **Level:** advanced
- **Prerequisites:** `security.llm-security`
- **Taught in:** `projects/04-ai-engineering/security/lectures/06-authentication-authorization-lecture.md`
- **Sources:** `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** An RBAC matrix enforced in code, with a test proving a denied path stays denied.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `security.api-security` - API security and input validation

- **Level:** advanced
- **Prerequisites:** `security.auth-authorization`
- **Taught in:** `projects/04-ai-engineering/security/lectures/07-api-security-lecture.md`
- **Sources:** `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** Rate limit, size limit, and validation boundary each demonstrated by a rejected request.
- **Target:** 6/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `security.content-safety` - Content safety for Islamic knowledge

- **Level:** advanced
- **Prerequisites:** `security.llm-security`
- **Taught in:** `projects/04-ai-engineering/security/lectures/02-content-moderation-lecture.md`
- **Sources:** `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/athar-lab`
- **Evidence:** A policy that refuses a fatwa-style answer while still serving the cited source.
- **Target:** 6/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-14, review every 0 days

### `security.monitoring-audit` - Security monitoring and audit logging

- **Level:** advanced
- **Prerequisites:** `security.api-security`
- **Taught in:** `projects/04-ai-engineering/security/lectures/10-security-monitoring-lecture.md`
- **Sources:** `source-index#25`, `source-index#28`
- **Exercises:** `projects/04-ai-engineering/security/exercises`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One request reconstructable end to end from its audit record alone.
- **Target:** 6/10
- **Evidence required:** `test`, `deployment`
- **Verified:** 2026-10-14, review every 0 days

## architecture

### `arch.solid-clean-code` - Clean code and SOLID

- **Level:** core
- **Prerequisites:** none
- **Taught in:** `docs/learning/paths/adr-driven-ai-systems.md`
- **Sources:** `source-index#28`
- **Exercises:** `docs/learning/paths/adr-driven-ai-systems.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A module refactored so its business logic tests with the I/O faked, plus an ADR naming the rejected option.
- **Target:** 6/10
- **Evidence required:** `adr`, `test`
- **Verified:** 2026-10-14, review every 0 days

### `arch.hexagonal` - Hexagonal architecture, ports and adapters

- **Level:** advanced
- **Prerequisites:** `arch.solid-clean-code`
- **Taught in:** `docs/learning/paths/adr-driven-ai-systems.md`
- **Sources:** `source-index#28`
- **Exercises:** `docs/learning/paths/adr-driven-ai-systems.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One use case behind a port, satisfied by both a real and a fake adapter under the same contract test.
- **Target:** 6/10
- **Evidence required:** `adr`, `test`
- **Verified:** 2026-10-14, review every 0 days

### `arch.patterns-as-decisions` - Design patterns as recorded decisions

- **Level:** advanced
- **Prerequisites:** `arch.hexagonal`
- **Taught in:** `docs/learning/paths/adr-driven-ai-systems.md`
- **Sources:** `source-index#28`
- **Exercises:** `docs/learning/paths/adr-driven-ai-systems.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One pattern applied, with an ADR that names the alternative rejected and the cost accepted.
- **Target:** 6/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-14, review every 0 days

### `arch.adr-discipline` - ADR discipline

- **Level:** core
- **Prerequisites:** `system-design.contracts`
- **Taught in:** `projects/00-core-foundations/python/10-system-design/05-architecture-decision-records`
- **Sources:** `source-index#26`
- **Exercises:** `projects/00-core-foundations/python/10-system-design/challenges/05-architecture-decision-records`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** An ADR that states context, decision, rejected alternatives, and consequences a reviewer can act on.
- **Target:** 6/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-14, review every 0 days

## product

### `product.personas-jtbd` - Personas and jobs to be done

- **Level:** core
- **Prerequisites:** none
- **Taught in:** `docs/learning/paths/production-ai-systems-engineering.md`
- **Sources:** `source-index#28`
- **Exercises:** `docs/learning/paths/production-ai-systems-engineering.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One persona with a stated job, and a feature list cut to the minimum that completes it.
- **Target:** 5/10
- **Evidence required:** `adr`
- **Verified:** 2026-10-14, review every 0 days

### `product.north-star-metrics` - North-star metric and anti-metrics

- **Level:** core
- **Prerequisites:** `product.personas-jtbd`
- **Taught in:** `docs/learning/paths/production-ai-systems-engineering.md`
- **Sources:** `source-index#28`
- **Exercises:** `docs/learning/paths/production-ai-systems-engineering.md`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** One north-star metric with three anti-metrics, each with a stated way to measure it.
- **Target:** 5/10
- **Evidence required:** `eval_report`
- **Verified:** 2026-10-14, review every 0 days

## tooling

### `tooling.git-workflow` - Git workflow and branching

- **Level:** core
- **Prerequisites:** none
- **Taught in:** `projects/00-core-foundations/git-linux/01-git-basics`, `projects/00-core-foundations/git-linux/02-branching-merging`, `projects/00-core-foundations/git-linux/03-remote-workflows`
- **Sources:** `source-index#6`, `source-index#7`
- **Exercises:** `projects/00-core-foundations/git-linux`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A feature branch merged through a review, with the history explaining why each commit exists.
- **Target:** 5/10
- **Evidence required:** `pr`
- **Verified:** 2026-10-14, review every 0 days

### `tooling.linux-cli` - Linux command line

- **Level:** core
- **Prerequisites:** `tooling.git-workflow`
- **Taught in:** `projects/00-core-foundations/git-linux/04-linux-command-line`
- **Sources:** `source-index#6`
- **Exercises:** `projects/00-core-foundations/git-linux`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A diagnostic performed from the shell alone, without an IDE or a GUI tool.
- **Target:** 5/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days

### `tooling.ds-algorithms` - Data structures and algorithms

- **Level:** core
- **Prerequisites:** none
- **Taught in:** `projects/00-core-foundations/ds-algo/01-arrays-strings`, `projects/00-core-foundations/ds-algo/02-hash-maps`, `projects/00-core-foundations/ds-algo/03-recursion`, `projects/00-core-foundations/ds-algo/04-sorting-searching`
- **Sources:** `source-index#1`
- **Exercises:** `projects/00-core-foundations/ds-algo`
- **Used by:** `projects/04-ai-engineering/devmate`
- **Evidence:** A solution whose complexity is stated and justified against the input bound.
- **Target:** 5/10
- **Evidence required:** `test`
- **Verified:** 2026-10-14, review every 0 days
