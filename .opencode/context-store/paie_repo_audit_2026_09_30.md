---
id: paie_repo_audit_2026_09_30
reported_by: architect
created_at: 2026-09-30T14:42:22.896Z
---

# Production AI Systems Engineer — Repo Audit (2026-09-30)

## Verdict
Active 10-week DevMate track covers ~60-70% of Production AI Systems competency (LLM application layer). Remaining 30-40% is serving engines, gateway/routing, cost enforcement, SLO operations, experiment tracking, k8s/GPU orchestration.

## What is real
- DevMate LLM client (785 lines): streaming, retries, 3 providers, cost — `projects/04-ai-engineering/devmate/src/devmate/llm/client.py`
- Tracing + cost: `devmate/src/devmate/obs/`, Langfuse in `infra/docker/docker-compose.yml`
- API SSE/lifespan/health: `devmate/src/devmate/api/main.py`
- Semantic cache: `devmate/src/devmate/cache/semantic_cache.py`
- Guardrails: `devmate/src/devmate/guards/guardrails.py`
- Agent + MCP: `devmate/src/devmate/agent/`, `devmate/src/devmate/mcp/`
- RAG + vector store: `devmate/src/devmate/retrieve/`, `devmate/src/devmate/index/`
- LLMOps guide (design only): `projects/06-devops/llmops/README.md`
- Production arch reference: `docs/reference/llm-production-architecture.md`

## Placeholders (do not claim as production evidence)
- `devmate/eval/README.md` — run_ragas.py does not exist
- `devmate/tests/load/README.md` — 5-line placeholder
- `devmate/tests/integration/README.md` — 7-line placeholder
- `model-serving/*.py` — VRAM arithmetic demos, no server started
- `06-devops/{docker,deployment,ci-cd}/` — README only
- `thanaweyagpt/` — README + .gitkeep only

## Missing for PAI Systems titles
Self-hosted vLLM/TGI with TTFT/TPOT numbers; multi-provider gateway/routing; MLflow/registry; cost budgets/enforcement; SLO operations; eval-gated CI; k8s manifests (infra/k8s/ does not exist); multi-tenancy.

## Recommendation
Production track is Phase 3 after the 10-week track, not a concurrent plan. Gate: A4 + preferably A6. Highest-leverage immediate gaps already scheduled in active track: eval harness, load tests, integration tests, public URL.

## Written
`docs/roadmap/production-ai-systems-engineer.md` (P0-P8 phases, gap analysis, evidence bar, interview themes).
