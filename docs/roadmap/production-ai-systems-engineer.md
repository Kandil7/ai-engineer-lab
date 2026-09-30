# Production AI Systems Engineer — Roadmap

> **Strategic track.** Target: Production AI Systems Engineer / AI Platform Engineer /
> LLMOps Engineer — the engineer who builds the substrate other AI teams consume.
>
> **Plan of record remains** [`active-track-10-week.md`](active-track-10-week.md)
> ([ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md)). This document does
> not replace it. It defines production-depth work that sits on top of DevMate once the
> applied layer is real, and records what this repo already has versus what is missing.
>
> **Market research:** 2026-09-30 · **Repo audit:** 2026-09-30

---

## 1. Role definition

| Role | Primary output | Measured on |
| --- | --- | --- |
| **Production AI Systems / AI Platform** | Self-service substrate: gateway, serving stack, evals infra, cost/governance | Teams unblocked, cost per token, SLOs of shared services |
| Applied LLM / LLM Engineer | Product features on models (RAG, agents, prompts) | Feature quality, user outcomes |
| ML Engineer | Trained / fine-tuned models | Model metrics in production |
| Classical MLOps | Training pipelines, feature stores, registries | Pipeline reliability |

**One-line distinction:** an AI Platform Engineer's customers are *other engineers*. An
Applied AI Engineer's customers are *end users*. Platform work is judged by how much
velocity other teams get without you in the loop.

**Remote target titles:** AI Platform Engineer, Production AI Systems Engineer, LLMOps
Engineer, AI Infrastructure Engineer, Inference Platform Engineer, AI SRE.

**Remote-friendly companies to track (2026 postings):** Groq (geo-agnostic), Vercel
(AI Gateway), Together AI, Red Hat (vLLM / llm-d, FDE remote), Baseten (selected remote).
Re-check location clauses at application time; Egypt eligibility is posting-specific.

---

## 2. Relation to the active 10-week track

| Active weeks | Already advances production AI systems | Still missing after the track |
| --- | --- | --- |
| 0 | CI, packaging, test discipline | Eval gates, deploy gates |
| 1 | LLM client, tracing, cost ledger, prompt versioning | Dashboards, SLOs, budgets, routing |
| 2–3 | Golden set, eval harness, chunkers, hybrid RAG | Eval-as-CI-gate, online sampling, judge pinning |
| 4 | FastAPI, Docker, Postgres, public URL, SQL sprint | Load tests, integration tests, k8s |
| 5–6 | Agent tools, ReAct, LangGraph, MCP | Agent observability at platform scale |
| 7 | Semantic cache, guardrails, fallback, load tests, failure-modes | Cost enforcement, eval-gated rollback, red-team schedule |
| 8–10 | Portfolio, applications, interviews | Serving-engine depth, gateway, experiment tracking |

**Audit conclusion:** the active track covers roughly 60–70% of Production AI Systems
competency — the LLM application layer. The remaining 30–40% (self-hosted serving,
gateway/routing, experiment tracking, orchestration, cost *enforcement*, SLO operations)
is out of scope for the first remote AI/LLM role and correctly so. This track holds the
remainder.

**Sequence rule:** do not run this track concurrently with weeks 0–10. Finish at least
through **A4 (public URL)** and preferably **A6 (production hardening)** before Phase P1.
Starting earlier splits focus and repeats the curriculum-instead-of-shipping failure mode
documented in [`progress-dashboard.md`](progress-dashboard.md).

---

## 3. Gap analysis — current content vs this role

### 3.1 Exists and is real

| Asset | Path | Production value |
| --- | --- | --- |
| LLM client (streaming, retries, 3 providers, cost) | `projects/04-ai-engineering/devmate/src/devmate/llm/client.py` | High |
| Tracing + cost ledger | `devmate/src/devmate/obs/`, Langfuse in compose | Medium — instrumented, not operated |
| API with SSE, lifespan, health | `devmate/src/devmate/api/main.py` | High |
| Semantic cache | `devmate/src/devmate/cache/semantic_cache.py` | Medium — hit rate unmeasured |
| Guardrails | `devmate/src/devmate/guards/guardrails.py` | Medium — not red-teamed on a schedule |
| Agent + MCP | `devmate/src/devmate/agent/`, `devmate/src/devmate/mcp/` | Medium |
| RAG + vector store protocol | `devmate/src/devmate/retrieve/`, `devmate/src/devmate/index/` | High |
| LLMOps lifecycle guide | `projects/06-devops/llmops/README.md` | Design reference, not implementation |
| Production architecture reference | `docs/reference/llm-production-architecture.md` | Design reference |
| Model-serving curriculum | `projects/04-ai-engineering/model-serving/` (4 topics) | Curriculum only |
| Eval / observability curriculum | `docs/curriculum/lectures/04-evaluation-observability.md` | Curriculum only |
| Security curriculum | `projects/04-ai-engineering/security/` (10 topics) | Curriculum + toy exercises |
| Golden RAG set + baseline | `evaluations/rag/datasets/devmate-golden.jsonl` | Start of eval infra |

### 3.2 Partial — text or placeholder

| Domain | Evidence | Classification |
| --- | --- | --- |
| Evaluation infrastructure | `devmate/eval/README.md` states `run_ragas.py` does not exist | **Harness missing** |
| Load / performance testing | `devmate/tests/load/README.md` is a 5-line placeholder | **No numbers** |
| Integration testing | `devmate/tests/integration/README.md` is a 7-line placeholder | **Path untested** |
| Observability operations | Langfuse in compose + code; no dashboard, SLO, or alert | **Instrumented, not operated** |
| Cost engineering | `obs/cost.py` records spend; nothing enforces budgets or routes | **Visibility without control** |
| CI for AI quality | `.github/workflows/ci.yml` runs ruff/mypy/pytest only | **No eval gate** |
| Containerization | Compose stack real; `devmate/docker/Dockerfile` exists; no k8s | **Partial** |
| Self-hosted serving | `model-serving/02-self-hosted-models.py` is VRAM arithmetic + asserts | **Curriculum only** |
| LLMOps lifecycle | 9-phase guide exists; DevMate has versioned prompts only | **Guide ahead of code** |

### 3.3 Missing

| Domain | Evidence | Blocking for role? |
| --- | --- | --- |
| Self-hosted inference (vLLM / TGI) with measured TTFT/TPOT | No server process in repo | **Yes** for platform titles |
| Multi-provider gateway / model routing | 3 providers in client; no router | **Yes** for platform titles |
| Experiment tracking / model registry | Zero code; marked "overkill here" in llmops README | Medium — interview topic |
| Kubernetes / GPU orchestration | `infra/k8s/` does not exist; READMEs describe systems never built | Medium — role-dependent |
| Cost budgets, quotas, chargeback | Cost ledger only | **Yes** for senior platform signal |
| SLO / error-budget operations | None | **Yes** |
| Eval-gated release + rollback | Proposed YAML in llmops README; not in CI | **Yes** |
| Red-team schedule as CI | Week 7 content, not recurring | Medium |
| Multi-tenancy | Single-user DevMate | Medium — platform differentiation |
| Feature stores / classical MLOps | Interview questions and mastery-plan stubs only | **No** for most 2026 postings |

### 3.4 Production-adjacent, not production-grade

| Content | What it actually is | Do not claim it as evidence |
| --- | --- | --- |
| `model-serving/*.py` | 60–70-line demos; `--verify` checks arithmetic | "I can serve models" |
| `ai-evaluation/07-production-monitoring.py` | List averaging + `if` statements | "I run production monitoring" |
| `06-devops/*` READMEs | Docker/k8s/CI *descriptions* | "I operate infrastructure" |
| `thanaweyagpt/` scaffolds | README + `.gitkeep` | Any capstone claim |
| DevMate `tests/load/`, `tests/integration/`, `eval/` | Placeholders | "Production-hardened system" until filled |

### 3.5 Competency scoreboard (12 domains)

| # | Domain | Current | Target | Path forward |
| --- | --- | --- | --- | --- |
| 1 | Model serving & inference optimization | 2 | 7 | P5 |
| 2 | LLMOps pipelines | 3 | 7 | P1 + P6 |
| 3 | Observability & telemetry | 4 | 7 | P2 |
| 4 | Cost engineering | 3 | 7 | P3 |
| 5 | Reliability / SRE for AI | 3 | 7 | P4 |
| 6 | GPU infrastructure & orchestration | 1 | 5–6 | P5 + P7 |
| 7 | Evaluation infrastructure | 3 | 8 | P1 |
| 8 | Multi-tenancy & model gateway | 1 | 6 | P6 |
| 9 | Data / RAG platform | 4 | 7 | A3 + P1 |
| 10 | Agent runtime & tool governance | 3 | 6 | A5 + P2 |
| 11 | Security, guardrails, governance | 3 | 7 | A7 + P4 |
| 12 | Developer platform / DX | 2 | 6 | P8 |

Scale: 1 aware · 2 exposure · 3 basic · 4 working · 5 working+ · 6 intermediate ·
7 advanced · 8 expert. Levels require evidence: file path, test, URL, or measured number.

---

## 4. Competency domains (market-aligned)

1. **Model serving & inference optimization** — vLLM, TensorRT-LLM, TGI, SGLang; continuous
   batching, PagedAttention, KV-cache; TTFT vs TPOT; quantization; speculative decoding.
2. **LLMOps pipelines** — CI/CD for prompts, models, eval suites; canary/shadow deploys;
   automated rollback for semantic failures; golden sets as regression gates; model registry.
3. **Observability & telemetry** — TTFT, TPOT, tokens/sec, KV occupancy, queue depth;
   quality signals; cost telemetry; OTel GenAI conventions; distributed traces.
4. **Cost engineering** — cost per request *and per successful outcome*; token budgets;
   model routing; prompt + semantic caching; chargeback; cost-anomaly alerting.
5. **Reliability / SRE for AI** — SLOs and error budgets; on-call and postmortems;
   cold-start-aware autoscaling; provider failover; drain long streams on deploys.
6. **GPU infrastructure & orchestration** — K8s GPU scheduling, device plugins,
   multi-tenancy (MIG / time-slicing), DCGM, capacity planning.
7. **Evaluation infrastructure** — golden sets on real query distributions; pinned judge;
   CI gates vs absolute bars; drift detection; eval coverage as a platform KPI.
8. **Multi-tenancy & model gateway** — one API in front of self-hosted + third-party
   models; quotas; KV-aware routing; multi-provider fallback; usage attribution.
9. **Data / RAG platform** — vector DB operations, embedding pipelines, index rebuilds,
   hybrid search + rerank as platform defaults, corpus access control.
10. **Agent runtime & tool governance** — tool timeouts, MCP, durable memory,
    human-in-the-loop for irreversible actions, full tool-call traces.
11. **Security, guardrails, governance** — PII, prompt injection, jailbreak monitoring,
    policy-as-code, lineage, audit trails.
12. **Developer platform / DX** — golden paths, templates, SDKs, runbooks; your users
    are engineers on other teams.

---

## 5. Phased roadmap

**Vehicle:** DevMate is the applied-layer base. Production depth is added on top, not as
a second product. New work lands in:

```text
projects/04-ai-engineering/devmate/          # application + platform layers
projects/04-ai-engineering/model-serving/    # real serving labs (replace toy demos)
projects/06-devops/llmops/                   # LLMOps implementation notes
infra/production/                            # k8s / gateway / monitoring manifests
evaluations/                                 # gates, reports, red-team suites
docs/decisions/                              # ADRs for every irreversible pick
```

### Gate to start P-track

- [ ] Active-track **A4** done — public URL live
- [ ] Active-track **A6** done — cache, guardrails, fallback, load-test numbers
- [ ] `eval/` harness exists and prints a metrics table
- [ ] P-track does not steal Build time from the active window

**P-track progress note (2026-09-30):** week-1 A2 advanced. Prompt golden cases landed at
`evaluations/prompts/golden-cases/devmate.jsonl` (10 cases) with offline schema validation
in `devmate/tests/unit/test_prompt_golden.py`. Offline eval harness also landed:
`devmate/src/devmate/eval/run_ragas.py` + metrics + recorded retrieval/answer fixtures.
Live scoring / CI gate remains P1 after A4/A6. Langfuse UI keys still required for a
live traced `devmate ask` (compose comment documents the manual step).

### Phase P1 — Evaluation infrastructure as a platform (2 weeks)

**Why first:** routing, caching, model choice, and prompt changes are unprovable without
a gate.

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| Running RAG eval harness | `devmate/eval/` | recall@5/10, MRR, faithfulness printed from golden set |
| Prompt-change regression suite | `evaluations/prompts/golden-cases/` + runner | fails CI when metrics drop below floor |
| Eval gate wired into CI | `.github/workflows/ci.yml` | PR touching prompts/models/retrieve blocks on regression |
| Pinned judge configuration | `evaluations/judge/pinned.yaml` | judge model + prompt version recorded with every run |
| Hand-grade calibration sample | `evaluations/reports/hand-grade-*.md` | automated metrics correlated with human labels |
| Eval coverage report | `evaluations/reports/coverage.md` | % of product paths covered by golden cases |

**Milestone P1:** eval command exists, CI gates quality, numbers cite measured runs.

### Phase P2 — Observability and SLOs (2 weeks)

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| Observability dashboard | self-hosted Langfuse in compose | p50/p95 latency, tokens, cost, error rate visible |
| LLM-native metrics exported | `devmate/src/devmate/obs/` | TTFT, TPOT, tokens/sec where available |
| Quality signals in traces | `obs/tracing.py` | refusals, guardrail verdicts, structured-output failures |
| Written SLOs | `devmate/docs/slos.md` | p95 `/ask` latency, cost/request, faithfulness floor |
| Alert rules | `infra/production/alerts/` | latency, error-budget burn, cost anomaly |
| Error taxonomy | `devmate/docs/error-taxonomy.md` | 4xx vs 5xx vs provider vs guardrail vs timeout |

**Milestone P2:** you can answer "what is p95 latency and $/query right now?" without
opening a code file.

### Phase P3 — Cost engineering and routing (2 weeks)

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| Per-feature cost attribution | `obs/cost.py` + Postgres | query "most expensive routes this week" |
| Hard token and $ budgets | config + middleware | over-budget requests rejected or downgraded with typed error |
| Model routing rules | `devmate/src/devmate/llm/routing.py` | cheap model by default; escalate on structured uncertainty |
| Semantic cache KPI | cache module + dashboard | hit rate measured and trended |
| Cost-per-successful-outcome metric | eval + cost join | success = golden-case pass, not just 200 OK |
| Break-even memo (self-host vs API) | `docs/decisions/NNNN-cost-routing.md` | ADR with measured numbers on RTX 5000 and/or API pricing |

**Milestone P3:** cost is enforced, attributed, and routable — not merely logged.

### Phase P4 — Reliability, failure modes, adversarial suite (2 weeks)

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| Real load test | `devmate/tests/load/` | p50/p95/p99 under defined concurrency; number in README |
| Integration test suite | `devmate/tests/integration/` | API → Postgres → Redis → Qdrant path green |
| Failure-modes v2 | `devmate/docs/failure-modes.md` | every dependency failure exercised and dated |
| Circuit breakers + degradation | llm client + cache | provider death, Redis full, Qdrant kill mid-query |
| Red-team suite as scheduled job | `evaluations/redteam/` | OWASP LLM payloads; block-rate tracked over time |
| Chaos checklist run | `docs/learning/sessions/` | key revoke, mid-stream kill, oversized prompt |

**Milestone P4:** the system degrades instead of crashing, with tests that prove it.

### Phase P5 — Self-hosted serving lab (2–3 weeks)

**Constraint:** Dell Precision 7740, RTX 5000 16 GB VRAM, Turing sm_75. Not an A100
fleet. The lab proves *understanding and measurement*, not hyperscale operation.

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| vLLM (or TGI) serving a small open model | `projects/04-ai-engineering/model-serving/lab/` | server starts; OpenAI-compatible endpoint answers |
| TTFT / TPOT / throughput measurements | `model-serving/lab/reports/` | numbers recorded, not estimated |
| Quantization comparison | lab + report | FP16 vs 4-bit on quality (golden subset) vs latency vs VRAM |
| Prompt / prefix caching experiment | lab report | cache hit effect on cost and TTFT |
| Ollama vs vLLM comparison | lab report | when local beats API and when it does not |
| Integration with DevMate | env-flag provider in `llm/client.py` | `devmate ask` can hit local model |
| Honest capability statement | `model-serving/lab/README.md` | what sm_75 can and cannot claim |

**Milestone P5:** you can measure serving behavior on real hardware and defend the
numbers in an interview without overclaiming fleet scale.

### Phase P6 — Gateway, multi-provider ops, LLMOps release (2–3 weeks)

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| Model gateway in front of providers | `devmate/src/devmate/gateway/` or LiteLLM sidecar | one OpenAI-compatible endpoint; auth; rate limits; per-key budgets |
| Routing policies | gateway config | round-robin vs cost vs latency; multi-provider fallback |
| Eval-gated promote / rollback | CI + registry | prompt/model change merges only if gates pass; rollback is one command |
| Canary on the public deployment | deploy docs + checklist | traffic split, metric comparison, abort criteria |
| Prompt registry as deployable artifact | `devmate/src/devmate/llm/prompts/` + registry | every trace carries `prompt.version` |
| Runbooks | `devmate/docs/runbooks/` | alert → dashboard → trace query → rollback path |

**Milestone P6:** a prompt change cannot silently degrade production; rollback needs no
archaeology.

### Phase P7 — Orchestration depth (1–2 weeks, demand-gated)

**Start only if postings you care about require it.** Otherwise skip and keep compose.

| Deliverable | Path | Acceptance |
| --- | --- | --- |
| Kubernetes manifests for DevMate | `infra/production/k8s/` | apply on minikube/kind; health probes correct |
| GPU scheduling notes | ADR or lab doc | device plugins, cold-start reality, why HPA-on-CPU fails for LLM pods |
| GitOps or Helm packaging | `infra/production/` | one-command environment reproduce |
| Scaling story | written design | queue-depth / TTFT-based scaling narrative, not CPU% |

**Milestone P7:** you can explain and demonstrate how DevMate would run on K8s, with
cold-start and probe pitfalls named.

### Phase P8 — Platform-shaped capstone (2–3 weeks)

**Option A — Multi-tenant DevMate:** workspaces, quotas, chargeback, per-tenant evals.
**Option B — Mini AI Platform:** gateway + eval harness + cost dashboard + observability,
packaged so another engineer can onboard in one README. Prefer B if time is tight.

| Deliverable | Acceptance |
| --- | --- |
| Public live URL | recruiter can click without cloning |
| README as product spec | problem → architecture → eval table → $/query → failure modes → limits |
| Cost narrative | before/after caching and routing, with measured deltas |
| One open-source PR | vLLM, Ragas, LangChain, Ollama, or KServe — even small |
| One public ADR or generalized postmortem | decision + trade-off + revisit condition |
| Interview bank answers | production-platform questions drilled (see §7) |

**Milestone P8:** a stranger understands what the platform does, what it costs, and how
you know it works — in under two minutes from the README.

---

## 6. Milestones (P-track)

| ID | Milestone | Phase | Evidence | Status |
| --- | --- | --- | --- | --- |
| P0 | Gate: A4 + A6 complete | — | public URL + `failure-modes.md` | Planned |
| P1 | Eval infrastructure + CI gate | P1 | `evaluations/`, CI workflow change | Planned |
| P2 | SLOs + observability operations | P2 | `devmate/docs/slos.md`, dashboard | Planned |
| P3 | Cost enforcement + routing | P3 | budgets, `routing.py`, ADR | Planned |
| P4 | Reliability + red-team schedule | P4 | load tests, integration tests, `evaluations/redteam/` | Planned |
| P5 | Self-hosted serving lab | P5 | `model-serving/lab/reports/` | Planned |
| P6 | Gateway + eval-gated release | P6 | gateway code, rollback proof | Planned |
| P7 | K8s / orchestration depth | P7 | `infra/production/k8s/` | Planned — demand-gated |
| P8 | Platform capstone | P8 | live URL + README + OSS PR | Planned |

Dependency: `P0 → P1 → P2 → P3 → P4 → P5 → P6 → P8`; `P7` is optional between P6 and P8.

---

## 7. Evidence bar (what hiring managers scan for)

Must-have:

1. Production system others depend on — not a demo. Live URL in about 90 seconds.
2. Eval harness you can defend — golden set, automated scoring, regression detection,
   and a story about an eval failure you caught before launch.
3. Numbers, not claims — p50/p95 latency, tokens/sec, cost per 1k tokens, eval pass rates,
   dollar savings.
4. Failure-mode analysis — what broke, what changed afterward, which gate would have
   caught it.

Strong differentiators:

5. Open-source contribution to production AI infra (vLLM, Ragas, LangChain, Ollama, KServe).
6. Observability + cost narrative — e.g. "18% of agent runs hit a retry loop; here is the fix."
7. Platform-shaped work framed for other engineers, not end users.
8. Quantified impact — "cut inference cost 40% via prefix caching + routing while holding
   p95 TTFT under 800ms."

Weak signals that do not count: certificates as primary proof, Kaggle medals, tutorial
clones, notebook-only repos, tool lists without context of use.

---

## 8. Interview themes to drill

**System design (flagship):**

- Design an LLM inference serving platform (p95 targets, continuous batching, PagedAttention,
  KV-cache arithmetic, TTFT vs TPOT, prefix caching, TP size, quantization).
- Design a multi-tenant AI inference platform (packaging, autoscaling, routing, isolation,
  SLOs, cost controls, canary/shadow).
- Design an LLM gateway (auth, rate limits, token metering, per-team budgets, failover).
- Design ChatGPT / a chat product at scale (GPU memory, conversation storage, streaming).

**Strong answers state:** TTFT and TPOT targets unprompted; KV-cache arithmetic on the
board; prefill (compute-bound) vs decode (bandwidth-bound); goodput as the objective;
self-host break-even; cold-start realities; scale on queue depth / KV occupancy / TTFT p95.

**Trap answers:** "GPU utilization was 95% so we were fine"; least-connections for
inference; rolling deploys that kill long streams; HPA on CPU for GPU pods.

**Operational scenarios:** p99 TTFT doubled under load; CrashLoopBackOff during model
load; one team squatting the GPU fleet; provider down at peak; bill tripled; how to prove
a prompt change improved quality; define SLI/SLO/error budget for the inference platform.

**Not typically required:** PhD, pretraining research, CUDA kernels, deep classical ML
theory, frontend ownership, certifications as gates, fine-tuning as a daily skill.

---

## 9. Sources

| Topic | Source |
| --- | --- |
| Role cluster definition | aiinfrainterviews.com role comparison; AgenticCareers; Vibe Engines |
| Competency domains | OpenNebula, Red Hat vLLM/llm-d, SentinelOne, BlackRock, RTX, Together AI, Baseten postings |
| Interview design | SystemDesign Academy LLM inference guide; CareerStack AI Platform questions; sde2ai; InterviewLoop |
| Seniority signals | ai-infra-curriculum CAREER_PROGRESSION.md; MyEngineeringPath; MentorCruise |
| Evidence bar | Kore1 AI Engineer JD template; JobsByCulture portfolio guides; landed.jobs catalog |
| Remote targets | Groq, Vercel AI Gateway, Together AI, Red Hat FDE postings (2025–2026) |

Full research artifact: `context-store` id `job_market_production_ai_platform_2026`.
Repo audit artifact: `context-store` id `paie_repo_audit_2026_09_30`.

---

## 10. Related documents

| Document | Role |
| --- | --- |
| [`active-track-10-week.md`](active-track-10-week.md) | Plan of record through employment |
| [`milestones.md`](milestones.md) | Active A1–A10 + long-track M IDs |
| [`skills-matrix.md`](skills-matrix.md) | Skill levels with evidence rules |
| [`roadmap-sh-gap-analysis.md`](roadmap-sh-gap-analysis.md) | roadmap.sh AI Engineer coverage |
| [`../reference/llm-production-architecture.md`](../reference/llm-production-architecture.md) | Production LLM systems reference |
| [`../tracking/current-focus.md`](../tracking/current-focus.md) | What to do right now |
| [`phase-2-athar-baligh.md`](phase-2-athar-baligh.md) | Domain depth after employment |

*Last updated: 2026-09-30*
