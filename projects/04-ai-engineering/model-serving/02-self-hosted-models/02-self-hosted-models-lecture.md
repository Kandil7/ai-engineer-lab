# Model Serving 02: Self-Hosted Models

## 🎯 Topic Overview

Self-hosting a model trades API cost for infrastructure work. Ollama and
vLLM are the two main paths. This lecture covers the tradeoff, the tools,
and the discipline of serving locally.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the self-hosting tradeoff
2. Choose between Ollama and vLLM
3. Budget VRAM for a local model
4. Serve a model with an OpenAI-compatible API
5. Measure local inference latency

---

## 1. The Tradeoff

Self-hosting eliminates per-token cost but adds infrastructure: GPU
memory, model loading, serving, and monitoring. The tradeoff is worth it
for high volume, privacy-sensitive, or offline workloads. The roadmap's
exit test: "the self-hosting tradeoff is understood."

## 2. Ollama

Ollama is the simplest path: download a model, run it, get an
OpenAI-compatible API. It handles quantization, memory, and the server.
Good for development and single-user workloads. The roadmap's exit test:
"Ollama is used for local serving."

## 3. vLLM

vLLM is the production path: high-throughput serving with paged attention
and continuous batching. It handles concurrency and throughput. Good for
multi-user production workloads. The roadmap's exit test: "vLLM is used
for production serving."

## 4. VRAM Budget

A local model's size determines whether it fits. A 7B model at 4-bit is
~4 GB; at 16-bit it is ~14 GB. The budget includes weights, KV cache, and
activations. The roadmap's exit test: "the VRAM budget is checked."

## 5. OpenAI-Compatible API

Both tools expose an OpenAI-compatible API. The application code is
identical whether calling OpenAI or a local model — only the base URL
changes. The roadmap's exit test: "the API is OpenAI-compatible."

## Common Mistakes

- Self-hosting for a low-volume workload (API is cheaper).
- No VRAM budget (OOM at startup).
- Ollama for production (no batching).
- No latency measurement.
- Locking the app to one provider.

## Key Takeaways

1. Self-hosting trades cost for infrastructure.
2. Ollama for development; vLLM for production.
3. The VRAM budget decides the model size.
4. The API is OpenAI-compatible.
5. Measure local latency.