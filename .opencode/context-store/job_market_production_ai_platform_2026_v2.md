---
id: job_market_production_ai_platform_2026_v2
reported_by: researcher
created_at: 2026-09-30T14:43:31.411Z
---

# Production AI Systems / AI Platform / LLMOps Job Market (2026-09-30) v2

## Role
Production AI Systems / AI Platform Engineer builds self-service substrate (gateway, serving stack, evals infra, cost/governance). Customers are other engineers. Measured on: teams unblocked, cost per token, SLOs of shared services. Distinct from Applied LLM Engineer (product features) and ML Engineer (trains models).

## 12 competency domains
1. Model serving & inference optimization (vLLM, TensorRT-LLM, TGI, continuous batching, PagedAttention, TTFT/TPOT, quantization)
2. LLMOps pipelines (eval-gated CI, canary, rollback, golden sets)
3. Observability (LLM-native metrics, OTel GenAI, cost telemetry)
4. Cost engineering (cost per successful outcome, routing, budgets, chargeback)
5. Reliability/SRE for AI (SLOs, cold-start autoscaling, circuit breakers)
6. GPU infrastructure & orchestration (K8s GPU, multi-tenancy, DCGM)
7. Evaluation infrastructure (golden sets, pinned judge, CI gates, drift)
8. Multi-tenancy & model gateway (quotas, KV-aware routing, fallback)
9. Data/RAG platform
10. Agent runtime & tool governance (MCP, HITL)
11. Security/guardrails/governance
12. Developer platform / DX (golden paths for other engineers)

## Evidence bar (hiring)
Must: production system + live URL, defensible eval harness, numbers (p95, $/query, eval rates), failure-mode analysis. Differentiators: OSS PR to vLLM/Ragas/LangChain/Ollama/KServe, cost narrative, platform-shaped project. Weak: certificates, Kaggle, tutorial clones, notebooks only.

## Interview themes
Design LLM inference platform; multi-tenant AI platform; LLM gateway; ChatGPT at scale. Strong answers: TTFT/TPOT unprompted, KV-cache math, prefill vs decode, goodput, cold-start, scale on queue depth not CPU%. Traps: GPU utilization %, least-connections, HPA on CPU for GPU pods.

## Not required
PhD, pretraining research, CUDA kernels, deep classical ML, frontend ownership, fine-tuning as daily skill, certifications as gates.

## Remote-friendly targets (Egypt)
Groq (geo-agnostic), Vercel AI Gateway, Together AI, Red Hat vLLM/llm-d FDE (remote), Baseten (selected remote). Verify location clauses per posting. Egypt eligibility UNKNOWN per posting.

## Sources
Official postings (Anthropic, Vercel, Baseten, Modal, Groq, Lambda, Together, Red Hat, OpenNebula, SentinelOne, BlackRock, RTX, Deutsche Telekom); SystemDesign Academy; CareerStack; ai-infra-curriculum; Kore1; JobsByCulture; landed.jobs.

## Written
docs/roadmap/production-ai-systems-engineer.md — phases P0-P8, gap analysis, evidence bar, interview themes.
