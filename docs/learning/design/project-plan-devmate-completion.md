# DevMate Completion Execution Plan (A1–A10 + AWS track)

### Context

Repo: ai-engineer-lab. Plan of record: docs/roadmap/active-track-10-week.md (adopted 2026-08-02, ADR-0004), vehicle DevMate, milestones A1–A10, target first applications 2026-10-12. Session goal: produce the ultra-detailed execution plan that completes the entire project, grounded in a verified state audit, and integrate the W3Schools AWS Cloud Practitioner tutorial (8h, CLF-C02 prep) the user shared as a parallel track.

### Explanation

## 0. Verified state audit (2026-08-05)

### What already exists (committed 2026-08-02, b5e52ee)
- Plan of record + ADR-0004/0005/0006; `.github/workflows/ci.yml` (devmate job, integration job disabled, docs-link job, freshness job, advisory legacy-lint); root `Makefile` with ci/lint/fmt/types/test/eval/run/up/down targets
- `infra/docker/docker-compose.yml` already declares postgres, redis, qdrant, langfuse, devmate-api, devmate-mcp, devmate-ui
- DevMate source: 21 files / ~5,600 lines covering ALL target modules (llm/client.py 583, agent/agent.py 590, api/main.py 338, cache 188, db/models.py 379, guards 307, index/embeddings 301 + vector_store 411, ingest/chunker 418 + repo_reader 234, mcp/server 251, obs/cost 173 + tracing 283, retrieve/rag 225 + retriever 252, cli/main 275, config 116) — a first draft written in ONE commit, never verified
- 3 unit tests (test_chunker, test_cost, test_repo_reader); Dockerfile (39 lines); `.venv` = Python 3.13.11 with only pydantic/httpx/tenacity/tiktoken/pytest/pytest-asyncio

### What is broken or missing (the real starting line)
1. `devmate` package NOT installed in the venv → all 3 tests fail with `ModuleNotFoundError`
2. No `poetry.lock`; poetry not installed on the machine (documented blocker) — local runs must use `pip install -e .[dev]` or CI-only poetry
3. venv lacks fastapi, uvicorn, qdrant-client, redis, sqlalchemy, alembic, langfuse, typer, rich, loguru, ruff, mypy, jinja2
4. `eval/`, `migrations/`, `ui/` directories are EMPTY (no run_ragas.py, no Alembic, no Streamlit app.py)
5. No `devmate/README.md`; no `llm/prompts/` Jinja templates; no golden cases (`evaluations/prompts/golden-cases/devmate.jsonl`); no RAG dataset (`evaluations/rag/datasets/devmate-golden.jsonl`)
6. No `agent/tools/` subpackage; no `ingest/chunkers/` subpackage; no hybrid retrieval/rerank code despite retrieve/ modules existing
7. Suspicious `pass` bodies outside Protocols: guards/guardrails.py:53, retrieve/retriever.py:37, cache/semantic_cache.py except-blocks, llm/client.py:98/111/115 — need audit
8. Zero tests for llm, agent, api, db, guards, index, retrieve, mcp, cache modules
9. Legacy Python baseline: 34 failing files (backlog R1–R7, R9) + CI-known 2 collection errors / 68 failures from directory shadowing
10. Cadence debt: 1 daily log (2026-07-18), 0 weekly reviews; `current-focus.md` stamped 2026-08-02 → freshness job fails after 2026-08-10; 0 PRs since the mega-commit

### The core risk
~90% of DevMate's code EXISTS but NOTHING is verified. The golden rule applies in reverse: code written in one AI-assisted mega-commit must be audited module-by-module and explained before it is trusted. The completion plan is therefore: verify → repair → measure → deploy → harden → package.

## 1. Phase W0 — Finish Week 0, achieve A1 (2 days: 08-05 → 08-06)

| # | Task | Owner agent | Acceptance |
|---|------|-------------|-----------|
| W0.1 | Make DevMate installable: `pip install -e ".[dev]"` in `.venv`; fix pyproject gaps (add streamlit, jinja2 already there, ensure eval/agents extras match CI) | software-engineer | `python -m pytest tests -q` collects, not ModuleNotFoundError |
| W0.2 | Generate lockfile for CI (poetry.lock via CI job `poetry lock`, or switch Makefile/CI to `pip install -e .[dev]` consistently — decide once, record in ADR) | dev-ops-platform-engineer | local `make ci` == GitHub Actions commands, both green |
| W0.3 | Module audit of all 21 source files: for each, classify VERIFIED / REPAIR (list defects) / REWRITE (stub or unfixable); fix the `pass` bodies in guards/retriever/cache/client; produce `devmate/docs/state-audit.md` | code-reviewer | every module has a status line; defects logged to `mistakes.md` |
| W0.4 | Expand unit tests: repo_reader edge cases (empty repo, binary files, .gitignore), chunker 3 strategies, cost math, guards, retriever mocks | test-engineer | `pytest` ≥ 25 tests green; coverage ≥ 60% on core modules |
| W0.5 | Run `devmate stats .` on this repo; fix output until correct (functions/classes/LOC/file-type counts) | software-engineer | CLI output matches manual counts on a fixture |
| W0.6 | Push → GitHub Actions green on master (ruff → format → mypy → pytest); docs-link + freshness jobs must pass | dev-ops-platform-engineer | CI badge green |
| W0.7 | Legacy remediation R1–R7 + R9 (34 failing files: hang, syntax, API drift, encoding, deps, SQL, Mongo, docs) | data-engineer | each fix reproduced + verified; backlog closed |
| W0.8 | 5 PRs with clean history (small, reviewable, one concern each) | human-led + code-reviewer | PR descriptions follow `.ai/workflows/feature/` chain |
| W0.9 | Cadence: daily log + update current-focus.md + weekly protocol first review | human-led | freshness job passes; 1 weekly review artifact |
| W0.10 | Decide scope: master-ai-engineering 12-topic module + fill embeddings/prompt-engineering/rag-system — ONLY after W0.1–W0.6 are green; else defer to buffer (ADR-0006 allows it, A1 gates it) | orchestrator | no lecture file created before `make ci` green |

**Milestone A1 gate:** `make ci` green locally AND on GitHub; `devmate stats .` prints correct stats; tests exist and pass; 5 merged PRs; remediation R1–R7/R9 closed.

## 2. Phase W1 — LLM layer traced and costed (A2, 1 week)

1. Audit/fix `llm/client.py` (583 lines): streaming, retries w/ backoff (tenacity), timeout, typed errors, structured output validation; fix any stubbed paths
2. Create `llm/prompts/` — versioned Jinja templates (system, answer, code-explainer) with schema-version metadata
3. Verify `obs/tracing.py` (Langfuse) and `obs/cost.py`: every call = 1 trace + token + $ cost; add `devmate ask --trace` flag
4. `cli/main.py`: `devmate ask "<question>"` streaming to rich console; verify cost report after each answer
5. Create `evaluations/prompts/golden-cases/devmate.jsonl` — 10 question→expected-property cases
6. Break-it-on-purpose session (network kill, 200k-token, malformed JSON) → `mistakes.md` entries + regression tests
7. Study-after-build: Huyen ch.1–3 → source-summary artifact

**A2 gate:** every LLM call visible in Langfuse with tokens+cost; can state $/ask from memory; golden cases pass.

## 3. Phase W2–3 — RAG, measured (A3, 2 weeks)

Order is fixed: dataset → harness → chunkers → stores → hybrid → rerank → ADRs.

1. `evaluations/rag/datasets/devmate-golden.jsonl` — 25 questions over THIS repo with expected source files (data-engineer)
2. `eval/run_ragas.py` + `evaluations/rag/harness/` — recall@5/10, MRR, faithfulness, answer relevance; `make eval` prints table (ai-evaluation-engineer)
3. `ingest/chunkers/` — fixed-size, recursive, AST-aware; keep tests for each (data-engineer)
4. Verify/fix `index/vector_store.py` Protocol + Qdrant adapter per ADR-0005; `index/embeddings.py` provider abstraction (vector-db-engineer, embedding-engineer)
5. Chroma adapter, time-boxed 2 days → comparison report (vector-db-engineer)
6. `retrieve/` hybrid dense+BM25 fusion, then rerank; fix retriever.py:37 stub (rag-optimization-engineer)
7. Two ADRs with results tables: chunking strategy, vector store (design-teacher + data)
8. Integration job in CI enabled (`if: false` → true) with Qdrant+Redis services; `make test-int` green (dev-ops-platform-engineer)

**A3 gate:** `make eval` prints metrics; ADRs cite numbers; can explain why AST-aware chunking wins on code.

## 4. Phase W4 — API, deploy, SQL sprint (A4, 1 week) ← the milestone

1. Verify/fix `api/main.py` (338 lines): `/health`, `/ask` SSE streaming, `/ingest`; lifespan loads client once; typed errors
2. Middleware: API-key auth + rate limiting; secrets only via env (security-compliance-engineer)
3. `db/models.py` audit + Alembic init: `migrations/` with initial revision; indexes justified in comments (database-engineer)
4. Docker multi-stage build verified (`docker/Dockerfile` 39 lines likely too thin — expand: builder stage, non-root, healthcheck); compose `devmate-api` boots with real stack; `make up` end-to-end smoke (dev-ops-platform-engineer)
5. **Deploy decision (see AWS track §10):** fast path Railway/Render for A4 on time; AWS production path right after
6. Streamlit `ui/app.py` (8501) — ingest a repo, ask questions, show sources + cost (frontend-engineer)
7. SQL sprint (3 days, real persistence): "most expensive queries this week" view → EXPLAIN → add indexes → measure before/after (database-engineer)

**A4 gate:** public URL a recruiter can click; governing rule lifts; keep-warm or cold-start note in README.

## 5. Phase W5–6 — Agents + MCP (A5, 2 weeks)

Build incrementally, one tool before the next (audit first: agent.py 590 lines may already contain a draft):
1. `agent/tools/` — search_code, read_file, run_tests, propose_patch (agent-systems-engineer)
2. Hand-rolled ReAct loop with step cap + loop detection + TEST proving infinite-loop prevention (ai-safety-engineer)
3. Port to LangGraph; comparison in notes.md (agent-systems-engineer)
4. MCP server: verify `mcp/server.py` against a real client (Claude Desktop / mcp inspector); streamable HTTP transport; compose devmate-mcp boots (full-stack-ai-engineer)
5. Agent eval: task completion rate, tool-selection accuracy → `evaluations/agents/` (ai-evaluation-engineer)

**A5 gate:** agent answers a ≥2-tool question; MCP reachable from a real client; loop-prevention test green.

## 6. Phase W7 — Production hardening (A6, 1 week)

1. Fix and verify `cache/semantic_cache.py` (188 lines, has bare `pass` in excepts) — Redis semantic cache with hit-rate metric (llm-ops-engineer)
2. `guards/guardrails.py` — fix stub; input: injection detection, size limits; output: PII scan, schema validation (ai-safety-engineer)
3. Fallback chain in llm/client.py: primary → cheaper → cached → graceful error (llm-ops-engineer)
4. LLM-aware tests: mocked client, prompt snapshots, VCR cassettes (qa-automation-engineer)
5. Load test + p50/p95 → `tests/load/` (observability-engineer)
6. Failure-injection day: revoke key mid-request, fill Redis, OWASP LLM top-10 prompt injection, kill Qdrant in flight → every entry lands in `devmate/docs/failure-modes.md` (ai-safety-engineer + observability-engineer)

**A6 gate:** cache hit-rate measured; injections blocked with evidence; graceful degradation proven.

## 7. Phase W8 — Portfolio (A7, 1 week)

Nothing new built; everything becomes legible: blog post (decisions, not tutorial), `devmate/README.md` (architecture diagram, eval numbers, $/query, demo GIF), CV targeted at remote AI roles, 3 recorded 2-min English explanations, 27 interview answers in `docs/reference/interview-bank.md`. If AWS cert track (below) is on schedule, sit CLF-C02 this week so it lands on the CV.

**A7 gate:** stranger understands the project from README alone in <2 min.

## 8. Phase W9–10 — Apply (A8/A9, 2 weeks)

20 applications/week logged in `docs/tracking/applications.md`; platforms: Wellfound, RemoteOK, WWR, LinkedIn remote, workatastartup; parallel contracting (Toptal/Turing); 2 mock interviews/week; gap-loop from every rejection → gap entry → task. Practical: W-2 vs 1099 vs EOR; Wise/Payoneer; timezone overlap offer.

## 9. Phase W11–12 — Buffer (A10)

Float only. Priority order: ML sprint (scikit-learn pipeline + one PyTorch loop + attention by hand → `07-machine-learning/`), LoRA/QLoRA if postings demand, DDIA chapters, Athar (Arabic RAG) revival, master-ai-engineering module if deferred in W0.

## 10. AWS track (integrating the W3Schools tutorial the user shared)

The tutorial = ~8h AWS Cloud Practitioner prep (CLF-C02): cloud concepts, EC2, Lambda, S3, RDS/DynamoDB, security (shared responsibility, IAM, CloudWatch/CloudTrail), pricing/free tier, well-architected. Three insertion points:

1. **Week 4 deployment decision (do not let AWS block A4):**
   - Fast path: Railway/Render per plan → recruiter-clickable URL in days. Recommended for A4.
   - AWS path (production-grade story, post-A4): **Lightsail** (simplest, predictable $3.5–10/mo, free-tier eligible) running docker-compose; or **Elastic Beanstalk** (managed) — both better interview material than "pushed to Render". ECS/Fargate if time allows.
2. **Weeks 4–5 study track (1h/day × 8 days):** work through the W3Schools tutorial (cloud essentials → compute → storage/databases → security → monitoring → pricing); apply each chapter to DevMate — e.g., RDS instead of compose Postgres, S3 for repo snapshots/artifacts, CloudWatch for the keep-warm ping + logs, SQS for async ingestion queue (excellent interview story), CloudTrail for audit. Log each mapping as a source-summary artifact per repo rule.
3. **Cert before week 8:** sit CLF-C02 (~$100) after the tutorial + free practice exams (AWS Skill Builder / ExamPro / free question banks) so the cert appears on the CV for A8/A9. Budget: 8h tutorial + 4h practice exams.

AWS services map for DevMate specifically: EC2/Lightsail (API+UI), RDS PostgreSQL (conversations/eval runs/cost), ElastiCache Redis OR Redis container (cache — note RDS has no Redis), S3 (ingested repo bundles), CloudWatch (logs/metrics/alarms), SQS (ingest jobs), optional Bedrock (Claude) as second provider in the fallback chain. The SQL sprint's EXPLAIN work transfers directly to RDS.

## 11. Cross-cutting cadence repair (parallel every week)

- Daily log via `infra/scripts/new-daily-log.ps1` (0 since 07-18 — restart now)
- Weekly review via `docs/WEEKLY_PROTOCOL.md` (0 so far — first one due 08-09)
- Update `current-focus.md` every Sunday (freshness job hard-fails at 8 days)
- One feature-chain artifact set per week: plan.md → ai-review.md → notes.md → mistakes.md
- PRs: small, one concern, from `.ai/workflows/feature/01-plan.md`

## 12. Agent assignment map

| Phase | Agents |
|---|---|
| W0 | software-engineer, dev-ops-platform-engineer, code-reviewer, test-engineer, data-engineer |
| W1 | full-stack-ai-engineer, prompt-engineer, llm-ops-engineer, observability-engineer |
| W2–3 | data-engineer, embedding-engineer, vector-db-engineer, rag-optimization-engineer, ai-evaluation-engineer, design-teacher |
| W4 | api-engineer, database-engineer, dev-ops-platform-engineer, frontend-engineer, security-compliance-engineer |
| W5–6 | agent-systems-engineer, software-engineer, ai-safety-engineer, ai-evaluation-engineer, full-stack-ai-engineer |
| W7 | llm-ops-engineer, ai-safety-engineer, qa-automation-engineer, observability-engineer |
| W8 | product-engineer, documenter, code-teacher, design-teacher |
| W9–10 | human-led; general/research for gap-loop research |
| Buffer | mlops-engineer, data-scientist |

## 13. Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| The 5,600-line draft is low-quality AI code the user can't explain | High | W0.3 audit is non-negotiable; rewrite modules where explanation fails; golden rule re-check hourly |
| Poetry unavailable locally delays `make ci` | High | Standardize on `pip install -e .[dev]` + uv/pip-tools lock; CI keeps poetry; Makefile uses venv python directly |
| AWS track expands scope and delays A4 | Medium | Fast-path deploy for A4; AWS is post-A4 depth + study track |
| Week 0 backlog (legacy remediation + curriculum) eats the week | Medium | A1 gates everything; curriculum deferred to buffer if needed |
| Langfuse/Qdrant/Redis version drift on Windows | Medium | Docker compose pinned images; integration CI job enabled at W2 |
| Cadence collapse (the demonstrated failure mode) | High | Freshness job + daily logs + weekly review as hard gates |

## 14. First 90 minutes (executing today)

1. `pip install -e ".[dev]"` in devmate/.venv; fix pyproject issues → tests collect
2. Run `ruff check .` + `mypy src/`; triage errors into fix-now vs audit-list
3. Audit `llm/client.py` + `ingest/repo_reader.py` first (they gate W0.5)
4. Fix `devmate stats .` until correct on this repo
5. Commit + push → confirm GitHub Actions green

### Alternatives

## Alternatives considered
1. **Rewrite DevMate from scratch** (ignore the 5,600-line draft): pros — clean, user-authored code satisfying the golden rule; cons — 2–3 weeks lost, plan slips A4, and much of the draft may be sound. Rejected as the default; adopted per-module: rewrite only modules that fail audit (W0.3).
2. **Deploy directly on AWS in week 4** (skip Railway/Render): pros — one platform, stronger portfolio story; cons — free-tier EC2 + RDS setup, DNS, security groups, and debugging add 2–4 days to the highest-risk week. Rejected for A4; kept as the post-A4 production path.
3. **Poetry everywhere** (as the plan assumed): pros — CI parity; cons — not installed locally, adds a tooling layer on Windows. Rejected; standardized on pip editable install + lockfile, CI unchanged.
4. **AWS cert as week-0 item**: pros — early CV item; cons — displaces A1, the actual gate. Rejected; scheduled weeks 4–5 study + exam in week 8.
5. **Build curriculum modules first** (current-focus tasks 4–5): the demonstrated failure mode (lectures instead of shipping). Rejected; gated behind A1 per ADR-0006.

### Rationale (Why this?)

The audit shows the repo is at a fork: the plan's week 0 assumed writing DevMate from scratch, but a 5,600-line draft already exists unverified. The plan therefore re-bases Week 0 as a verification-and-repair phase (audit before build) — this protects both the milestone dates and the learning golden rule (code must be explainable). AWS is integrated as a three-point track (deploy decision, study track, cert timing) so it strengthens the portfolio without delaying the A4 public URL, which is the single highest-leverage milestone for the job search. Cadence repair is treated as a hard gate because the documented failure mode is plan abandonment, not capability.

### Exercises

1. Run the W0.3 audit yourself on two modules: `llm/client.py` and `cache/semantic_cache.py` — mark every `pass` as Protocol-body vs stub vs swallowed-exception, then explain each file aloud without notes.
2. Get `devmate stats .` correct by hand for one directory (count functions/classes/LOC with grep) and compare against the CLI output.
3. After W1: write down the $ cost of a 5-answer session from memory, then verify against Langfuse.
4. After W2–3: reproduce the chunking ADR numbers by running `make eval` and re-deriving one metric (e.g., MRR) manually on a 3-question slice.
5. Week 4: explain the difference between Railway, Lightsail, and ECS to a non-technical person in 90 seconds (recorded).

### Next Steps

1. Execute W0.1–W0.2 (install package, fix pyproject, align Makefile/CI) — the immediate blocker.
2. Run W0.3 audit module-by-module with the code-reviewer agent, starting with llm/client.py and ingest/repo_reader.py.
3. Push and confirm GitHub Actions green (first CI commit since the workflow was written).
4. Update current-focus.md before 2026-08-10 (freshness job deadline).
5. Book the first weekly review for 2026-08-09 using docs/WEEKLY_PROTOCOL.md.
6. When A1 lands, start the W3Schools AWS tutorial at 1h/day during weeks 4–5, mapping each chapter to a DevMate component.

---
