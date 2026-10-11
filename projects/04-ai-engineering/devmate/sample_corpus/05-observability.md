# Observability

You cannot operate what you cannot see. DevMate records both traces and cost.

## Tracing

Every model call, retrieval, and cache access runs inside a span. Spans carry
attributes such as the provider, the model, and the latency, and they export to
Langfuse for inspection. A single request produces a tree of spans you can read to
find where time went.

## Cost tracking

The cost ledger records, per request: provider, model, prompt tokens, completion
tokens, total tokens, an estimated cost in dollars, and the latency. From this you
can answer operational questions: what does one request cost, which model is the
most expensive, and where is the spend going.

## Readiness

The `/ready` endpoint reports the state of each dependency (the API, Qdrant, Redis,
and the language model provider). It returns `ready` when all are healthy and
`degraded` otherwise, so an orchestrator knows whether to send traffic.

## Why it matters

A production LLM system fails in ways a plain web service does not: providers rate
limit, streams stall, and costs drift. Traces and a cost ledger turn those into
observable, debuggable facts.
