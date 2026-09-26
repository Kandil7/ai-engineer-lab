# Gap Analysis — roadmap.sh AI Engineer vs. 10-Week Track

**Source:** roadmap.sh AI Engineer roadmap, topic inventory pulled 2026-09-26 from
`nilbuild/developer-roadmap`, `roadmaps/ai-engineer/content` on `master` (189 unique topics).
**Baseline:** [active-track-10-week.md](active-track-10-week.md), adopted by ADR-0004.

## Legend

| Status | Meaning |
| --- | --- |
| Covered | Scheduled with a build deliverable and definition of done |
| Partial | Touched but incomplete; no dedicated deliverable |
| Missing | No home in the track; suggested home given |
| Deferred | Documented trade-off in the track; revisit only if postings demand it |
| Divergence | Deliberate track choice that differs from the roadmap; not a gap |
| Out of scope | Not needed for a code-assistant vehicle aimed at a remote role |

## Tally

Covered 76 · Partial 37 · Missing 6 · Deferred 4 · Divergence 19 · Out of scope 47.
(189 unique slugs, machine-counted; multi-slug rows split on commas, zero duplicates.)

## 1. Orientation

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| what-is-an-ai-engineer | Covered | Track goal section; applied-LLM generalist framing |
| ai-vs-agi | Out of scope | Background trivia, no build relevance |
| ai-engineer-vs-ml-engineer | Covered | Deferred-ML section states the trade-off explicitly |
| how-llms-work | Partial | Chip Huyen ch. 1–3 after building; no deliverable |
| large-language-model-llm | Partial | Same as above |
| type-of-models | Partial | Week 1 works one provider deeply |
| pre-trained-models | Partial | Assumed; never taught |
| closed-vs-open-source-models | Partial | No comparison deliverable |
| choosing-the-right-model | Missing | Minor; could be a third ADR in weeks 2–3 |
| purpose-and-functionality | Out of scope | Product framing |
| impact-on-product-development | Out of scope | Product framing |
| know-your-customers--usecases | Out of scope | Product framing |
| introduction | Covered | Week 0 onboarding |

## 2. Providers and models

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| anthropic-claude | Covered | Week 1 primary provider |
| claude-messages-api | Covered | `devmate/src/devmate/llm/client.py` |
| openai-gpt-o-series | Out of scope | Single-provider depth chosen |
| openai-response-api | Out of scope | Same as above |
| open-ai-embeddings-api | Partial | Week 2–3 covers embedding choice generically |
| openai-compatible-apis | Partial | Fallback chain week 7 implies it |
| gemini, google-gemini, google-gemini-api | Out of scope | Single-provider depth chosen |
| deepseek, mistral, meta-llama, qwen, gemma | Out of scope | Single-provider depth chosen |
| cohere (2 nodes) | Out of scope | Rerank vendor; track reranks without naming one |
| openrouter | Out of scope | Week 7 fallback chain could use it; unnamed |
| self-hosted-models | Missing | Minor; no Ollama/vLLM anywhere |
| ollama, lm-studio | Missing | Minor; same as above |
| models-on-hugging-face | Partial | Sources list references HF docs; no deliverable |
| hugging-face, hugging-face-hub, hugging-face-models, hugging-face-tasks | Partial | Same as above |
| hugging-face-inference-sdk | Missing | Minor |
| transformersjs | Out of scope | Browser inference irrelevant to vehicle |

## 3. API mechanics

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| tokens | Partial | Cost tracking implies it; never taught directly |
| context-window | Partial | Prompt caching week 1; limits handled ad hoc |
| temperature | Covered | Week 1 inference parameters |
| top-k, top-p | Covered | Week 1 inference parameters |
| sampling-parameters | Covered | Week 1 inference parameters |
| repetition-penalties | Covered | Week 1 inference parameters |
| streaming-responses | Covered | Week 1 client + `/ask` SSE week 4 |
| structured-output | Covered | Week 1 Pydantic schemas |
| input-format | Partial | Covered via schemas; multimodal inputs excluded |
| function-calling, tools--function-calling | Covered | Week 1 basics, weeks 5–6 in depth |
| using-sdks-directly | Covered | Week 1 hand-rolled client |
| costlatency-monitoring | Covered | Week 1 cost tracking; latency week 7 load test |

## 4. Prompt engineering

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| prompt-engineering | Covered | Week 1 study block |
| zero-shot, few-shot | Covered | Week 1 study block |
| cot | Covered | Week 1 study block |
| react-prompting | Covered | Weeks 5–6 agent loop |
| system-prompting, role--behavior | Covered | Week 1 versioned Jinja templates |
| robust-prompt-engineering | Partial | No promptfoo-style A/B harness |
| prompt-caching | Covered | Week 1 explicit deliverable |
| prompt-vs-context-engineering, context-vs-prompt-eng | Partial | Tied to the context-engineering gap, section 8 |
| adding-end-user-ids-in-prompts | Missing | Minor; fold into week 7 guardrails |

## 5. Embeddings and chunking

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| what-are-embeddings, embedding, embeddings | Covered | Weeks 2–3 study + build |
| embedding-models | Covered | "Embeddings and when to use which model" |
| sentence-transformers | Covered | Implied local-embedding path; named in sources |
| gemini-embedding, jina | Partial | Covered under generic model choice |
| indexing-embeddings | Covered | Qdrant adapter, `devmate/src/devmate/index/` |
| chunking | Covered | Three chunkers + comparison ADR |
| haystack, ragflow | Divergence | Hand-rolled pipeline by design |
| long-context-processing | Partial | Handled ad hoc; no strategy deliverable |
| external-memory | Partial | Postgres conversations week 4; no memory design |

## 6. Vector databases

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| vector-database, vector-databases, vector-dbs | Covered | Weeks 2–3 + ADR-0005 |
| qdrant | Covered | Primary adapter |
| chroma | Covered | Comparison adapter, 2-day timebox |
| pinecone, weaviate, faiss, lancedb | Divergence | Two-store comparison serves the goal better than a tour |
| mongodb-atlas, supabase | Out of scope | Postgres is the track's store |

## 7. Retrieval and RAG

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| rag, rags, what-are-rags | Covered | Weeks 2–3 core |
| rag-usecases | Partial | DevMate itself is the use case; no survey |
| retrieval-process | Covered | Hybrid dense + BM25 + rerank |
| performing-similarity-search | Covered | VectorStore Protocol + adapters |
| semantic-search | Covered | Same as above |
| rag-and-dynamic-filters, rag--dynamic-filters | Covered | Weeks 2–3 hybrid retrieval |
| langchain, langchain-for-multimodal-apps | Divergence | Hand-rolled by design; LangGraph only at week 5 |
| llama-index, llamaindex-for-multimodal-apps | Divergence | Same as above |

## 8. Context engineering

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| context, context-engineering (2 nodes) | Covered | Week 5 context-engineering block |
| context-sources | Covered | Week 5 block |
| context-compaction | Covered | Week 5 block |
| context-evaluation | Covered | Week 5 block |
| context-failure-modes | Partial | Week 7 failure-modes doc covers system failures, not context failures |
| context-isolation | Covered | Week 5 block |
| context-security | Partial | Week 7 guardrails cover injection; isolation unaddressed |
| what-is-a-context-layer | Covered | Week 5 block |
| generation | Out of scope | Low-information node |

## 9. Agents

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| ai-agents (2 nodes) | Covered | Weeks 5–6 |
| agents-usecases | Partial | DevMate is the use case; no survey |
| multi-agents | Deferred | Weeks 11–12 buffer candidate |
| multi-agent-context-sharing | Deferred | Weeks 11–12 buffer candidate |
| react | Covered | Hand-rolled loop before LangGraph |
| manual-implementation | Covered | Explicit first step before frameworks |
| memory-systems | Partial | Conversations + semantic cache; no memory architecture |
| state--historical-context | Partial | Same as above |
| claude-agent-sdk | Divergence | Hand-rolled + LangGraph by design |
| openai-agentkit--agent-sdk | Divergence | Same as above |
| google-adk, vertex-ai-agent-builder | Divergence | Same as above |
| modus | Out of scope | Single-vendor framework node |

## 10. MCP

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| mcp, model-context-protocol-mcp | Covered | Weeks 5–6 study (modelcontextprotocol.io) |
| mcp-server, building-an-mcp-server | Covered | Week 5–6 step 5, 2-day budget |
| mcp-client, building-an-mcp-client | Covered | Week 6 step 7 |
| mcp-host | Covered | Week 6 step 7 |
| connect-to-local-server, connect-to-remote-server | Covered | Week 6 step 7 |
| transport-layer, data-layer | Covered | Week 6 MCP study block |

## 11. Evaluation and observability

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| evaluation-metrics | Covered | recall@5/10, MRR, faithfulness, relevance |
| llm-evaluations | Covered | Eval harness weeks 2–3 + agent eval weeks 5–6 |
| deterministic-evals | Partial | Golden sets serve this role; never framed as such |
| model-based-evals | Partial | Faithfulness/relevance imply a judge; unnamed |
| human-evals | Covered | Weeks 2–3 hand-grading round |
| ragas | Covered | `devmate/eval/run_ragas.py` |
| deepeval | Divergence | One harness picked; RAGAS |
| regression-testing | Partial | Prompt snapshots week 7 approximate it |
| llm-observability | Covered | Langfuse from week 1 |
| tracing--logging | Covered | `devmate/src/devmate/obs/tracing.py` |
| langfuse | Covered | Pinned in sources |
| langsmith, helicone, arize-ai, posthog | Divergence | One platform picked; Langfuse |
| production-monitoring | Partial | Load test + latency numbers; no dashboards or alerts |

## 12. Training and fine-tuning

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| fine-tuning | Deferred | Week 11+ buffer, conditional on postings |
| training | Deferred | Same as above (ML sprint) |
| rag-vs-fine-tuning | Partial | Decision implicit; never written as ADR |

## 13. Safety and governance

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| ai-safety-and-ethics | Partial | Guardrails + OWASP payload; no ethics framing |
| bias-and-fairness | Out of scope | No user-facing classification in vehicle |
| security-and-privacy-concerns | Partial | API auth week 4, PII scan week 7 |
| prompt-injection-attacks | Covered | Week 7 input guardrails with evidence |
| constraining-outputs-and-inputs, constrains, constraints | Covered | Schema validation both sides week 7 |
| content-moderation-apis | Out of scope | Hand-rolled guards chosen |
| conducting-adversarial-testing | Partial | One payload; not a discipline |
| data-classification | Out of scope | No sensitive-data flows in vehicle |
| atlan, datahub | Out of scope | Enterprise catalogs |

## 14. Multimodal

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| multimodal-ai, multimodal-ai-usecases | Out of scope | No modality in a code assistant; note as decided |
| image-generation, image-understanding | Out of scope | Same as above |
| video-understanding | Out of scope | Same as above |
| audio-processing, speech-to-text, text-to-speech | Out of scope | Same as above |
| whisper-api, dall-e-api, openai-vision-api, nanobanana-api | Out of scope | Same as above |

## 15. Domains, tools, inference

| Roadmap topic | Status | Track home / note |
| --- | --- | --- |
| recommendation-systems, anomaly-detection | Out of scope | Domain use cases outside the vehicle |
| roles-and-responsiblities | Out of scope | Career framing, covered by week 8 CV work |
| development-tools | Out of scope | Tools are used, not studied |
| claude-code, cursor, windsurf, codex, replit | Out of scope | Same as above |
| inference | Partial | API hosting week 4; model serving never covered |

## Recommendation

Applied 2026-09-26: sampling parameters (week 1), metadata filtering and one
hand-grading round (weeks 2–3), context-engineering block (week 5), MCP-client step
(week 6), and a documented deferral for multi-agent, multimodal, and self-hosted
models. Everything else either is covered or is correctly out of scope. The rows
above still describe the roadmap side; the track side has moved.
