# Lecture 01: The LLMOps Lifecycle — Operating DevMate in Production

## Topic Overview

Shipping an LLM feature is the easy half. The hard half is running it: versioning prompts so a change is reviewable, gating releases on measured quality instead of vibes, tracing every request so an incident has a cause, controlling cost before the invoice arrives, and rolling back in a defined order when reality disagrees with the eval. This lecture teaches the nine-phase LLMOps lifecycle as an engineering discipline, grounded in DevMate — the real LLM system in this repository. Every phase is tied to a DevMate path, a real command, or a measured number, and where the repository has a gap between its documented target design and its current state, this lecture says so rather than pretending.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Basic Python, an understanding of what an LLM API call is, familiarity with CI concepts; the Docker containerization lecture is helpful but not required

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Map** the nine LLMOps lifecycle phases and explain why each depends on the one before it
2. **Version** prompts like code with a registry, and explain why git-in-repo beats a spreadsheet
3. **Gate** prompt and model changes in CI on recall floors, faithfulness floors, and cost diffs
4. **Design** a trace schema that records enough to answer "why did this request cost $0.12 and cite the wrong file"
5. **Apply** guardrails at the input and output boundaries with a defined action vocabulary
6. **Slice** monitoring dashboards by model and prompt version so a single-version regression cannot hide in a global average
7. **Budget** per-query cost, attribute spend to tenants and features, and use semantic caching as a cost lever safely
8. **Run** an incident response process with a fixed rollback order and a postmortem that produces a new gate
9. **Schedule** recurring red-team suites against prompt injection, and keep them from rotting
10. **Audit** a prompt registry mechanically, and estimate query cost against a budget, using only the Python standard library

---

## Key Concepts

### 1. The Nine Phases

The LLMOps lifecycle is nine phases in dependency order. Each phase assumes the one before it exists; skipping one does not remove the work, it converts the work into an incident later.

```text
1. Prompt registry ──► 2. Eval-gated releases ──► 3. Trace schema
         │                      │                       │
         ▼                      ▼                       ▼
4. Guardrails           5. Deployment gates        6. Monitoring
         │                      │                       │
         ▼                      ▼                       ▼
7. Cost control ◄──────── 8. Incident response ◄── 9. Governance / audit
```

The dependency logic, stated plainly:

| If you skip... | ...you get |
|---|---|
| Prompt versioning | Incidents with no cause: a behavior changed and nothing records what changed |
| Eval gates | Quality invisible: regressions merge because nobody can measure them |
| Tracing | Undebuggable production: you cannot answer what a specific request did |
| Guardrails | An injection payload in week 7 becomes a public incident in week 8 |
| Cost control | A month-end invoice surprise, usually from one unchecked retry loop |
| Incident response | Heroics instead of runbooks; the fix lives in one person's head |
| Governance | An auditor question you cannot answer: "what answered our users in March?" |

DevMate's own track README (`projects/06-devops/llmops/README.md`) states the same order and the same dependency rule. The phases are not checkboxes to complete once; they are disciplines that must hold continuously.

**FACT vs general practice.** Throughout this lecture, FACT means verified in this repository at a specific path. General practice means current industry consensus, not yet implemented here. The distinction matters because DevMate is mid-lifecycle: the tracing, cost, guardrail, and eval layers are real code; the file-based prompt registry is a documented target that does not exist on disk yet (section 2 explains exactly what does exist).

**Where each phase lands on the 10-week track** (`docs/roadmap/active-track-10-week.md`):

| Phase | Track week | DevMate artifact |
|---|---|---|
| 1. Prompt registry | Week 1 | `llm/prompts/` planned; `PromptTemplate` schema + golden-case pins shipped |
| 2. Eval-gated releases | Weeks 2-3 | `eval/run_ragas.py`, CI floors at Hit@5 1.0 / MRR 0.70 |
| 3. Trace schema | Week 1 | `obs/tracing.py` + optional Langfuse export |
| 4. Guardrails | Week 7 | `guards/guardrails.py` (injection, PII, length, extraction) |
| 5. Deployment gates | Week 4 | CI stages: lint → type → test → eval; human prod approval |
| 6. Monitoring | Week 7 | span-derived metrics; dashboards sliced by model + version |
| 7. Cost control | Week 1, hardened week 7 | `obs/cost.py`, `cache/semantic_cache.py`, fallback chain |
| 8. Incident response | Week 7 | `docs/failure-modes.md`, rollback order, regression tests |
| 9. Governance | Continuous | ADRs, versioned golden sets, eval reports in git |

### 2. Prompt Registry and Versioning

A prompt is production code. It deserves the same treatment: review before merge, an immutable version identifier, a rollback path, and an audit trail. The mechanism is a prompt registry — a machine-readable index of every prompt, its version, and whether it is gated by evaluation.

**Where prompts should live (target design).** The track README and the 10-week roadmap both point at `projects/04-ai-engineering/devmate/src/devmate/llm/prompts/` with a registry in `prompts/registry.py`. **FACT: that directory does not exist today.** The `llm/` package contains exactly three files: `client.py`, `schemas.py`, and `__init__.py`. Citing a path that is not on disk is how documentation rots; the honest statement is that the registry is a planned deliverable.

**What does exist (all FACT):**

| Artifact | Path | What it proves |
|---|---|---|
| `PromptTemplate` schema | `projects/04-ai-engineering/devmate/src/devmate/llm/schemas.py:179` | The contract: every template has `name`, `version`, `template`, `variables`, `description` |
| RAG system prompt | `projects/04-ai-engineering/devmate/src/devmate/retrieve/rag.py:45` | Today's reality: an inline string constant, `RAG_SYSTEM_PROMPT`, with no version field |
| Prompt golden cases | `evaluations/prompts/golden-cases/devmate.jsonl` | Ten cases, each pinned to `prompt_id: devmate.rag.answer` and `prompt_version: 1.0.0` |
| Golden-set validator | `projects/04-ai-engineering/devmate/src/devmate/eval/validate_prompt_golden.py` | Offline gate: exactly 10 cases, unique ids, `prompt_id` must equal `devmate.rag.answer` |

The golden cases already implement the versioning discipline at the consumption end: every case names the prompt version it was written against. When a prompt's behavior changes intentionally, the case's `prompt_version` bumps and a regression file is recorded (per the maintenance rules in `evaluations/prompts/golden-cases/devmate-README.md`). The missing piece is the supply end — the versioned files and the registry that `client.py` would resolve at runtime.

**Git-in-repo vs Langfuse vs Braintrust.** Three viable homes for a prompt registry:

| Tool | Fit for DevMate | Tradeoff |
|---|---|---|
| Git + in-repo registry | Current plan | Zero new infra; diffs are reviewable; rollback is a git revert |
| Langfuse prompt management | Possible later | UI and version history for free; adds a service dependency at runtime |
| Braintrust datasets | Reference pattern | Collaborative golden-set curation; heavier than this stage warrants |

The rule that decides it: **new tools arrive via ADR, never via enthusiasm.** A measured pain — prompts outgrowing files, non-engineers editing prompts daily — justifies the migration. Nothing observed today does.

**Why an inline string fails every requirement.** `RAG_SYSTEM_PROMPT` in `rag.py` is a working prompt with no version, no registry entry, and no eval gate on changes to it. Editing those five guideline lines changes production behavior for every `devmate ask` call, and nothing in a trace will say which version of the text produced a given answer. That is the exact failure the registry exists to prevent: an edit nobody can attribute to a version is an incident without a cause.

### 3. Eval-Gated Releases

An eval gate is a CI check that blocks a merge when measured quality drops below a floor. The floor is not a vibe; it is a number recorded next to the gate.

**The real DevMate gate (FACT).** `.github/workflows/ci.yml:71-77` runs, on every pull request:

```bash
python -m devmate.eval.run_ragas --mode offline --no-report \
  --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70
```

The harness (`projects/04-ai-engineering/devmate/src/devmate/eval/run_ragas.py`) exits 1 when Hit@5 falls below 1.0 or MRR below 0.70. Below threshold: no merge, no debates, no subjective reviews. The same command runs locally inside the DevMate gate documented in the repo's `AGENTS.md`.

**What the floors mean.** Hit@5 is the fraction of golden cases whose expected source appears in the top-5 retrieved chunks. MRR (mean reciprocal rank) rewards ranking the right chunk first: a hit at rank 1 scores 1.0, at rank 2 scores 0.5, a miss scores 0.0. Hit@5 1.0 says "every case's answer is reachable in five looks." MRR 0.70 says "the right answer is usually near the top, not buried at rank 4."

**The trap the offline floor hides (FACT, ADR-0009).** The CI floor is satisfied by *offline fixture scoring*, not live retrieval. `docs/decisions/0009-fix-indexing-scope-before-chunk-tuning.md` records the measured gap:

| Metric | Offline (fixtures) | Live (real index, 2026-10-14) |
|---|---|---|
| Hit@5 | 1.000 | 0.900 |
| MRR | 1.000 | 0.820 |

The offline number was never a measurement of the index; the harness itself labels fixture mode as such. The live run found two real defects: `pyproject.toml` absent from the index entirely, and `devmate.egg-info/` build artifacts competing with source code at the top of results. The lesson generalizes: **a gate is only as honest as the thing it measures.** ADR-0009's decision — fix indexing scope, re-baseline, then compare chunkers — is eval-gate discipline applied to RAG, and the follow-up (a live gate at the re-baselined number) is the same discipline applied forward.

**The gate covers three regressions:**

1. **Retrieval floors** — Hit@5 and MRR, as above.
2. **Answer-property floors** — the ten prompt golden cases carry `expected_properties` (`must_be_grounded_in_context`, `must_cite_sources`, `must_not_invent_api`, `forbidden_phrases`) that catch a generator inventing APIs or dropping citations even when retrieval is perfect.
3. **Prompt-change cost diffs** — a prompt edit that triples output tokens should fail before merge, not after the invoice. This third leg is general practice; DevMate's harness has the token and cost plumbing (`obs/cost.py`) but does not yet diff cost in CI. Do not cite it as implemented.

### 4. Trace Schema

One trace per request, correlated end to end. The trace is the unit of debugging in an LLM system: when a user reports a bad answer, you start from the request id and walk the spans.

**What DevMate records (FACT).** `projects/04-ai-engineering/devmate/src/devmate/obs/tracing.py` defines `Span` and `Trace` dataclasses with: `trace_id`, `span_id`, `parent_span_id`, `name`, `start_time`, `end_time`, `duration_ms`, `attributes` (free-form key/value), `events`, `status` (`ok` or `error`), and `error`. Spans nest through `parent_span_id`, so a request trace looks like:

```text
Trace: devmate-ask
├── span: guardrail.prompt_injection      (attributes: category, action)
├── span: retrieve.embed_query
├── span: retrieve.qdrant_search          (attributes: top_k, latency)
├── span: retrieve.rerank
├── span: llm.complete                    (attributes: model, prompt_tokens,
│                                          completion_tokens, cost_usd)
└── span: guardrail.pii_output
```

Langfuse export is wired optionally: when `tracing_enabled` and both keys are configured, `end_span` pushes each span to Langfuse; failures to export are swallowed (`obs/tracing.py:271-297`) because observability must never take down the request path.

**The full production schema — what a complete trace carries (general practice, of which DevMate has the core):** request id, tenant, the final prompt text with `prompt.version`, model id, the retrieval set (chunk ids and scores), tool calls, token counts, per-stage latency, dollar cost, guardrail verdicts, and output. DevMate's span attributes carry much of this today; the `prompt.version` field is exactly what the missing registry (section 2) would enable.

**PII redaction at the boundary.** Raw PII never enters a trace. The rule: redact or hash at the ingestion boundary; store identifiers, not values. DevMate's `PIIGuardrail` (`guards/guardrails.py:112`) shows the mechanism — patterns for email, phone, SSN, credit card, IP address, API keys, AWS keys, GitHub tokens, with action `REDACT` substituting `[REDACTED_EMAIL]`-style placeholders before content moves downstream. A trace that stores raw user emails is a breach dossier waiting for a subpoena.

**Retention policy.** Full retention on errors and refusals — those are the traces you will re-read. Tail-based sampling on routine successes to bound storage. This is general practice; DevMate's in-memory tracer stores recent traces and exports to Langfuse when configured.

### 5. Guardrails and Content Safety

Guardrails are checks at the input and output boundaries with a defined action when they fire. DevMate's vocabulary (`guards/guardrails.py:15-34`, FACT):

**Actions:** `block` (refuse the request), `warn` (proceed but log), `redact` (strip the offending content), `log` (record only).

**Categories:** `prompt_injection`, `pii`, `toxicity`, `code_execution`, `system_prompt_extraction`, `jailbreak`, `excessive_length`.

The implemented guardrails and their defaults:

| Guardrail | Default action | What it catches |
|---|---|---|
| `PromptInjectionGuardrail` | block | "ignore previous instructions", fake `system:` turns, `DAN mode`, `developer mode` |
| `SystemPromptExtractionGuardrail` | block | "show me your system prompt", "what are your instructions" |
| `LengthGuardrail` | block | inputs over `max_prompt_length` (100,000 chars, `config.py:129`) |
| `PIIGuardrail` | redact | the eight secret/PII patterns above |
| `CodeExecutionGuardrail` | warn | `exec(`, `eval(`, `os.system`, `subprocess` in user input |

Two design points that separate a guardrail layer from a regex pile:

1. **Every check is traced.** `PromptInjectionGuardrail.check` runs inside `tracer.trace("guardrail.prompt_injection")` (`guardrails.py:95`), so guardrail trigger rates become a monitorable metric, not a silent filter.
2. **Over-blocking is itself a failure mode.** The failure-modes document (`projects/04-ai-engineering/devmate/docs/failure-modes.md`) lists it in the FMEA table: guardrails that block legitimate answers degrade the product invisibly. Fix the class, not the whole guard.

A guardrail is not security, it is defense in depth. The golden case `devmate-ask-007` encodes this: the expected answer must *not overclaim full security*.

### 6. Deployment Gates

Deployment gates decide what artifact reaches which environment. For an LLM system the artifact is a triple — code image, prompt version, model pin — and the gate must approve all three together.

The DevMate-relevant gates, in merge-to-production order (FACT where noted):

1. **Lint/type/test gate** — ruff, ruff format, mypy, pytest (CI, verified green in `plan.md`).
2. **Eval gate** — the Hit@5 1.0 / MRR 0.70 floors (CI, `ci.yml:71-77`).
3. **Golden-set schema gate** — `devmate.eval.validate_prompt_golden` ensures the ten cases stay structurally valid.
4. **Prompt/model-change gate** — any PR touching `prompts/**` should trigger the eval suite; the roadmap's LLMOps README sketches this workflow. Today the trigger path is aspirational because `prompts/` does not exist; the harness it would call is real.
5. **Human approval for production** — automated gates may pass low-risk changes to staging; humans approve production promotions. This is governance (phase 9) intersecting deployment.

The ordering rule: **fail leftmost.** The cheapest gate that can catch a defect is the one closest to the edit. A prompt typo caught by the registry validator costs a second; the same typo caught by a production incident costs a rollback, a postmortem, and user trust.

The full promotion pipeline, gates in order:

```text
edit ──► lint/type gate ──► unit tests ──► eval gate (Hit@5, MRR)
                                              │
                              below floor ────┴───► block merge
                                              │
                                           at floor
                                              ▼
                                    staging (automated)
                                              │
                                     human approval
                                              ▼
                                    production (pinned
                                    model + prompt version)
```

### 7. Monitoring

Monitoring an LLM system means watching quality and cost the way traditional services watch latency and error rate — with SLOs, not vibes.

**The metrics that matter (general practice, mapped to DevMate's plumbing):**

| Metric | Source in DevMate | Alert condition |
|---|---|---|
| p95 latency | `Span.duration_ms` per stage | SLO breach (e.g. p95 > 8s) |
| Faithfulness trendline | eval harness + weekly human samples | trend drops over N days at flat error rate |
| Tool-call error rate | agent spans with `status=error` | error rate above threshold |
| Guardrail trigger rate | `guardrail.*` spans | spike (attack) or drop (guard disabled?) |
| Cost per request | `CostRecord.cost_usd` | over per-query budget |
| Cache hit rate | semantic cache metrics | hit rate collapse (cache broken or queries novel) |

**Slice by model and prompt version.** A global average quality number hides a single-version regression: if prompt v1.2 is perfect and v1.3 is broken, and traffic splits 50/50, the average looks "slightly off" while half your users are getting bad answers. Every dashboard slice should carry `model` and `prompt_version` dimensions. This requires exactly the `prompt.version` attribute the trace schema (section 4) and the registry (section 2) provide — the phases compose.

**Alert on silent degradation.** The dangerous failure class in `failure-modes.md` is the *silent* one: no exception, no failed request, wrong or ungrounded answer. A quality drift at flat error rates is the signature. If your only alerts fire on 5xx, you will learn about a faithfulness collapse from a user, not a pager.

### 8. Cost Control

Spend is a signal. Treating it as a monthly accounting chore forfeits the cheapest early warning you have: a per-query cost that doubles after a prompt edit is a regression even if every eval still passes.

**What DevMate implements (FACT).** `projects/04-ai-engineering/devmate/src/devmate/obs/cost.py` maintains `MODEL_PRICING` per million tokens — for example `gpt-4o` at (5.00, 15.00), `claude-3-5-haiku-20241022` at (0.80, 4.00) for input and output — and a thread-safe `CostTracker` that records every call (`provider`, `model`, token counts, `latency_ms`, `cost_usd`, `request_id`) and aggregates summaries by model and by provider. `estimate_cost()` computes a hypothetical call's price without issuing it. This is the attribution backbone: cost per model, per provider, per request id.

**The cost control stack (what to build on that backbone):**

1. **Per-query budgets with alerts.** Set a ceiling per request (say $0.05 for an interactive `devmate ask`); alert when actuals cross it. Month-end surprises are the failure mode this eliminates.
2. **Attribution by tenant and feature,** not just by model. "Claude cost $400" is accounting; "the summarize-repo feature cost $350 across 3 tenants" is actionable.
3. **Semantic cache as a cost lever.** DevMate's `SemanticCache` (`src/devmate/cache/semantic_cache.py`, FACT) stores responses keyed by model plus query, matched by cosine similarity at threshold 0.85 (`config.py:126`) with a 3600-second TTL. Every hit is a free LLM call. The trap: **never cache malformed or unvalidated outputs** — a cached error amplifies across every future similar query while the dashboard shows rising "savings."
4. **Retry loops get budgets and circuit breakers.** A retry policy without a cap, pointed at an expensive model, erases a quarter of careful optimization overnight. A circuit breaker stops calling a failing provider after N failures and fails fast until a half-open probe succeeds.

The worked numbers: the exercise for this lecture implements `estimate_cost` against DevMate's own price table and flags budget breaches with codes COST001 (per-query) and COST002 (monthly projection), using the same per-million-token arithmetic as `cost.py:110-112`.

### 9. Incident Response

When quality, latency, or cost breaches an SLO, someone gets paged and follows a runbook. Runbooks, not heroics.

**The rollback order (general practice, stated in the DevMate LLMOps README):**

```text
1. Prompt version   ← cheapest, fastest, most common fix
2. Image tag        ← code regression the eval gate missed
3. Provider region  ← provider-side outage or degradation
```

The order is deliberate. A prompt rollback is a registry pointer change — seconds, no rebuild, and it reverses the most frequent class of regression (a prompt edit). An image rollback is minutes and reverses code. A region failover is last because it is the most disruptive and addresses infra, not your changes. DevMate's golden-set maintenance rule reinforces the first lever: when a prompt version changes behavior, the version bumps and the old behavior remains addressable — rollback is pointing at the previous version, not reconstructing it from chat logs.

**Every incident ends in a failure-modes entry.** The taxonomy in `failure-modes.md` (FACT) classifies each failure as transient, permanent, partial, or silent, and the FMEA-lite table records detection, blast radius, and recovery for each component. The doc already contains one real postmortem: long questions caused Ollama HTTP 500s because the retrieved-context prompt exceeded `qwen2.5-coder:7b`'s default context window; the fix was `rag_context_char_budget` (8000 chars, `config.py:114`) plus `ollama_num_ctx` 8192, with regression tests. That is the standard: **postmortems without a new gate or a new test are storytelling.**

### 10. Red-Team Schedule

A red-team suite is a corpus of adversarial inputs — OWASP LLM prompt-injection payloads, jailbreaks, extraction attempts — run against the system on a schedule. The critical word is *schedule*. A suite run once and forgotten decays: new guardrail versions, new model versions, and new tools each change the threat surface, and a static suite stops measuring it.

The discipline:

1. **Source payloads from the OWASP LLM top-10** (prompt injection, jailbreak, sensitive information disclosure, and the rest). Do not invent threats from imagination when a maintained list exists.
2. **Rerun on every relevant change:** new guardrail version, new model pin, new tool exposed to the agent. DevMate's week-7 track deliverable requires an OWASP injection payload actually blocked with evidence (`docs/roadmap/active-track-10-week.md`).
3. **Track block-rate over time.** A dropping block-rate on a static suite means the suite rotted or a regression landed — investigate either way. An always-100% block-rate on an evolving system usually means the suite stopped generating novel cases.
4. **Adversarial sanity tests gate model changes.** A model swap re-scores the suite before merge, same as any other eval.

DevMate's `PromptInjectionGuardrail` patterns are the current defense; the red-team suite is the measurement of that defense. Defense without measurement is an assumption.

### 11. Governance and Audit

Governance is making every production answer reconstructible after the fact. The auditor's question is concrete: "What answered a user in March?" The acceptable answer is a trace id.

The minimum viable audit trail:

| Record | Where it lives | Enables |
|---|---|---|
| Model version pins | deployment config / client settings | reproduce which model served a date range |
| Prompt versions | registry (target) + golden-case pins (FACT) | reproduce the exact instruction text |
| Eval snapshots | `evaluations/rag/reports/`, golden sets in git | prove what quality bar a release met |
| Approval tags on promotions | CI + human sign-off records | show production changes were authorized |
| Retention policy | stated in weeks, with a storage bill to prove it | answer data-deletion and retention questions |

DevMate already has two of five in strong shape: golden sets and eval reports are versioned in git (`evaluations/prompts/golden-cases/`, `evaluations/rag/`), and every ADR in `docs/decisions/` is itself an audit artifact — ADR-0009 records who decided, when, with which measured numbers, and what would have to be restated. The prompt-version record strengthens once the registry lands.

**Tool landscape (2026, from the track README).** Langfuse for tracing and prompts (self-hosted free tier), RAGAS plus golden JSONL for eval datasets, a cost ledger for experiment tracking, hand-rolled budgets for cost caps, git plus code as the registry. The picks stand until a measured pain says otherwise.

---

## Code Examples

### Example 1: The Real Eval Gate, Local and CI

The exact command CI runs, runnable locally with no API key:

```bash
# From projects/04-ai-engineering/devmate/ with the project venv active:
python -m devmate.eval.run_ragas --mode offline --no-report \
  --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70
```

What each flag enforces:

| Flag | Effect |
|---|---|
| `--mode offline` | score recorded fixtures; no network, no key (default mode) |
| `--no-report` | print the metrics table; skip writing a report file |
| `--fail-under-hit-at-5 1.0` | exit 1 if Hit@5 < 1.0 |
| `--fail-under-mrr 0.70` | exit 1 if MRR < 0.70 |

The same invocation appears in `.github/workflows/ci.yml:76-77`. A prompt change that breaks retrieval relative to the recorded baseline cannot merge. Remember ADR-0009's caveat: offline 1.0 is fixture satisfaction, not live truth; the live gate is a planned follow-up.

### Example 2: A Versioned Prompt File and Registry Entry

The target format the missing `prompts/` directory would hold — frontmatter carries the version contract that `PromptTemplate` (`llm/schemas.py:179`) already defines:

```markdown
---
name: devmate.rag.answer
version: 1.0.0
eval_gate: true
variables: [context, question]
description: Grounded answer prompt for the RAG path
---
You are a helpful AI assistant that answers questions based on the provided context.

Guidelines:
1. Use ONLY the information provided in the context to answer the question
2. If the context doesn't contain enough information, say so honestly
3. Cite your sources using [1], [2], etc. corresponding to the context chunks
4. Be concise but thorough

Context:
{context}

Answer the user's question based on the above context.
```

And the registry entry that makes it discoverable and auditable:

```python
REGISTRY = {
    "devmate.rag.answer": {
        "version": "1.0.0",
        "eval_gate": True,  # CI runs the golden set on every change
        "path": "prompts/rag_answer.md",
    },
}
```

The body is DevMate's actual `RAG_SYSTEM_PROMPT` text from `retrieve/rag.py:45-57` — the content is real; the packaging (file, frontmatter, registry) is the deliverable that does not exist yet. The exercise for this lecture audits exactly this contract: files without registry entries, entries without files, missing versions, missing eval-gate flags.

### Example 3: Per-Query Cost Arithmetic

The same formula `cost.py:110-112` uses, worked with DevMate's real price table. `gpt-4o-mini` is priced at ($0.15 in, $0.60 out) per million tokens:

```python
def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    input_per_m, output_per_m = MODEL_PRICING[model]
    return (prompt_tokens / 1_000_000) * input_per_m + (
        completion_tokens / 1_000_000
    ) * output_per_m


# A typical grounded RAG answer: ~2500 input tokens (system prompt +
# retrieved context under the 8000-char budget) + ~350 output tokens.
per_query = estimate_cost("gpt-4o-mini", 2500, 350)  # $0.000585
monthly = per_query * 20_000  # $11.70 at 20k queries
```

Compare against a budget before shipping, not after:

```python
PER_QUERY_BUDGET = 0.01  # $0.01 interactive ceiling
MONTHLY_BUDGET = 50.00  # $50 at 20k queries/month

assert per_query <= PER_QUERY_BUDGET  # passes with 17x headroom
assert monthly <= MONTHLY_BUDGET  # passes with ~4x headroom
```

Now the regression case that a cost gate catches: swapping to `claude-3-opus-20240229` ($15 in, $75 out per M) with a longer 12k-token context and 2k output costs $0.33 per query — 33x the interactive budget, and $6,600/month at the same volume. Every quality eval could still pass. Only the cost gate fails the change. That is why cost is a first-class gate, not a dashboard curiosity.

### Example 4: Recording a Request the Way the Trace Schema Demands

DevMate's tracer (`obs/tracing.py`) already provides the span API; the discipline is attaching the attributes the schema requires. A sketch of one `devmate ask` request:

```python
from devmate.obs.tracing import tracer
from devmate.obs.cost import cost_tracker, TokenUsage

with tracer.trace("devmate.ask", request_id=req_id, tenant=tenant) as root:
    root.set_attribute("prompt_version", "1.0.0")  # from the registry, once it exists

    with tracer.trace("guardrail.prompt_injection") as span:
        verdict = await injection_guard.check(user_text)
        span.set_attribute("triggered", verdict.triggered)
        span.set_attribute("action", str(verdict.action))

    with tracer.trace("retrieve.qdrant_search") as span:
        hits = await retriever.search(user_text, top_k=settings.rag_top_k)
        span.set_attribute("top_k", settings.rag_top_k)
        span.set_attribute("chunk_ids", [h.id for h in hits[:5]])

    with tracer.trace("llm.complete", model=model_id) as span:
        answer, usage = await llm.complete(messages)
        span.set_attribute("prompt_tokens", usage.prompt_tokens)
        span.set_attribute("completion_tokens", usage.completion_tokens)
        usd = cost_tracker.record_usage(
            provider="anthropic",
            model=model_id,
            usage=TokenUsage(**usage.to_dict()),
            latency_ms=span.duration_ms(),
            request_id=req_id,
        )
        span.set_attribute("cost_usd", usd)

    root.set_attribute("guardrail_verdicts", "clean")
```

Three properties make this schema-compliant rather than merely logged: the request id appears on the root and on every cost record; the structured attributes (`prompt_version`, `chunk_ids`, `cost_usd`) are queryable fields, not prose; and PII never enters the span because the guardrail ran first. Swap the inline `prompt_version` for a registry lookup and the loop from section 2 closes.

---

## Common Mistakes to Avoid

### 1. Editing Prompts as Inline Strings

```python
# ❌ BAD: no version, no registry, untraceable change
RAG_SYSTEM_PROMPT = """You are a helpful assistant..."""

# ✅ GOOD: versioned file resolved through a registry; the trace
# records which version answered this request
# (target design — prompts/rag_answer.md + registry entry, Example 2)
```

### 2. Celebrating an Offline Eval Score That Never Measured Anything

```bash
# ❌ BAD: Hit@5 1.000 from fixture mode, quoted as if it were retrieval quality
python -m devmate.eval.run_ragas --mode offline   # fixtures, not the index

# ✅ GOOD: know which mode produced your number, and cite both
# offline (fixtures): Hit@5 1.000   |   live (real index): Hit@5 0.900
# (ADR-0009's measured gap — the lesson, not a hypothetical)
```

### 3. Storing Raw PII in Traces

```python
# ❌ BAD: the trace warehouse now holds a searchable database of user emails
span.set_attribute("user_email", "ahmed@example.com")

# ✅ GOOD: redact or hash at the boundary; the PII guardrail's
# REDACT action substitutes placeholders before content moves downstream
span.set_attribute("user_id_hash", sha256(email)[:16])
```

### 4. Caching Unvalidated Model Outputs

```python
# ❌ BAD: a malformed or ungrounded answer becomes immortal and
# amplifies across every future similar query while the
# dashboard reports rising "savings"
cache.store(query, raw_llm_output)

# ✅ GOOD: schema-validate and screen for refusals before caching;
# a cache hit must be a response you would ship again
if is_valid(answer) and not is_refusal(answer):
    cache.store(query, answer)
```

### 5. Retrying Without Budgets or Circuit Breakers

```python
# ❌ BAD: one provider outage becomes a month of unplanned spend
for attempt in range(20):
    cost += call_expensive_model(prompt)

# ✅ GOOD: cap attempts, cap spend, and open the circuit after
# consecutive failures so you fail fast instead of failing expensively
```

### 6. Writing a Postmortem That Changes Nothing

An incident write-up that ends with "we rolled back and monitored" but adds no gate, no test, and no alert guarantees the same incident recurs. The DevMate standard is the `failure-modes.md` entry: taxonomy class, detection, blast radius, recovery — and for the context-window incident, a named regression test (`tests/unit/test_rag_context_budget.py`). If the next person cannot point to the new gate, the postmortem is incomplete.

### 7. Swapping the Model Without Re-Gating

```text
# ❌ BAD: change the model pin in config, ship it, discover three
# regressions from users — the new model parses the prompt
# differently, the red-team suite was tuned on the old model, and
# token accounting shifted

# ✅ GOOD: a model change is a release like any other —
# re-run the golden set, re-run the red-team suite, re-estimate
# cost against the budget with the new pricing, then merge with
# the eval snapshot attached to the PR
```

The track README states the rule directly: adversarial prompt sanity tests gate any model change. The model is half the (model, prompt, endpoint) deployable unit; it gets half the gates.

---

## Best Practices

1. **Version every prompt**; every trace records which version answered; rollback is a registry pointer
2. **Gate merges on measured floors** — retrieval, answer properties, and (when wired) cost diffs
3. **Know which mode produced every number** — offline fixtures and live measurements are different facts
4. **Design the trace schema before the incident,** not during it; request id, prompt version, tokens, cost, verdicts
5. **Redact PII at the boundary**; traces store hashes and placeholders, never raw secrets
6. **Give every guardrail a category and an action**, and monitor trigger rates per category
7. **Slice every quality and cost dashboard by model and prompt version**
8. **Alert on silent degradation** — quality drift at flat error rates — not only on 5xx
9. **Set per-query cost budgets before launch**; attribute spend by tenant and feature, not just model
10. **Never cache outputs you have not validated**; a cache hit must be a shippable answer
11. **Cap retries with budgets and circuit breakers**; an uncapped loop is a billing incident
12. **Follow the rollback order:** prompt version, then image tag, then provider region
13. **Run the red-team suite on a schedule** and on every guardrail, model, or tool change
14. **End every incident with a new gate or test**; a postmortem without a gate is storytelling
15. **Introduce new tools via ADR**, with a measured pain as the justification

---

## Practice Exercises

### Exercise 1: Audit the Golden Set Against Its Own Contract
Run the golden-set validator (`python -m devmate.eval.validate_prompt_golden` from the DevMate venv) and read each rule it enforces. Then write one paragraph explaining how "exactly 10 cases, `prompt_id` pinned, unique ids" functions as a miniature prompt registry even though the actual registry does not exist yet.

### Exercise 2: Run the Eval Gate and Break It
Run the offline eval gate locally with its real floors. Then deliberately lower a floor below the measured value (say `--fail-under-mrr 0.95`) and confirm the harness exits 1 with the `FAIL: MRR ...` message. Restore the floors. The point is feeling the gate reject, not just watching it pass.

### Exercise 3: Design the Missing Registry
Write the `prompts/` layout DevMate needs: one file per prompt with frontmatter (`name`, `version`, `eval_gate`, `variables`), plus a `registry.py` exposing a lookup by name. Migrate `RAG_SYSTEM_PROMPT` from `retrieve/rag.py` into `prompts/rag_answer.md` at version 1.0.0. Note every call site the migration touches.

### Exercise 4: Cost a Prompt Change Before Merging It
Using the price table in `obs/cost.py`, estimate the current RAG path (~2500 input, ~350 output tokens) on two models. Compute the per-query and monthly (20k queries) cost of each. Decide whether the swap fits a $0.01 per-query and $50 monthly budget, and write the diff you would put in the PR description.

### Exercise 5: Write the Runbook You Would Page Yourself
Pick one alert — guardrail trigger rate spike — and write the runbook: which dashboard to open, which trace query isolates the pattern, which guardrail category is firing, and which of the three rollback levers applies. Keep it under one page. Then check it against the `failure-modes.md` FMEA row for guards and note what your runbook missed.

---

## Summary

LLMOps is the 80% that keeps an LLM system alive after the demo works. The durable takeaways:

1. **The nine phases are dependency-ordered, not a menu.** Registry before evals before traces before gates; skipping one converts work into an incident.
2. **Prompts are production code.** Version them, gate them, record the version on every trace. DevMate's schema and golden cases are ready; the file registry is the missing deliverable, and this lecture refuses to pretend otherwise.
3. **A gate is only as honest as its measurement.** ADR-0009's offline-1.000 versus live-0.900 gap is the canonical lesson: cite which mode produced your number.
4. **Traces make incidents debuggable; guardrails make attacks visible;** both must record structured attributes, not prose logs.
5. **Cost is a first-class signal.** Per-query budgets, tenant attribution, validated-only caching, and capped retries turn the invoice into a dashboard.
6. **Rollback order is prompt, image, region.** Postmortems end in gates. Red teams run on a schedule. Auditors get a trace id.

**Next lecture:** Evaluation pipelines in depth — building golden sets, choosing metrics (recall@k, MRR, faithfulness), calibrating LLM judges against human labels, and wiring the results into the CI gate you met here.
