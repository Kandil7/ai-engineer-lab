# Skills Scoreboard

> Generated from `registries/evidence.yaml` joined with `registries/knowledge-registry.yaml` by `infra/scripts/build-skills-scoreboard.ps1`.
> Do not edit by hand. Run the script and commit the result. The knowledge gate fails CI when this file drifts.

**Summary:** 78 concepts, 15 with evidence, 0 at or above target, 63 with no evidence yet.
**Evidence provenance:** 4 script-checked, 11 self-assessed, 0 external. Prefer script-checked; self-assessed levels are claims until a test or gate backs them.

## python

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `python.production` Production Python | 7 | 2 | 5 | 1 (pr) |
| `python.testing` Test strategy (unit to regression) | 6 | 2 | 4 | 1 (test) |

## ai-engineering

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `llm.fundamentals` LLM fundamentals | 7 | 0 | 7 | none |
| `llm.streaming` Streaming and structured outputs | 7 | 0 | 7 | none |
| `llm.prompt-engineering` Prompt engineering | 7 | 0 | 7 | none |
| `obs.tracing` Observability and tracing | 6 | 1 | 5 | 1 (pr) |
| `obs.cost-tracking` Cost tracking | 6 | 2 | 4 | 1 (pr) |
| `rag.embeddings` Embeddings and model selection | 6 | 0 | 6 | none |
| `rag.chunking` Chunking strategies | 7 | 2 | 5 | 1 (pr) |
| `rag.vector-store` Vector store (Qdrant) | 7 | 0 | 7 | none |
| `rag.hybrid-retrieval` Hybrid retrieval (dense plus BM25) | 7 | 0 | 7 | none |
| `rag.reranking` Reranking | 7 | 0 | 7 | none |
| `rag.citations-abstention` Citations and abstention | 7 | 0 | 7 | none |
| `eval.golden-datasets` Golden datasets and annotation | 7 | 2 | 5 | 1 (eval_report) |
| `eval.retrieval-metrics` Retrieval metrics (recall, MRR) | 7 | 2 | 5 | 1 (eval_report) |
| `eval.faithfulness` Faithfulness and citation precision | 7 | 0 | 7 | none |
| `eval.llm-as-judge` LLM-as-judge | 7 | 0 | 7 | none |
| `eval.eval-in-ci` Evaluation in CI | 7 | 2 | 5 | 1 (deployment) |
| `agents.tool-use` Tool use | 7 | 0 | 7 | none |
| `agents.react` ReAct loop | 7 | 0 | 7 | none |
| `agents.mcp` Model Context Protocol | 6 | 1 | 5 | 1 (pr) |
| `agents.multi-agent` Multi-agent orchestration | 6 | 0 | 6 | none |
| `prod.semantic-cache` Semantic caching | 5 | 1 | 4 | 1 (pr) |
| `prod.guardrails` Guardrails and injection defence | 6 | 2 | 4 | 1 (pr) |
| `prod.ai-safety` AI safety and harm review | 6 | 0 | 6 | none |

## backend

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `backend.fastapi-service` FastAPI service | 7 | 2 | 5 | 1 (pr) |

## databases

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `databases.sql-schema` SQL schema and indexes | 6 | 1 | 5 | 1 (pr) |
| `databases.redis` Redis cache and queues | 5 | 0 | 5 | none |

## data-engineering

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `data.etl-pipelines` ETL/ELT and ingestion pipelines | 6 | 0 | 6 | none |
| `data.contracts` Schemas and data contracts | 6 | 0 | 6 | none |
| `data.reliability` Idempotency and checkpointing | 6 | 0 | 6 | none |
| `data.quality` Data quality and deduplication | 6 | 0 | 6 | none |
| `data.lineage` Provenance, versioning and lineage | 6 | 0 | 6 | none |
| `data.streaming-storage` Batch vs streaming and storage layout | 6 | 0 | 6 | none |
| `data.lakehouse` Lakehouse table layout | 5 | 0 | 5 | none |
| `data.feature-stores` Feature stores and feature pipelines | 5 | 0 | 5 | none |

## devops

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `deploy.docker` Docker containerization for AI services | 6 | 1 | 5 | 1 (deployment) |
| `deploy.ci-cd` CI/CD pipelines and quality gates | 6 | 0 | 6 | none |
| `deploy.strategies` Deployment strategies and Kubernetes fundamentals | 6 | 0 | 6 | none |
| `deploy.llmops` LLMOps lifecycle for production LLM systems | 7 | 0 | 7 | none |

## system-design

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `system-design.contracts` Component contracts | 6 | 2 | 4 | 1 (adr) |
| `system-design.failure-modes` Failure modes and resilience | 6 | 0 | 6 | none |

## ml-foundations

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `ml.vectors-similarity` Vectors and similarity | 5 | 0 | 5 | none |
| `ml.evaluation-metrics` Precision, recall, confusion | 5 | 0 | 5 | none |
| `ml.baselines-error-analysis` Rules vs models, error analysis | 5 | 0 | 5 | none |
| `ml.neural-net-foundations` Neural network foundations | 5 | 0 | 5 | none |
| `ml.nlp-foundations` NLP foundations | 5 | 0 | 5 | none |
| `ml.transformers` Transformers and the attention mechanism | 6 | 0 | 6 | none |

## fine-tuning

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `fine-tuning.sft` Supervised fine-tuning | 6 | 0 | 6 | none |
| `fine-tuning.lora-qlora` LoRA and QLoRA | 6 | 0 | 6 | none |
| `fine-tuning.training-data` Training data preparation | 6 | 0 | 6 | none |
| `fine-tuning.model-registry` Model registry and versioning | 5 | 0 | 5 | none |
| `fine-tuning.rag-vs-ft` RAG vs fine-tuning | 6 | 0 | 6 | none |

## arabic-nlp

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `arabic-nlp.text-fundamentals` Arabic text fundamentals | 6 | 0 | 6 | none |
| `arabic-nlp.normalization` Arabic normalization and tokenization | 6 | 0 | 6 | none |
| `arabic-nlp.lexical-retrieval` Arabic lexical retrieval | 6 | 0 | 6 | none |
| `arabic-nlp.embeddings` Arabic embeddings | 6 | 0 | 6 | none |
| `arabic-nlp.hybrid-search` Arabic hybrid search | 7 | 0 | 7 | none |
| `arabic-nlp.ann-search` Arabic ANN search | 6 | 0 | 6 | none |
| `arabic-nlp.mrr-evaluation` Arabic retrieval evaluation | 7 | 0 | 7 | none |

## model-serving

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `serving.model-selection` Choosing a model | 6 | 0 | 6 | none |
| `serving.self-hosted` Self-hosted models | 6 | 0 | 6 | none |
| `serving.inference` Inference serving | 6 | 0 | 6 | none |

## security

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `security.llm-security` LLM application security | 6 | 0 | 6 | none |
| `security.data-privacy` Data privacy and retention | 6 | 0 | 6 | none |
| `security.auth-authorization` Authentication and authorization | 6 | 0 | 6 | none |
| `security.api-security` API security and input validation | 6 | 0 | 6 | none |
| `security.content-safety` Content safety for Islamic knowledge | 6 | 0 | 6 | none |
| `security.monitoring-audit` Security monitoring and audit logging | 6 | 0 | 6 | none |

## architecture

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `arch.solid-clean-code` Clean code and SOLID | 6 | 0 | 6 | none |
| `arch.hexagonal` Hexagonal architecture, ports and adapters | 6 | 0 | 6 | none |
| `arch.patterns-as-decisions` Design patterns as recorded decisions | 6 | 0 | 6 | none |
| `arch.adr-discipline` ADR discipline | 6 | 0 | 6 | none |

## product

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `product.personas-jtbd` Personas and jobs to be done | 5 | 0 | 5 | none |
| `product.north-star-metrics` North-star metric and anti-metrics | 5 | 0 | 5 | none |

## tooling

| Concept | Target | Current | Gap | Evidence |
| --- | --- | --- | --- | --- |
| `tooling.git-workflow` Git workflow and branching | 5 | 0 | 5 | none |
| `tooling.linux-cli` Linux command line | 5 | 0 | 5 | none |
| `tooling.ds-algorithms` Data structures and algorithms | 5 | 0 | 5 | none |
