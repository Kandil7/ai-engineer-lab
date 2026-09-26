# Active Track — 10-Week AI Engineer (Remote)

> **This is the plan of record.** Adopted by [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md)
> on 2026-08-02. It supersedes [`master-roadmap.md`](master-roadmap.md) as the active plan;
> that document is retained as the **long track** for post-employment depth.

**Start:** 2026-08-03 · **Target application date:** 2026-10-12 (week 10) ·
**Window:** 12 weeks for 10 weeks of work
**Vehicle:** DevMate — `projects/04-ai-engineering/devmate/`
**Availability assumed:** 5+ hours/day, full-time

---

## 1. Goal

A remote AI/LLM engineering role. The deliverable that gets there is **one deployed,
evaluated, observable system** plus the ability to explain every decision inside it.

Not the deliverable: more curriculum, more lectures, more finished tutorial exercises.

### The governing rule

> **The lecture moratorium is lifted — but only because the ratio argument is already satisfied.**
> [ADR-0006](../decisions/0006-adopt-master-ai-engineering-curriculum.md) amended the original
> rule from ADR-0004: new lectures, glossaries, quizzes, case studies, and challenges are
> permitted **provided the curriculum is production-focused and anchored to the active DevMate
> work**. The original rule — *no new lecture, glossary, or quiz file until DevMate is deployed
> at a public URL* — is superseded.
>
> What remains in force: **the repo must keep at least one running service (DevMate), and the
> curriculum must trace to a DevMate concept or an interview answer.** The failure mode the
> rule existed to prevent — lectures replacing shipping — is still guarded, now by rule 6 below.

---

## 2. The project — DevMate

An AI assistant for code repositories. It ingests a GitHub repo or docs folder, answers
questions about it, explains code, and proposes changes.

It evolves along one continuous line rather than restarting each week:

```text
week 0   CLI that reads a repo and prints statistics
week 1   + LLM: streaming answers, structured output, traced and costed
week 2-3 + RAG: chunk → embed → hybrid retrieve → rerank, with an eval harness
week 4   + API: FastAPI, Docker, deployed, Streamlit UI, Postgres persistence
week 5-6 + Agent: tools, ReAct, LangGraph, MCP server
week 7   + Production: cache, guardrails, fallback, LLM-aware tests
week 8   + Portfolio: blog post, README, demo, CV
```

**Why this project:** covers RAG + agents + tool use in one artifact; needs no content
sourcing (this repo is the test corpus); is immediately legible to an engineer interviewer;
grows without rewrites.

**Athar / Baligh (Arabic RAG, Arabic LLM fine-tuning) are phase 2** — revived after the job
search as the domain-depth story. Their deep-dives in `docs/learning/deep-dives/` stay valid.

---

## 3. Corrections applied to the source plan

The source plan (`docs/plan/archive/AI_Engineer_Roadmap.md`) is followed except for these six
changes, each recorded in ADR-0004:

| # | Source plan said | This track says | Why |
| --- | --- | --- | --- |
| 1 | RAGAS in week 8 | Eval harness in weeks 2–3 | Week 3 asks you to compare 3 chunking strategies. Without measurement that comparison is opinion. Eval is a precondition, not a capstone. |
| 2 | Langfuse in week 8 | Tracing + cost from week 1 | The source transcript itself says connect it "from day one of this phase, not last". The distilled plan contradicted its own source. |
| 3 | No CI anywhere | CI green in week 0 | The same plan argues your GitHub *is* your CV for remote roles. A repo with no pipeline undercuts that. |
| 4 | SQL never scheduled | 3-day sprint in week 4 | Listed as required twice in the source, scheduled zero times. Folded in as real persistence, not standalone study. |
| 5 | Python refresher = 7 days | Week 0 = 2–3 days | 354 Python files already exist, including all 20 advanced topics and 25 FastAPI topics. Week 1 and most of week 5 collapse. |
| 6 | 9 weeks, zero buffer | 10 weeks in a 12-week window | One bad week otherwise cascades through every subsequent one. |

### Deliberately deferred

**Classical ML/DL** — no scikit-learn, no PyTorch, no attention internals in weeks 0–10. This
is a real trade-off, not an oversight: it is correct for an applied-LLM generalist role and
wrong for a research-leaning one. Scheduled as a sprint at week 11+ into the existing
`projects/00-core-foundations/python/07-machine-learning/` folder.

**Go / Flutter / Next.js** — paused. Lives on in [`master-roadmap.md`](master-roadmap.md).

**Multi-agent systems, multimodal, self-hosted models** — deferred. No home in weeks 0–10;
multi-agent is a weeks 11–12 buffer candidate. Multimodal and self-hosted serving stay out
unless postings demand them.

---

## 4. Week-by-week

Every week runs through the existing artifact chain in `.ai/workflows/feature/`:
`01-plan → 02-design → 03-build → 04-review → 05-fix → 06-reflect`, producing `plan.md`,
`ai-review.md`, `notes.md`, and `mistakes.md` in the DevMate folder — the same chain
`auth-service` already demonstrates.

---

### Week 0 — Foundation and hygiene (2–3 days)

Compressed hard, because the Python work is already done.

**Study (minimal):** skim your own `02-advanced-python/` notes on decorators, generators,
context managers, async. Git deep practice — branching, merge conflicts, interactive rebase —
performed **on this repo**, not on a tutorial sandbox.

**Build:**

| Deliverable | Path |
| --- | --- |
| Repo hygiene: pyproject typo, gitignore, tracked binaries removed | repo root |
| CI pipeline: ruff → black --check → mypy → pytest, green | `.github/workflows/ci.yml` |
| Root Makefile | `Makefile` |
| Poetry env for DevMate | `projects/04-ai-engineering/devmate/pyproject.toml` |
| `devmate stats <repo>` — counts functions, classes, LOC, file types | `devmate/src/devmate/ingest/repo_reader.py` |
| Tests for the stats CLI | `devmate/tests/unit/` |
| 5 PRs with clean history | this repo |

**Definition of done:** `make ci` passes locally and on GitHub. `devmate stats .` prints real
statistics about this repo. 5 merged PRs.

**Milestone:** A1

---

### Week 1 — LLM layer, observable from day one

**Study:** Claude API — messages, streaming, structured outputs, tool-use basics, prompt
caching. Inference parameters: temperature, top-k/top-p, repetition penalties.
Prompt engineering: zero-shot, few-shot, chain-of-thought, system-prompt design.
Read *AI Engineering* (Chip Huyen) ch. 1–3 **after** the day's code, not before.

**Build:**

| Deliverable | Path |
| --- | --- |
| LLM client: streaming, retries with backoff, timeout, typed errors | `devmate/src/devmate/llm/client.py` |
| Pydantic schemas for structured outputs | `devmate/src/devmate/llm/schemas.py` |
| Versioned Jinja prompt templates | `devmate/src/devmate/llm/prompts/` |
| **Langfuse tracing wired in** | `devmate/src/devmate/obs/tracing.py` |
| **Token + $/request cost tracking** | `devmate/src/devmate/obs/cost.py` |
| CLI: `devmate ask "<question>"` with streaming output | `devmate/src/devmate/cli.py` |
| 10 golden cases (question → expected properties) | `evaluations/prompts/golden-cases/devmate.jsonl` |

**Break it on purpose:** kill the network mid-stream; send a 200k-token prompt; force a
malformed structured output. Record each failure and its handling in `mistakes.md`.

**Definition of done:** every LLM call appears as a Langfuse trace with token count and cost.
You can state the cost of one `devmate ask` in dollars.

**Milestone:** A2

---

### Weeks 2–3 — RAG, measured

The heaviest two weeks. Eval comes **first**, so every later choice is backed by numbers.

**Study:** embeddings and when to use which model; chunking strategies; hybrid search
(dense + BM25); reranking. DeepLearning.AI "Building and Evaluating Advanced RAG".
*AI Engineering* RAG chapter — again, after building.

**Build, in this order:**

1. **Golden set first** — 25 questions over this repo with expected source files.
   `evaluations/rag/datasets/devmate-golden.jsonl`
2. **Eval harness** — recall@5, recall@10, MRR, faithfulness, answer relevance.
   `devmate/eval/run_ragas.py`. Hand-grade a sample of answers to calibrate the metrics.
3. **Three chunkers** — fixed-size, recursive, AST-aware (code-structure boundaries).
   `devmate/src/devmate/ingest/chunkers/`
4. **`VectorStore` Protocol** + Qdrant adapter, per [ADR-0005](../decisions/0005-vector-db-qdrant-over-chromadb.md).
   `devmate/src/devmate/index/`
5. **Chroma adapter** — time-boxed to 2 days; comparison report.
6. **Hybrid retrieval** — dense + BM25 fusion, metadata filtering, then reranking.
   `devmate/src/devmate/retrieve/`
7. **Two ADRs**, each with a results table: chunking strategy, vector store comparison.

**Definition of done:** `make eval` prints a metrics table. The chunking ADR cites measured
numbers, not intuition. You can explain why AST-aware chunking helps on code specifically.

**Milestone:** A3

---

### Week 4 — API, deploy, and the SQL sprint

**Study:** FastAPI is largely already covered (25 topics in `05-web-frameworks/fastapi/`) —
skim only streaming responses, lifespan events, and dependency injection. Docker: images vs.
layers, multi-stage builds. SQL: joins, indexes, query plans, migrations.

**Build:**

| Deliverable | Path |
| --- | --- |
| `/health`, `/ask` (SSE streaming), `/ingest` | `devmate/src/devmate/api/` |
| Model/client loaded once at startup via lifespan | `devmate/src/devmate/api/main.py` |
| Rate limiting + API key auth | `devmate/src/devmate/api/middleware/` |
| **Postgres: conversations, messages, eval runs, cost per query** | `devmate/src/devmate/db/` |
| Migrations (Alembic) with indexes justified in comments | `devmate/migrations/` |
| Multi-stage Dockerfile | `devmate/docker/Dockerfile` |
| Service added to the existing compose stack | `infra/docker/docker-compose.yml` |
| Deployed to Railway or Render — **public URL** | — |
| Streamlit UI | `devmate/ui/app.py` |

**SQL sprint (3 days, inside this week):** design the schema yourself; write the queries that
power a "show my most expensive queries this week" view; read the query plans; add the indexes
that fix them. This is the SQL requirement, satisfied as real persistence.

**Definition of done:** a public URL a recruiter can click. The governing rule lifts here.
Note free-tier cold starts — add a keep-warm ping or say so in the README.

**Milestone:** A4 — **first portfolio-ready artifact**

---

### Weeks 5–6 — Agents and MCP

**Study:** tool use in depth; ReAct; LangGraph; **MCP (Model Context Protocol)**; context
engineering (compaction, isolation, failure modes). Hugging Face
Agents Course, one module per day, applying each to DevMate rather than to course examples.

**Build incrementally — one tool working before the next is added:**

| Step | Deliverable |
| --- | --- |
| 1 | Single tool: `search_code`, hand-rolled loop, no framework |
| 2 | ReAct loop with a step cap and loop detection |
| 3 | Port to LangGraph; compare against the hand-rolled version in `notes.md` |
| 4 | Tools 2–4: `read_file`, `run_tests`, `propose_patch` |
| 5 | **MCP server exposing DevMate retrieval to any MCP client** |
| 6 | Agent eval: task completion rate, tool-selection accuracy |
| 7 | **MCP client: consume an outside MCP server from the DevMate agent** |

Paths: `devmate/src/devmate/agent/tools/`, `agent/graph.py`, `devmate/mcp/`

**MCP is the differentiator.** It appears in current postings, and this repo has zero MCP
code today. Budget 2 full days.

**Definition of done:** the agent answers a question requiring ≥2 tools. The MCP server is
reachable from a real MCP client. Infinite loops are provably prevented — with a test.

**Milestone:** A5

---

### Week 7 — Production hardening

**Study:** semantic caching; guardrails and prompt-injection defence; testing strategies
specific to non-deterministic systems.

**Build:**

| Deliverable | Path |
| --- | --- |
| Redis semantic cache (not exact-match) with hit-rate metric | `devmate/src/devmate/cache/` |
| Input guardrails: injection detection, size limits | `devmate/src/devmate/guards/input.py` |
| Output guardrails: PII scan, schema validation | `devmate/src/devmate/guards/output.py` |
| Model fallback chain (primary → cheaper → cached → graceful error) | `devmate/src/devmate/llm/client.py` |
| LLM-aware tests: mocked client, prompt snapshots, recorded cassettes | `devmate/tests/` |
| Load test + p50/p95 latency numbers | `devmate/tests/load/` |
| Failure-modes document | `devmate/docs/failure-modes.md` |

**Break it on purpose:** revoke the API key mid-request; fill Redis; submit a prompt-injection
payload from the OWASP LLM top-10; kill Qdrant while a query is in flight. Every one gets an
entry in `failure-modes.md`.

**Definition of done:** cache hit rate measured; injection attempts blocked with evidence;
the system degrades rather than crashes when a dependency dies.

**Milestone:** A6

---

### Week 8 — Portfolio

Nothing new is built. Everything built becomes legible.

| Deliverable | Path |
| --- | --- |
| Technical blog post — decisions and trade-offs, not a tutorial | `docs/writing/devmate-engineering.md` |
| Portfolio README: architecture diagram, eval numbers, $/query, demo GIF | `devmate/README.md` |
| CV targeted at remote AI roles | `docs/career/cv.md` |
| LinkedIn + GitHub profile cleanup | — |
| 3 recorded 2-minute English explanations (project, RAG pipeline, hardest bug) | `docs/career/recordings/` |
| Answers drafted for all 27 interview questions | `docs/reference/interview-bank.md` |

**Definition of done:** someone who has never seen the project understands what it does and
why it is built that way, from the README alone, in under two minutes.

**Milestone:** A7

---

### Weeks 9–10 — Apply

| Activity | Cadence |
| --- | --- |
| Applications | 20/week, logged in `docs/tracking/applications.md` |
| Platforms | Wellfound, RemoteOK, We Work Remotely, LinkedIn (Remote filter), workatastartup.com |
| Contracting entry | Toptal / Turing as a parallel path |
| Mock interviews | 2/week in English |
| Gap loop | every rejection or stumble → a gap entry → a task |

**Practical setup:** understand W-2 vs. 1099 vs. EOR (Deel, Remote.com); open Wise or
Payoneer; decide and be able to state your timezone-overlap offer (3–4 hours is the common
expectation).

**Milestones:** A8, A9

---

### Weeks 11–12 — Buffer, then depth

**These two weeks are float.** They absorb slippage from weeks 0–10. Do not pre-fill them.

If unused, in priority order:

1. **Deferred ML sprint** — scikit-learn pipeline end-to-end, one PyTorch training loop from
   scratch, attention implemented by hand once, into
   `projects/00-core-foundations/python/07-machine-learning/`. Closes the stated gap. → A10
2. Fine-tuning (LoRA/QLoRA) if postings you are seeing ask for it.
3. System design depth — *Designing Data-Intensive Applications*, selected chapters.
4. Revive Athar (Arabic RAG) as the domain-depth story.

---

## 5. Milestones

| ID | Milestone | Week | Evidence | Status |
| --- | --- | --- | --- | --- |
| A1 | CI green + `devmate stats` CLI | 0 | `.github/workflows/ci.yml`, `devmate/src/` | Planned |
| A2 | LLM layer traced and costed | 1 | `devmate/src/devmate/obs/` | Planned |
| A3 | RAG with measured eval + 2 ADRs | 2–3 | `evaluations/rag/reports/` | Planned |
| A4 | **Deployed at a public URL** | 4 | live link in `devmate/README.md` | Planned |
| A5 | Agent with 4 tools + MCP server | 5–6 | `devmate/src/devmate/agent/`, `devmate/mcp/` | Planned |
| A6 | Production hardening | 7 | `devmate/docs/failure-modes.md` | Planned |
| A7 | Portfolio complete | 8 | `docs/writing/`, `docs/career/` | Planned |
| A8 | 40 applications submitted | 9–10 | `docs/tracking/applications.md` | Planned |
| A9 | First technical interview | 9–10 | `docs/tracking/applications.md` | Planned |
| A10 | Deferred ML sprint | 11+ | `07-machine-learning/` | Planned |

---

## 6. Sources

Fixed list. The source plan's own warning applies: reaching for an additional source "to be
sure you understood" is a procrastination signal — go back to the code.

| Topic | Source |
| --- | --- |
| Claude API | docs.claude.com |
| Prompt engineering | promptingguide.ai · DeepLearning.AI short course |
| RAG | DeepLearning.AI "Building and Evaluating Advanced RAG" · Activeloop RAG course |
| Embeddings | Hugging Face Sentence Transformers docs |
| Vector DB | Qdrant docs (primary) · ChromaDB docs (comparison week) |
| FastAPI | fastapi.tiangolo.com/tutorial — mostly already covered |
| Docker | docker-curriculum.com |
| Agents | Hugging Face Agents Course (free, certificate) |
| LangGraph | official docs |
| MCP | modelcontextprotocol.io |
| Evaluation | docs.ragas.io |
| Observability | langfuse.com/docs (self-host free) |
| Testing | pytest docs — fixtures and mocking only |

**Books, in order:** *AI Engineering* (Chip Huyen, 2025) — read fully, one chapter per phase,
after building · *The LLM Engineering Handbook* — weeks 7–8 · *Designing ML Systems* /
*Designing Data-Intensive Applications* — post-employment.

Full annotated list: [`docs/reference/books-and-sources.md`](../reference/books-and-sources.md)

---

## 7. Technical English

Not a separate subject. A byproduct of how the work is done.

- All code, comments, commits, PRs, docs, and personal notes in English from day one.
- 3×/week, 30–45 min: watch a tech talk untranslated · read an article and summarize it in
  writing · record yourself explaining your project for 2 minutes.
- Weeks 7–8: mock interviews in English.
- Tools: Grammarly, DeepL (for checking phrasing, not wholesale translation).

---

## 8. Execution rules

1. **Stuck > 45 minutes → move on.** Log it in `mistakes.md`, return later.
2. **Docs while building**, never after.
3. **Commit daily**, minimum.
4. **Last hour of each day = review**, not new material.
5. **Reaching for another source "to be sure" = procrastination.** Return to the code.
6. **Every source studied produces an artifact** in `docs/learning/source-summaries/`.
7. **`current-focus.md` is updated weekly.** A staleness test in
   `tests/repo-structure/validate.ps1` fails the suite after 8 days — the tracking layer went
   five weeks stale under the previous plan, so this is enforced rather than trusted.
8. **The amended governing rule** ([ADR-0006](../decisions/0006-adopt-master-ai-engineering-curriculum.md)): curriculum content is allowed but must be production-focused and anchored to DevMate; the repo keeps at least one running service. If the curriculum displaces Build time for more than a week, the moratorium returns.

---

## 9. Related documents

| Document | Role |
| --- | --- |
| [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md) | Why this plan is active |
| [ADR-0005](../decisions/0005-vector-db-qdrant-over-chromadb.md) | Qdrant vs. Chroma |
| [`master-roadmap.md`](master-roadmap.md) | Long track — not active |
| [`milestones.md`](milestones.md) | A1–A10 detail |
| [`progress-dashboard.md`](progress-dashboard.md) | Weekly status |
| [`../tracking/current-focus.md`](../tracking/current-focus.md) | What to do right now |
| [`../reference/`](../reference/) | Decomposed source material |
| [`../plan/archive/`](../plan/archive/) | Original plan documents |

*Last updated: 2026-08-02*
