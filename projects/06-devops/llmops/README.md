# LLMOps — Operating DevMate in Production

The 20% (model, prompt, endpoint) ships the demo. The 80% below keeps it
alive: prompt versioning, eval-gated releases, tracing, cost control, and
rollback. This guide is that 80%, mapped to DevMate paths. Sources:
current LLMOps practice (prompt registries, eval-gated CI, trace schemas,
per-query cost attribution — researched 2026-09-27) as implemented in weeks
1–7 of the active track.

---

## The Lifecycle (9 Phases)

Prompt management → evaluation pipelines → tracing → guardrails → deployment
gates → monitoring → cost control → incident response → governance/audit.
Each phase depends on the previous: skipping versioning makes incidents
undebuggable; skipping evals makes quality invisible. The phases are not
checkboxes.

## 1. Prompt Registry (Version Prompts Like Code)

Prompts live versioned in git (`devmate/src/devmate/llm/prompts/`, registry
in `prompts/registry.py`), never as inline strings. Every trace carries
`prompt.version`; every change goes through review plus the eval gate below.
Rollback is one step: point the registry at the previous version. A prompt
edit that nobody can attribute to a version is an incident without a cause.

| Tool | Fits DevMate? | Note |
|---|---|---|
| Git + in-repo registry | Yes (current) | zero new infra, reviewable diffs |
| Langfuse prompt management | Possible later | if prompts outgrow files |
| Braintrust datasets | Reference | collaborative golden-set curation pattern |

## 2. Eval-Gated Releases (CI Blocks Regressions)

Prompt or model changes merge only when quality gates pass. Adapted to this
repo (prompt paths, pytest harness):

```yaml
name: Prompt Evaluation
on:
  pull_request:
    paths:
      - 'projects/04-ai-engineering/devmate/src/devmate/llm/prompts/**'
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest evaluations/ -q   # golden set + metric floors
```

Below threshold: no merge, no debates, no subjective reviews. The gate
covers recall@k floors, faithfulness floors, and a prompt-change cost diff
(an edit tripling output tokens fails before merge, not after the invoice).

## 3. Trace Schema (What Every Call Records)

One trace per request, correlated end to end. Fields (matching
`devmate/src/devmate/obs/tracing.py`): request id, tenant, input, final
prompt + `prompt.version`, model id, retrieval set (chunk ids + scores),
tool calls, token counts, per-stage latency, $ cost, guardrail verdicts,
output. Redact raw PII at the boundary (hashes only, per the safety-identifier
rule). Full retention on errors and refusals; tail-based sampling on routine
successes to bound storage.

## 4. Cost Control (Spend as a Signal)

Per-query cost thresholds with alerts (not month-end surprises); attribution
by tenant and feature, not just by model; semantic-cache hit rate as a
cost lever with its own dashboard; schema validation before caching (never
cache malformed outputs — it amplifies errors while looking like savings).
Retry loops get budgets and circuit breakers: one unchecked loop erases a
quarter of careful optimization overnight.

## 5. Monitoring (SLOs, Not Vibes)

p95 latency with SLO alerts; faithfulness trendline with weekly human-sampled
points; tool-call error rate; hallucination-rate sampling protocol (define,
sample, judge, track over time). Slice every dashboard by model and prompt
version — global averages hide single-version regressions. Alert on silent
degradation (quality drift at flat error rates), not just on fires.

## 6. Incident Response (Runbooks, Not Heroics)

Paging on quality/latency/cost breaches with runbooks per alert: which
dashboard, which trace query, which rollback (prompt version first, image tag
second, provider-region third). Every incident ends in `failure-modes.md`
with cause class and the gate that would have caught it. Postmortems without
new gates are storytelling.

## 7. Red-Team Schedule (Adversarial, Recurring)

Prompt-injection payloads from the OWASP LLM list, rerun on a schedule (not
once in week 7 and forgotten): new guardrail versions, new model versions,
and new tools each re-trigger the suite. Track block-rate over time; a
dropping rate on a static suite means the suite rotted, not that attacks
stopped. Adversarial prompt sanity tests also gate any week-11 model change.

## 8. Governance (Audit-Ready by Default)

Version records for models, prompts, and eval snapshots; approval tags on
production promotions (automated gates may pass low-risk changes to staging;
humans approve production); data-retention policy stated in weeks, with the
storage bill to prove it's real. If an auditor asks what answered a user in
March, the answer is a trace id away.

## Tool Landscape (2026)

| Need | DevMate pick | Worth knowing |
|---|---|---|
| Tracing + prompts | Langfuse (self-host free) | Arize Phoenix for local RAG debugging |
| Eval datasets | RAGAS + golden JSONL | Braintrust for collaborative curation |
| Experiment tracking | Cost ledger + Langfuse | MLflow for full lifecycle (overkill here) |
| Gateway/cost caps | Hand-rolled budgets | Portkey/Helicone for multi-provider routing |
| Registry | Git + code | MLflow model registry at enterprise scale |

Picks stand until a measured pain says otherwise. New tools arrive via ADR,
never via enthusiasm.
