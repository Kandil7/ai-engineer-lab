# Model Serving 02: Self-Hosted Models

## Topic Overview

Self-hosting a model trades a per-token API bill for infrastructure work: GPUs, model
loading, quantization, serving, and monitoring become your responsibility. For the right
workload that trade is excellent, because the marginal cost of a request drops to
electricity and the data never leaves your machine. For the wrong workload it is a way
to spend a week of engineering to save a few dollars a month.

This lecture covers the tradeoff, the two main tools (Ollama for development, vLLM for
production), how to budget VRAM before you launch, and why both tools expose an
OpenAI-compatible API. The compatibility is the quiet superpower: application code does
not need to change when you move from a hosted API to a local model, or between local
tools, so the choice stays reversible.

On the workstation in this repo, self-hosting is also how the intelligence stays local
and private, which is a first-class reason to do it even when the cost math is close.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain when self-hosting beats a hosted API and when it does not.
2. Choose between Ollama (development) and vLLM (production).
3. Compute a VRAM budget and decide whether a model fits.
4. Serve a model behind an OpenAI-compatible API.
5. Measure local latency instead of assuming it.
6. Keep the application provider-agnostic so the choice is reversible.

## Prerequisites

- Model Serving 01 (choosing a model) for which model you are trying to serve.
- A mental model of GPU memory (weights plus runtime overhead).

---

## 1. The Self-Hosting Tradeoff

### What you gain

- **No per-token cost.** After the hardware, each request is nearly free.
- **Privacy.** Data never leaves the machine; no third party sees prompts or outputs.
- **Offline operation.** The system works without a network.
- **Control.** You pick the model, the quantization, and the version, and nothing
  changes under you overnight.

### What you pay

- **Hardware.** A GPU with enough VRAM for the model plus runtime.
- **Operational work.** Model loading, serving, quantization, upgrades, monitoring.
- **Throughput ceiling.** One 16 GB GPU serves far fewer concurrent users than a hosted
  fleet, so self-hosting does not scale by default.

### When it is worth it

Self-hosting wins for high volume (the API cost dominates), privacy-sensitive workloads,
offline requirements, and experimentation where the round trip to a hosted API is the
bottleneck. It loses for low volume (the API is cheaper than any hardware amortization)
and for bursty production scale that a managed endpoint absorbs better.

## 2. Ollama: The Development Path

### What it is

Ollama is the simplest path to a running local model: it downloads a model, handles
quantization and memory, and exposes a server. You get a model running in minutes.

### Strengths and limits

- **Strengths:** trivial setup, good for development, single-user use, quick experiments.
- **Limits:** it is not built for high concurrency; there is no continuous batching, so
  multiple simultaneous users degrade toward serialization.

Ollama is the right tool for building and testing the application on your machine. It is
usually the wrong tool for serving many users at once.

## 3. vLLM: The Production Path

### What it is

vLLM is a high-throughput inference server built around paged attention and continuous
batching. It keeps the GPU busy across requests by batching them dynamically, which is
what lets a single GPU serve many concurrent users well.

### Strengths and limits

- **Strengths:** high throughput, continuous batching, production-oriented metrics.
- **Limits:** more to configure, and it is still bounded by the GPU's memory and compute.

The rule of thumb: Ollama for development, vLLM for production. Both expose the same
API surface, so the application does not care which one is running underneath.

## 4. The VRAM Budget

### The formula for weights

Weights scale linearly with parameter count and precision:

```python
def vram_budget(params_b: float, quant_bits: int) -> float:
    """Weights at the given precision, in GB."""
    return params_b * quant_bits / 8
```

A 7B model at 4-bit is about 3.5 GB; at 16-bit it is about 14 GB. A 13B model at 4-bit
is about 6.5 GB. This is the number people forget to compute before they try to launch.

### Weights are not the whole budget

The real budget is weights plus KV cache plus activations plus runtime overhead. The KV
cache grows with context length and concurrency, so a model that "fits" at rest can OOM
under a long context or many parallel requests. Budget for the tail, not the empty case.

### Fitting on 16 GB

On a 16 GB card, a 7B model at 4-bit leaves generous room for the KV cache; the same
model at 16-bit barely fits and leaves little for context. The quantization choice is
therefore a function of the target context length and concurrency, not only of quality.

```python
mem_16bit = vram_budget(7.0, 16)  # 14.0 GB, barely fits
assert fits(mem_16bit, 16.0)
```

## 5. The OpenAI-Compatible API

### Why compatibility matters

Both Ollama and vLLM expose an OpenAI-compatible HTTP API, so the same client code works
against a hosted provider, Ollama, or vLLM. Only the base URL and the model name change:

```python
assert openai_compatible("http://localhost:11434/v1")  # Ollama
assert openai_compatible("http://localhost:8000/v1")  # vLLM
```

### The reversibility payoff

Because the interface is identical, moving from a hosted API to self-hosting, or back,
is a configuration change rather than a rewrite. This keeps the model-serving choice
reversible, which matters because the tradeoff flips as volume and requirements change.

### The lesson

Never bind the application to a provider-specific SDK in the core path. Wrap the client
behind a thin interface so the provider is a detail. This is the same provider-agnostic
discipline the pipeline needs for graceful degradation (Model Serving 03, section 4).

## 6. Measuring Local Latency

### Measure, do not assume

Local inference is not automatically faster than a hosted API; it is a different
latency profile. A hosted frontier model may still outperform a small local one in time
to first token. Measure time to first token, tokens per second, and total time for your
actual prompts and hardware.

### What to record

Record the numbers in the same place as the model choice. "7B at 4-bit, TTFT 0.4s, 40
tokens/sec on the RTX 5000" is a fact you can plan around; "it felt fast" is not.

### The break-even point

The self-hosting tradeoff has a break-even volume where the amortized hardware cost falls
below the API bill. Knowing your volume and your per-token API cost lets you place that
point and decide with numbers.

## 7. When Not to Self-Host

- **Low volume.** The API is cheaper than any hardware amortization.
- **Frontier capability needed.** A model that does not fit your GPU is not a
  self-hosting candidate.
- **Bursty, elastic load.** Managed endpoints scale up and down; a single GPU does not.
- **No GPU operations capacity.** Unless someone can keep the server healthy, a managed
  endpoint is lower risk.

Choosing not to self-host is a legitimate, often correct decision, and it belongs in the
same ADR framework as choosing to.

## Real-World Application

- Running a 7B model with Ollama during DevMate development, then the same weights under
  vLLM for a load test.
- Serving an Arabic embedding model locally for Athar so corpus text never leaves the
  machine.
- Computing the VRAM budget with the exercise's `vram_budget` before downloading a model.
- Switching the client's base URL from a hosted API to `localhost` without touching the
  pipeline code.

## Common Mistakes

1. **Self-hosting for a low-volume workload.** The API is cheaper.
2. **No VRAM budget.** The model OOMs at startup or under load.
3. **Ollama for production concurrency.** It lacks continuous batching.
4. **No latency measurement.** "Local" is assumed to be fast.
5. **Locking the app to one provider.** The choice stops being reversible.
6. **Budgeting only weights.** The KV cache and activations push a "fitting" model into
   OOM.
7. **Ignoring the operational cost.** Someone has to keep the server healthy.

## Key Takeaways

1. Self-hosting trades per-token cost for infrastructure and a throughput ceiling; it
   wins at high volume, for privacy, and offline.
2. Ollama for development, vLLM for production; both expose an OpenAI-compatible API.
3. The VRAM budget is weights plus KV cache plus activations plus overhead, and the
   quantization choice follows from it.
4. The OpenAI-compatible interface keeps the provider a reversible detail.
5. Measure local latency and record it; do not assume self-hosting is faster.

## Self-Check Questions

1. Give one workload where self-hosting beats a hosted API and one where it does not.
2. Compute the weight memory for a 13B model at 4-bit. Why is the real budget larger?
3. Why is Ollama usually wrong for production concurrency?
4. What does the OpenAI-compatible API buy you, and why does it matter for reversibility?
5. Name two reasons a team might correctly decide not to self-host.

## Further Reading / Connections

- Model Serving 01 (choosing a model) — the choice this lecture deploys.
- Model Serving 03 (inference serving) — batching, monitoring, and fallbacks on top of a
  self-hosted server.
- Model Serving 04 (HF Inference SDK) — the managed alternative, for comparison.
- `docs/reference/llm-production-architecture.md` — cost and inference sections.
