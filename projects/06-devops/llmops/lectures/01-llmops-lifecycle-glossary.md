# Glossary: The LLMOps Lifecycle

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| LLMOps | The operational discipline for running LLM systems in production | Extends MLOps with prompt, eval, and safety concerns |
| Prompt Registry | Machine-readable index of every prompt, its version, and its gates | Rollback is pointing at the previous version |
| Prompt Version | Immutable identifier for one state of a prompt's text | Every trace should carry it |
| Golden Set | Curated cases of question → expected behavior used by evals | The contract a release must satisfy |
| Eval Gate | CI check that blocks a merge below a metric floor | No merge below threshold, no debates |
| Hit@5 | Fraction of cases whose expected source appears in top-5 retrieval | DevMate CI floor: 1.0 |
| MRR | Mean reciprocal rank; rewards ranking the right chunk first | DevMate CI floor: 0.70 |
| Faithfulness | Degree to which an answer stays grounded in retrieved context | Trend it; alert on drift at flat error rates |
| Trace | One record per request, correlated end to end across stages | The unit of LLM debugging |
| Span | One timed stage inside a trace (retrieve, guardrail, LLM call) | Nest via parent_span_id |
| Trace Schema | The fixed field set every trace records | Request id, prompt version, tokens, cost, verdicts |
| Guardrail | Check at input/output boundaries with a defined action | Actions: block, warn, redact, log |
| Prompt Injection | Adversarial input that tries to override system instructions | Defended by patterns; measured by red-team suites |
| PII Redaction | Replacing personal data with placeholders or hashes at the boundary | Traces never store raw PII |
| Per-Query Budget | Dollar ceiling for one request's LLM cost | Alert on breach; catch it before the invoice |
| Semantic Cache | Cache keyed by embedding similarity, not exact string match | Never cache unvalidated outputs |
| Circuit Breaker | Switch that fails fast after N consecutive provider failures | Prevents retry storms from becoming bills |
| SLO | Service Level Objective; a numeric target for latency or quality | Monitoring fires on objective breach, not vibes |
| Silent Degradation | Quality drop with no error-rate signal | The most dangerous LLM failure class |
| Runbook | Step-by-step response for one alert class | Dashboard, trace query, rollback lever |
| Rollback Order | Fixed sequence for reverting: prompt → image → region | Cheapest and most common lever first |
| Red-Team Suite | Recurring corpus of adversarial payloads (OWASP LLM top-10) | Rerun on every guardrail, model, or tool change |
| Eval Gate Flag | Registry field marking a prompt as CI-gated | A missing flag is silent ungovernance |
| Governance | Records making every production answer reconstructible | Auditor question gets a trace id answer |

---

## Detailed Definitions

### LLMOps

**Definition:** The engineering practices for operating large-language-model systems in production: prompt versioning, evaluation-gated releases, tracing, guardrails, deployment gates, monitoring, cost control, incident response, and governance. It extends MLOps (models, data, training pipelines) with the concerns unique to stochastic text generation: prompts as deployable artifacts, non-deterministic outputs requiring property-based evals, and safety surfaces that traditional software does not have.

**Example:**
```text
DevMate's nine-phase lifecycle (projects/06-devops/llmops/README.md):
prompt management → evaluation pipelines → tracing → guardrails →
deployment gates → monitoring → cost control → incident response →
governance/audit. Each phase depends on the previous.
```

**Related Terms:** MLOps, Prompt Registry, Eval Gate, Trace Schema

**Key Facts:**
- LLMOps treats the (model, prompt, endpoint) triple as the deployable unit, not the model alone
- Skipping a phase does not remove the work; it converts the work into an incident
- The DevMate track implements phases 2-4 and 7 in real code; the file-based registry (phase 1) is a planned deliverable

---

### Prompt Registry

**Definition:** A machine-readable index mapping each prompt's stable name to its current version, file path, and gating metadata (whether CI evaluates changes to it). The registry is the single source of truth for what text the system will run, and the pointer that rollback moves.

**Example:**
```python
# Target design for DevMate (not yet on disk — llm/prompts/ does not exist)
REGISTRY = {
    "devmate.rag.answer": {
        "version": "1.0.0",
        "eval_gate": True,
        "path": "prompts/rag_answer.md",
    },
}

# What exists today instead: an inline constant with no version field
# projects/04-ai-engineering/devmate/src/devmate/retrieve/rag.py:45
RAG_SYSTEM_PROMPT = """You are a helpful AI assistant..."""
```

**Related Terms:** Prompt Version, Eval Gate Flag, Git-in-Repo, Langfuse

**Key Facts:**
- DevMate's `PromptTemplate` schema (`llm/schemas.py:179`) already requires `name` and `version` — the contract exists before the files do
- Golden cases pin `prompt_id` + `prompt_version`, so consumption-side versioning is live even without the registry
- Git-in-repo is the current plan: reviewable diffs, zero new infra, rollback by revert
- New registry tools (Langfuse, MLflow) arrive via ADR, not enthusiasm

---

### Prompt Version

**Definition:** An immutable identifier (typically semantic, like `1.0.0`) naming one exact state of a prompt's text. Editing the text in any behavioral way requires a new version; old versions remain addressable for rollback and for interpreting historical traces.

**Example:**
```jsonl
# evaluations/prompts/golden-cases/devmate.jsonl — every case pins a version
{"id": "devmate-ask-001", "prompt_id": "devmate.rag.answer",
 "prompt_version": "1.0.0", "question": "What does the chunker's _generate_id return..."}
```

**Related Terms:** Prompt Registry, Trace, Rollback Order

**Key Facts:**
- A trace without `prompt.version` cannot answer "which instruction text produced this output"
- The golden-set maintenance rule: never edit behavior in place; bump `prompt_version` and record a regression file
- Semantic versioning works for prompts too: patch for typos, minor for additive guidance, major for behavior changes

---

### Golden Set

**Definition:** A curated collection of cases, each pairing an input (question) with the expected behavior — expected context, expected answer, and checkable properties. Eval harnesses score a system against the golden set; CI gates compare scores to recorded floors.

**Example:**
```text
evaluations/prompts/golden-cases/devmate.jsonl   — 10 prompt cases
evaluations/rag/datasets/devmate-golden.jsonl    — retrieval golden set
```

Each DevMate prompt case carries `expected_properties` such as
`must_be_grounded_in_context`, `must_cite_sources`, `must_not_invent_api`,
and `forbidden_phrases` — machine-checkable answer contracts.

**Related Terms:** Eval Gate, Faithfulness, Expected Properties

**Key Facts:**
- The golden set is the contract: a case whose expected source is absent from the index fails for a reason no retrieval change can fix (ADR-0009)
- Ten cases is a starting contract, not a ceiling; grow the set as failure modes appear
- Keep gold answers short — long expected answers hide retrieval failures

---

### Eval Gate

**Definition:** A continuous-integration check that computes evaluation metrics for a change and exits non-zero when any metric falls below its recorded floor, preventing the merge. The floor is a number committed next to the gate, not a judgment call in review.

**Example:**
```bash
# The real DevMate gate — .github/workflows/ci.yml:71-77
python -m devmate.eval.run_ragas --mode offline --no-report \
  --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70
# Exits 1 (blocks merge) when Hit@5 < 1.0 or MRR < 0.70
```

**Related Terms:** Hit@5, MRR, Golden Set, Offline Eval

**Key Facts:**
- Below threshold: no merge, no debates, no subjective reviews
- A complete LLM gate covers three regressions: retrieval floors, answer-property floors, and prompt-change cost diffs
- A gate is only as honest as what it measures — DevMate's offline gate scores fixtures; a live gate at the re-baselined number is a named follow-up (ADR-0009)

---

### Hit@5

**Definition:** The fraction of golden cases whose expected source document appears among the top five retrieved results. It measures retrieval reachability: can the system find the right evidence within five looks?

**Example:**
```text
10 golden cases, 9 have their expected source in the top-5 → Hit@5 = 0.900
DevMate live baseline 2026-10-14: Hit@5 0.900 (9/10)
DevMate offline fixtures:          Hit@5 1.000 (fixtures, not a measurement)
```

**Related Terms:** MRR, Eval Gate, Golden Set

**Key Facts:**
- DevMate's CI floor is 1.0 on the offline path — every case reachable within five looks
- Hit@5 says nothing about ordering inside the five; that is MRR's job
- A case missing from the index entirely (ADR-0009's `pyproject.toml`) can never contribute to Hit@5 at any k

---

### MRR

**Definition:** Mean Reciprocal Rank — the average of 1/rank for the first correct result across cases. Rank 1 scores 1.0, rank 2 scores 0.5, rank 4 scores 0.25, a miss scores 0.0. It rewards putting the right evidence at the top, which is what the model actually reads.

**Example:**
```text
Ranks of correct result per case: [1, 1, 2, 5, miss]
Reciprocals: 1.0, 1.0, 0.5, 0.2, 0.0
MRR = (1.0 + 1.0 + 0.5 + 0.2 + 0.0) / 5 = 0.54
DevMate CI floor: 0.70
```

**Related Terms:** Hit@5, Eval Gate, Reranking

**Key Facts:**
- MRR is more sensitive than Hit@5 to top-of-list quality — a build artifact at rank 1 costs trust even when Hit@5 passes
- Signal-to-noise at the top matters more than recall at large k (ADR-0009 decision drivers)
- Reranking exists precisely to lift MRR: trade latency for top-of-list precision

---

### Faithfulness

**Definition:** The degree to which a generated answer stays grounded in the retrieved context, introducing no claims the context does not support. Measured by LLM judges or property checks; tracked as a trendline with periodic human calibration.

**Example:**
```jsonl
# The property checks on every DevMate golden case
"expected_properties": {
  "must_be_grounded_in_context": true,
  "must_cite_sources": true,
  "must_not_invent_api": true
}
```

**Related Terms:** Golden Set, Silent Degradation, LLM-as-Judge

**Key Facts:**
- Retrieval metrics can be perfect while the generator invents APIs — answer properties catch what retrieval cannot
- Track faithfulness as a trendline with weekly human-sampled points, not as a one-time number
- An LLM judge used for faithfulness must itself be calibrated against human labels, or you are measuring the judge

---

### Trace

**Definition:** One correlated record per request, containing the hierarchical spans of every stage the request passed through — guardrails, retrieval, reranking, the LLM call — plus request-level metadata. The trace is what you read when a user reports a bad answer.

**Example:**
```text
Trace: devmate-ask (trace_id=...)
├── guardrail.prompt_injection   status=ok
├── retrieve.qdrant_search       attributes: top_k=20
├── retrieve.rerank              attributes: rerank_top_k=5
├── llm.complete                 attributes: model, tokens, cost_usd
└── guardrail.pii                status=ok
```

**Related Terms:** Span, Trace Schema, Request ID

**Key Facts:**
- DevMate's `Trace` and `Span` dataclasses (`obs/tracing.py`) carry trace_id, span_id, parent_span_id, attributes, events, status, error, duration_ms
- Langfuse export is optional and must never block the request path — export failures are swallowed by design
- Full retention on errors and refusals; tail-sample routine successes to bound storage

---

### Span

**Definition:** A single timed stage inside a trace, with a name, start and end timestamps, structured attributes, events, and an ok/error status. Spans nest through `parent_span_id` to mirror the request's real call structure.

**Example:**
```python
# DevMate's tracing API — obs/tracing.py
async with tracer.trace("guardrail.prompt_injection") as span:
    result = await guardrail.check(content)
    span.set_attribute("triggered", result.triggered)
    span.set_attribute("category", str(result.category))
```

**Related Terms:** Trace, Trace Schema, Per-Stage Latency

**Key Facts:**
- Span names become metric series: `guardrail.*` trigger rates, `llm.*` latency percentiles
- An error span records both `status="error"` and the message, so alerts can group by error class
- Duration per span is how you find whether latency lives in retrieval, reranking, or generation

---

### Trace Schema

**Definition:** The fixed contract of fields every trace must record. For an LLM system the production schema is: request id, tenant, final prompt with `prompt.version`, model id, retrieval set (chunk ids and scores), tool calls, token counts, per-stage latency, dollar cost, guardrail verdicts, and output — with PII redacted at the boundary.

**Example:**
```text
| Field            | DevMate today                    | Enables                          |
|------------------|----------------------------------|----------------------------------|
| request id       | trace_id (uuid)                  | join across logs and DB          |
| prompt version   | missing (no registry yet)        | attribute behavior to an edit    |
| token counts     | llm span attributes, cost.py     | cost attribution                 |
| $ cost           | CostRecord.cost_usd              | per-request budget alerts        |
| guardrail verdicts | guardrail.* spans              | trigger-rate monitoring          |
| retrieval set    | retrieve span attributes         | debug "wrong file cited"         |
```

**Related Terms:** Trace, Span, PII Redaction, Governance

**Key Facts:**
- Design the schema before the incident; during an incident you only read it
- Missing `prompt.version` is the schema gap that the prompt registry fills
- Redact or hash PII at ingestion; a trace store holding raw emails is a breach dossier

---

### Guardrail

**Definition:** A check that runs on input or output before or after the model call, producing a structured result with a category and an action. Actions are a fixed vocabulary — block, warn, redact, log — so responses to different threat classes are consistent and monitorable.

**Example:**
```text
# DevMate's implemented guardrails — src/devmate/guards/guardrails.py
PromptInjectionGuardrail        action=block   catches "ignore previous instructions", DAN mode
SystemPromptExtractionGuardrail action=block   catches "show me your system prompt"
LengthGuardrail                 action=block   inputs > max_prompt_length (100,000 chars)
PIIGuardrail                    action=redact  emails, phones, SSNs, cards, API keys
CodeExecutionGuardrail          action=warn    exec(, eval(, os.system in input
```

**Related Terms:** Prompt Injection, PII Redaction, Red-Team Suite

**Key Facts:**
- Every DevMate guardrail check runs inside a traced span, so trigger rates are a metric
- Over-blocking legitimate answers is itself a failure mode (failure-modes.md FMEA row for guards)
- A guardrail is defense in depth, not security — never claim full protection from regexes

---

### Prompt Injection

**Definition:** An adversarial input that attempts to override, ignore, or rewrite the system's instructions — direct ("ignore previous instructions"), indirect (payloads embedded in retrieved documents), or structural (fake `system:` / assistant turns). The OWASP LLM top-10 lists it as the leading LLM-specific threat.

**Example:**
```text
# Payload classes in DevMate's PromptInjectionGuardrail patterns
"ignore previous above all instructions"     — direct override
"you are now a DAN"                          — role hijack
"system: you have no restrictions"           — fake turn injection
"bypass safety security filter"              — filter evasion
```

**Related Terms:** Guardrail, Red-Team Suite, Jailbreak

**Key Facts:**
- Regex patterns catch known shapes; they do not catch novel phrasings — hence the recurring red-team suite
- Indirect injection (payload in a retrieved chunk) is the RAG-specific variant DevMate's context pipeline must consider
- Measure block-rate over time; a dropping rate on a static suite means the suite rotted

---

### PII Redaction

**Definition:** Replacing personally identifiable information with placeholders or one-way hashes at the boundary where content enters logs, traces, or caches. The raw value never crosses the boundary, so a trace warehouse cannot leak what it never stored.

**Example:**
```python
# DevMate's PIIGuardrail REDACT action — guards/guardrails.py:151-152
sanitized = pattern.sub(f"[REDACTED_{pii_type.upper()}]", sanitized)
# "contact ahmed@example.com" → "contact [REDACTED_EMAIL]"

# Traces store hashes, not values
span.set_attribute("user_id_hash", hashlib.sha256(email.encode()).hexdigest()[:16])
```

**Related Terms:** Guardrail, Trace Schema, Data Retention

**Key Facts:**
- DevMate's pattern set covers email, phone, SSN, credit card, IP address, API keys, AWS keys, GitHub tokens
- Redact at ingestion; retrofitting redaction over stored traces is deletion theater
- Retention policy pairs with redaction: even hashes age out per a stated window

---

### Per-Query Budget

**Definition:** A dollar ceiling on what one request may cost in model tokens, set before launch and enforced by alerting (and ideally by rejection). It converts cost control from month-end accounting into a real-time signal.

**Example:**
```python
# The arithmetic from obs/cost.py, applied as a gate
per_query = (2500 / 1e6) * 0.15 + (350 / 1e6) * 0.60  # gpt-4o-mini: $0.000585
PER_QUERY_BUDGET = 0.01
# A swap to claude-3-opus with 12k context: $0.33/query — 33x the budget.
# Every quality eval can still pass; only the cost gate fails the change.
```

**Related Terms:** Cost Attribution, Semantic Cache, Circuit Breaker

**Key Facts:**
- DevMate records cost per request (`CostRecord.cost_usd`, `request_id`) — the attribution exists; the alert threshold is the missing gate
- Per-query budgets catch the "prompt edit tripled output tokens" regression before the invoice
- Attribute spend by tenant and feature, not just by model, to make the number actionable

---

### Semantic Cache

**Definition:** A response cache that returns a stored answer when a new query's embedding is similar enough to a cached query's embedding, rather than requiring exact string equality. Hit rate is a cost lever: every hit is a skipped model call.

**Example:**
```text
# DevMate's SemanticCache — src/devmate/cache/semantic_cache.py
key       = sha256(model + query)
match     = cosine(new_query_embedding, cached_embedding) >= 0.85   # config.py:126
ttl       = 3600 seconds                                             # config.py:125
```

**Related Terms:** Per-Query Budget, Cache Hit Rate, Silent Degradation

**Key Facts:**
- Never cache malformed, ungrounded, or abstained outputs — a cached error amplifies across future similar queries while the dashboard shows savings
- Schema-validate before storing; a cache hit must be an answer you would ship again
- Cache the model identity in the key: a cached answer from a cheaper model must not be served as the expensive model's output

---

### Circuit Breaker

**Definition:** A failure-count switch that stops calling a dependency after N consecutive failures, failing fast until a periodic probe succeeds and closes the breaker. Paired with retry budgets so a failing provider produces bounded failures, not unbounded spend.

**Example:**
```text
State machine (general pattern; wiring into DevMate's fallback chain is planned):
closed   → normal calls; failures increment a counter
open     → calls rejected immediately; no provider spend
half-open→ one probe allowed; success closes, failure re-opens
```

**Related Terms:** Fallback Chain, Retry Budget, Runbook

**Key Facts:**
- Without a breaker, a provider outage plus a retry loop is a billing incident layered on an outage
- DevMate's fallback chain (primary → cheaper/local → cached → graceful error) is the sibling control: the breaker stops the failing leg; the chain keeps the request alive
- The failure-modes taxonomy classes "transient" failures as retry-with-backoff territory — bounded attempts, always

---

### SLO

**Definition:** A Service Level Objective — a numeric target for a user-facing metric (p95 latency under a threshold, error rate under a percentage, faithfulness above a floor) over a window. Monitoring alerts on objective breach rather than on raw anomaly.

**Example:**
```text
SLO examples for an ask-style LLM endpoint:
p95 end-to-end latency   < 8 seconds          (spans: retrieve + llm)
guardrail false-block    < 1% of requests     (guardrail.* spans)
cost per request         < $0.01 p95          (CostRecord.cost_usd)
faithfulness (weekly)    >= 0.9 sampled       (eval harness + human points)
```

**Related Terms:** Silent Degradation, Trace, Monitoring

**Key Facts:**
- Latency SLOs are per-stage diagnosable only if spans exist — an end-to-end number alone cannot localize
- Quality SLOs need sampling protocols: define, sample, judge, track over time
- An SLO without an alert is documentation

---

### Silent Degradation

**Definition:** A quality or cost regression that produces no exception and no error-rate signal — wrong or ungrounded answers, rising spend, drift at flat 5xx rates. The most dangerous failure class in an LLM system because the user discovers it and the dashboard does not.

**Example:**
```text
# failure-modes.md taxonomy (FACT) — the silent class:
"stale index, ungrounded answer, cost overrun | detection metrics + alarm; never silent"

# Real instance: the Ollama context-window bug looked like a provider
# 500 but was a prompt-budget error — silent before the fix, surfaced
# only on long questions (failure-modes.md §5).
```

**Related Terms:** SLO, Faithfulness, Monitoring, Runbook

**Key Facts:**
- If your only alerts fire on 5xx, silent degradation is invisible by construction
- Alert on trendlines: faithfulness drifting down over N days at flat error rate
- Slice by model and prompt version — a global average hides a single-version collapse

---

### Runbook

**Definition:** A written, per-alert-class procedure: which dashboard to open, which trace query isolates the pattern, which rollback lever applies, and who owns the decision. Runbooks replace heroics when the pager fires at an inconvenient hour.

**Example:**
```text
Alert: guardrail trigger-rate spike (prompt_injection category)
1. Dashboard: guardrail.* span rates, sliced by tenant and route
2. Trace query: recent traces with guardrail.prompt_injection triggered=true
3. Classify: novel payload (add to red-team suite) vs over-block (fix the pattern)
4. Lever: if a new guardrail version caused it — roll back the guardrail
   (code/image lever); if traffic-authored — block is working as designed
```

**Related Terms:** Rollback Order, Incident Response, Red-Team Suite

**Key Facts:**
- Every incident ends in `failure-modes.md` with cause class and the gate that would have caught it
- A runbook that names no trace query is a wish
- Test runbooks in game days, not only in production at 3 a.m.

---

### Rollback Order

**Definition:** The fixed sequence for reverting a production regression: prompt version first, image tag second, provider region third. The order is cheapest-first and most-common-cause-first — prompt edits are the frequent regression class and take seconds to reverse via the registry pointer.

**Example:**
```text
Regression: answers got verbose and off-tone after a prompt merge
1. Prompt lever: point registry devmate.rag.answer 1.1.0 → 1.0.0   (seconds)
2. If no prompt change was involved: roll image tag to the previous digest (minutes)
3. If the provider itself is degraded: fail over to another region         (disruptive)
```

**Related Terms:** Prompt Registry, Incident Response, Runbook

**Key Facts:**
- The first lever only exists if prompts are versioned — this is why phase 1 precedes phase 8
- DevMate's golden-set rule (bump versions, keep old behavior addressable) is what makes lever 1 a pointer move
- Every rollback is temporary; it buys time for the fix that ends in a new gate

---

### Red-Team Suite

**Definition:** A recurring corpus of adversarial payloads — sourced from the OWASP LLM top-10 — run against the system on a schedule and after every relevant change (new guardrail version, new model pin, new tool). Block-rate over time is the tracked metric.

**Example:**
```text
Cadence (general practice for DevMate's week-7+ posture):
- Full suite: weekly, and on every guardrail/model/tool change
- Tracked: block-rate by payload class over time
- Regression signal: block-rate drops on a static suite → suite rot or a real regression
- New payloads: every incident contributes the payload that got through
```

**Related Terms:** Prompt Injection, Guardrail, Eval Gate

**Key Facts:**
- Run once and forgotten is the default failure: the threat surface moves, the suite does not
- Adversarial sanity tests gate model swaps the same way golden sets gate prompt edits
- A 100% block-rate that never moves usually means the suite stopped generating novel cases

---

### Governance and Audit

**Definition:** The records and approvals that make every production answer reconstructible after the fact. The concrete test: an auditor asks "what answered a user in March?" and the answer is a trace id, resolved to model version, prompt version, and the eval snapshot the release met.

**Example:**
```text
Minimum audit trail:
model version pins     → deployment config (which model served which dates)
prompt versions        → registry (target) + golden-case pins (live today)
eval snapshots         → evaluations/*/reports/ and golden sets in git
approval tags          → CI green + human sign-off on production promotions
retention policy       → stated in weeks, with the storage bill to prove it
```

**Related Terms:** Trace Schema, Prompt Version, Eval Gate

**Key Facts:**
- DevMate's strongest governance artifacts today are the versioned golden sets and eval reports in git, plus the ADR series in `docs/decisions/`
- Automated gates may pass low-risk changes to staging; humans approve production
- Data-retention policy stated in weeks — a policy without a storage bill is a wish

---

### Offline Eval

**Definition:** An evaluation run that scores recorded fixtures — recorded retrieval top-k, recorded answers — without network access or API keys. Deterministic, CI-safe, and fast; it measures scoring logic and recorded baselines, not live system behavior.

**Example:**
```bash
# DevMate's default eval mode — no key, no network
python -m devmate.eval.run_ragas --mode offline --no-report \
  --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70
# Offline fixture Hit@5: 1.000 — the harness notes this is NOT a live measurement
```

**Related Terms:** Live Eval, Eval Gate, Golden Set

**Key Facts:**
- Offline and live numbers are different facts: ADR-0009 measured offline Hit@5 1.000 against live 0.900
- Offline mode is the honest CI gate when live infra (Qdrant, embeddings) is not guaranteed in the runner
- Always cite which mode produced a number; quoting offline 1.000 as retrieval quality is the classic overclaim

---

### Live Eval

**Definition:** An evaluation run that exercises the real pipeline — live embedding, live retrieval against the actual index, optionally live generation — and scores the results. It measures what users experience; it needs running services and, for generation, a provider key.

**Example:**
```bash
# Live retrieval scoring (needs Qdrant + embeddings; --with-llm needs a key
# and never runs in CI)
python -m devmate.eval.run_ragas --mode live
# Measured baseline 2026-10-14: Hit@5 0.900, MRR 0.820 over the real index
```

**Related Terms:** Offline Eval, Eval Gate, Baseline

**Key Facts:**
- Live mode is how you discover index-scope defects (missing files, polluted rankings) that fixtures cannot see
- A live CI gate should be added at whatever the re-baselined index actually achieves — the threshold recorded next to the gate, not raised to meet the offline number (ADR-0009)
- LLM answer scoring in live mode requires a key and is excluded from default CI

---

## Summary

These terms cover the vocabulary you need to operate an LLM system from prompt edit to production answer and back:

1. **Prompts are versioned deployable artifacts.** The registry, the version field, and the golden-set pins form one contract; rollback is a pointer move.
2. **Gates measure, floors block.** Hit@5, MRR, answer properties, and cost diffs are numbers committed next to CI — and every number cites its mode (offline vs live).
3. **Traces make incidents debuggable.** Request id, prompt version, tokens, cost, and guardrail verdicts are the schema; PII is redacted before it ever lands.
4. **Guardrails defend in depth; red-team suites measure the defense** on a schedule that cannot be forgotten.
5. **Cost is a first-class signal.** Per-query budgets, tenant attribution, validated-only semantic caching, and circuit breakers turn the invoice into a dashboard.
6. **Incidents end in gates.** The rollback order is prompt, image, region; the postmortem's last line is the new test or alert; the auditor's question resolves to a trace id.

**Next:** Lecture 02 covers evaluation pipelines in depth — building golden sets, choosing and calibrating metrics, and wiring live gates at honest baselines.
