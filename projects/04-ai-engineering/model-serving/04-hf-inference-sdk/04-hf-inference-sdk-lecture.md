# Model Serving 04: Hugging Face Inference SDK

## Topic Overview

The Hugging Face Inference SDK calls models hosted on the Hub, either through the shared
free inference API or through dedicated Inference Endpoints. It is the managed middle
ground between calling a frontier API and self-hosting: you get a huge model catalog and
no infrastructure, at the cost of rate limits on the free tier and a per-hour bill on
dedicated endpoints.

This lecture covers the SDK, how to select a model from the Hub by task and language, the
difference between the free tier and Inference Endpoints, and how Hugging Face compares
to self-hosting. The most important discipline it teaches is selection: the Hub hosts
hundreds of thousands of models, and choosing one is a task-and-language filter followed
by a golden-set evaluation, not a popularity contest.

The same provider-agnostic rule from the other serving lectures applies here. The HF SDK
should sit behind the same thin interface as every other provider, so switching between
Hugging Face, a frontier API, and a local model stays a configuration change.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Call the Hugging Face Inference API through the SDK.
2. Select a model from the Hub by task, language, and size.
3. Use Inference Endpoints for production and understand what they add.
4. Handle the free tier's rate limits correctly.
5. Compare Hugging Face against self-hosting on the relevant axes.
6. Keep the application provider-agnostic so the choice is reversible.

## Prerequisites

- Model Serving 01 (choosing a model) for the selection axes.
- Model Serving 02 (self-hosted models) for the comparison baseline.

---

## 1. The SDK

### What it is

The HF Inference SDK wraps the hosted inference API. A model is specified by its Hub ID,
and the SDK handles the HTTP request, authentication, and response parsing:

```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2")
```

### Two backends, one client

The same client can talk to the free inference API (shared capacity, rate limited) or to
a dedicated Inference Endpoint (private capacity, no free-tier limit), depending on how
the client is configured. That makes local development and production use the same code
path with a different endpoint.

### What the SDK does not do

It does not choose the model, evaluate it, or manage the serving. Those remain your
responsibility, which is why the selection and evaluation discipline from Models Serving
01 applies here unchanged.

## 2. Model Selection from the Hub

### Filter by task and language first

The Hub is too large to browse. Filter by task (text-generation, feature-extraction,
and so on) and by language, then pick among the matching candidates. The exercise models
this:

```python
def pick_model(candidates: list[dict], task: str, language: str) -> str:
    """Select from the Hub by task and language."""
    matching = [
        c for c in candidates if c["task"] == task and language in c["languages"]
    ]
    assert matching, "no model matches the task and language"
    return min(matching, key=lambda c: c["size"])["name"]
```

On an Arabic task, the Arabic-capable model is the only match, and the smallest match
wins by default.

### Then evaluate on the golden set

Filtering produces a shortlist, not a winner. Run the shortlist on the golden set with
the same metrics (Model Serving 01) and pick the winner. The Hub's download counts and
likes are a weak prior, not a benchmark.

### Size as a tiebreaker

When two candidates match the task equally well, prefer the smaller one, because smaller
is cheaper and faster everywhere it runs. The exercise's `min(..., key=size)` encodes
that preference.

## 3. Inference Endpoints

### What they add

Inference Endpoints are dedicated, autoscaled deployments of a Hub model. They offer
consistent latency (no sharing with other users) and no free-tier rate limit, and they
scale with load.

### The cost model

They are billed by the hour of the running endpoint, not by the token. That is a
different cost shape from a per-token API and from self-hosting: you pay for uptime, so
the break-even depends on how continuously the endpoint runs.

### The production path

The free API is the development path; Inference Endpoints are the production path. The
same SDK and the same model ID work for both, so moving from one to the other is a
configuration change.

## 4. Free-Tier Limits

### The rate limit

The free inference API has a request rate limit and shared capacity. Exceeding the limit
returns an error (a 429-style rejection):

```python
def free_tier_allows(requests: int, limit: int) -> bool:
    """The free tier has a rate limit; exceeding it returns 429."""
    return requests <= limit
```

```python
assert free_tier_allows(10, 10)
assert not free_tier_allows(11, 10)  # rate limit exceeded
```

### Development versus production

The free tier is fine for development, testing, and low-volume experiments. It is not
fine for production: the rate limit will be hit, the shared capacity makes latency
unpredictable, and the terms are not meant for serving real traffic. Production uses
Inference Endpoints or another dedicated path.

### Handle the limit in code

The client must handle a rate-limit error gracefully: retry with backoff, or fall back
(Model Serving 03). A production system that crashes on a 429 is a production system
that will crash.

## 5. Hugging Face versus Self-Hosting

| Axis | HF Inference (managed) | Self-hosting |
| --- | --- | --- |
| Infrastructure | None | GPU, serving, monitoring |
| Cost shape | Per token (free tier) or per hour (endpoints) | Hardware amortization |
| Model catalog | Huge, one-line access | Whatever fits your GPU |
| Privacy | Data goes to a third party | Data stays local |
| Latency control | Shared (free) or dedicated (endpoints) | Full, bounded by the GPU |
| Scale | Endpoints autoscale | One GPU's ceiling |

### How to decide

Choose managed when you want a large model you cannot run locally, when you have no GPU
operations capacity, or when the load is bursty. Choose self-hosting when privacy,
offline operation, or per-request cost at high volume dominates. The decision belongs in
the same ADR framework as Model Serving 01 and 02, and it can be revisited as volume and
requirements change.

### The pragmatic default

A common pattern uses both: self-host a small model for the common case and fall back to
a managed endpoint for the hard cases. The provider-agnostic interface makes this a
configuration, not a rewrite.

## 6. Provider-Agnostic Wrapping

### The interface

Wrap the HF client behind the same thin interface used for every provider: a
`generate(messages, params) -> response` function that hides the SDK. The application
depends on the interface, not on `InferenceClient`.

### Why it matters

It keeps the choice reversible (switch providers without touching the pipeline), it
makes testing possible (swap in a fake provider), and it makes the fallback chain from
Model Serving 03 trivial to assemble from multiple providers.

### What not to do

Do not sprinkle `InferenceClient` calls through the codebase. That binds the system to
one provider and to one model, and it makes the fallback chain and the provider switch
far more expensive than they need to be.

## 7. Cost and Latency of Managed Endpoints

### Cost

Track cost per useful answer for the managed path as you would for any other (Model
Serving 01). The per-hour billing of an endpoint means idle time is paid time, which
changes the economics versus a per-token API when traffic is spiky.

### Latency

Measure TTFT and tokens per second for the managed endpoint as you would for a local
server. Dedicated endpoints give more consistent latency than the free tier, but
"managed" does not automatically mean "fast"; the numbers decide.

### The comparison to keep

Keep the self-hosting numbers and the managed numbers side by side in the ADR, so the
choice can be re-evaluated with data when volume or requirements change.

## Real-World Application

- Prototyping DevMate against the free inference API, then moving to a dedicated endpoint
  for a load test.
- Selecting an Arabic-capable embedding model from the Hub for Athar's index.
- Handling a 429 from the free tier with a retry and a cached fallback.
- Keeping the provider behind an interface so the same pipeline runs against Hugging
  Face, a frontier API, or a local model.

## Common Mistakes

1. **Using the free tier in production.** Rate limits and shared capacity.
2. **No evaluation of the Hub selection.** A popular model is not a measured one.
3. **Ignoring the rate limit in code.** A 429 crashes the request path.
4. **Binding the app to the HF SDK.** The provider choice stops being reversible.
5. **Assuming managed means fast.** Latency still must be measured.
6. **Not comparing against self-hosting.** The tradeoff is decided without numbers.
7. **Forgetting the per-hour cost of an idle endpoint.** Uptime is billed.

## Key Takeaways

1. The SDK wraps the Inference API; the free tier is for development, Inference Endpoints
   are for production.
2. Select Hub models by task and language, then evaluate the shortlist on the golden set,
   preferring the smaller match.
3. The free tier is rate limited; handle the limit in code and never rely on it in
   production.
4. HF versus self-hosting is a volume, privacy, and latency decision recorded in the ADR.
5. Wrap the provider behind a thin interface so the choice stays reversible and the
   fallback chain is easy to assemble.

## Self-Check Questions

1. What does the HF client do, and what does it explicitly not do?
2. How do you select a model from the Hub, and what decides the final winner?
3. What is the difference between the free inference API and an Inference Endpoint?
4. Give one reason to choose HF Inference over self-hosting and one to choose the reverse.
5. Why should the HF SDK sit behind a thin interface?

## Further Reading / Connections

- Model Serving 01 (choosing a model) — the selection axes applied to the Hub shortlist.
- Model Serving 02 (self-hosted models) — the comparison baseline.
- Model Serving 03 (inference serving) — the fallback chain the provider sits in.
- `docs/reference/books-and-sources.md` — Hugging Face course material.
