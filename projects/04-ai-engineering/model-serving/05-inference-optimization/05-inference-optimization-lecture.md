# Model Serving 05: Inference Optimization

## Topic Overview

A model behind an API is not a finished product; it is a budget problem. Every request spends three currencies at once — latency the user feels, cost the operator pays, and quality the task requires — and the serving stack is where those three are traded against each other deliberately instead of by accident. This lecture is the engine room of the model-serving track: the serving engines and the one idea that makes them fast (PagedAttention), the two phases of generation that behave like different machines (prefill and decode), the batching discipline that decides throughput (continuous batching), the memory structure that dominates the VRAM budget at long context (the KV cache), and the levers that change the trade itself (weight and KV quantization, prefix caching, speculative decoding, structured output, and model routing). The unifying rule is that latency alone is never the objective: you optimize a p95 SLO under a cost ceiling, above a quality floor, and you measure all three on every change. The examples are grounded in the workstation's real constraint — an NVIDIA Quadro RTX 5000 with 16 GB of VRAM (Turing, compute capability 7.5) on a Windows 11 host with WSL2 — and in DevMate, the LLM service in this repository that serves `qwen2.5-coder:7b` through Ollama. Topics 02 and 03 introduced Ollama for development and vLLM for production and sketched the VRAM budget; this lecture goes inside both.

**Duration:** 4-5 hours
**Difficulty:** Advanced
**Prerequisites:** Model Serving 02 (self-hosted models) for the VRAM budget and the Ollama/vLLM split; Model Serving 03 (inference serving) for prefill/decode vocabulary, TTFT, and percentiles; the Reliability lecture (`projects/06-devops/reliability/`) for the timeout/retry/fallback contract that the routing section composes with

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **State** the optimization objective as a p95 latency SLO under a cost ceiling above a quality floor, and refuse single-axis tuning.
2. **Compare** vLLM, SGLang, TGI, and Ollama by what each optimizes, with PagedAttention as vLLM's core idea.
3. **Explain** why prefill is compute-bound and decode is memory-bound, and how that split drives every batching and metric decision.
4. **Choose** between static, dynamic, and continuous batching, and defend continuous batching as the throughput win.
5. **Compute** KV-cache VRAM with `layers x 2 x kv_heads x head_dim x dtype_bytes x seq_len x batch`, and size `max_model_len` and batch against the 16 GB budget.
6. **Select** a quantization format (AWQ, GPTQ, FP8, INT4/INT8, GGUF Q4_K_M) and verify it with a perplexity delta plus a task eval, never by eye.
7. **Predict** when quantization is acceptable and when it is harmful — long-context retrieval, arithmetic, and citation fidelity as the usual fault lines.
8. **Exploit** prefix caching for RAG prompts with shared retrieved context, and explain why a one-byte change invalidates the cache.
9. **Decide** when speculative decoding helps (small batch, predictable tokens) and when it is pure overhead (large batch, high load).
10. **Design** structured output with schema-constrained decoding instead of retry-and-repair, and route requests across small, mid, and strong models with a fallback chain that ends in a degraded state.

---

## Key Concepts

### 1. The Objective: SLO, Cost Ceiling, Quality Floor

Latency is the metric people reach for first, and optimizing it alone is the classic way to ship a fast, cheap, wrong system. A quantized model that answers 30% faster but fails the citation check has not been optimized; it has been broken with extra steps. The objective this lecture optimizes everywhere is a triple constraint:

| Constraint | Shape of the number | Example for an interactive RAG service |
|---|---|---|
| **Latency SLO** | p95 of a user-visible metric | p95 TTFT < 2 s; p95 time-to-last-token < 30 s |
| **Cost ceiling** | Money per unit of work | < $0.02 per 1k output tokens (or GPU-hours/day) |
| **Quality floor** | Task metric that must not drop | Hit@5 >= 1.0, MRR >= 0.70 on the golden set |

Every lever in this lecture moves at least two of the three, usually in opposite directions: quantization cuts cost and latency, spends quality; continuous batching raises throughput, spends per-request latency; speculative decoding cuts decode latency, spends compute. The engineering discipline is to state all three numbers before pulling a lever and to re-measure all three after.

**FACT in this repository:** DevMate's CI already enforces the quality floor half of this triple. `.github/workflows/ci.yml:71-77` runs the offline retrieval gate with `--fail-under-hit-at-5 1.0 --fail-under-mrr 0.70`, so a serving-side change that tanks retrieval quality fails the pipeline even if latency improves. The cost ceiling and the latency SLO are the two numbers this lecture asks you to write down next to that gate.

### 2. Serving Engines and PagedAttention

Topic 02 drew the Ollama-versus-vLLM line; this section fills in the field. Four engines dominate local and self-hosted serving, and each optimizes a different thing:

| Engine | Optimizes for | Core ideas | Right when |
|---|---|---|---|
| **vLLM** | Throughput per GPU | PagedAttention, continuous batching, prefix caching, quantized serving | Many concurrent users on one GPU — the production default |
| **SGLang** | Compound throughput + structured generation | RadixAttention (shared-prefix tree), aggressive schedulers, JSON/grammar gen | Heavy shared prefixes (RAG, multi-turn) and structured outputs |
| **TGI** | Production stability on HF models | Continuous batching, token streaming, metrics, Prometheus | Hugging Face ecosystem shops wanting a supported server |
| **Ollama** | Developer ergonomics | One-command model pulls, GGUF quant management, simple API | Local development, single-user use — not high concurrency |

Topic 02 already established why Ollama is the development path and vLLM the production path; the honest addition is that Ollama has no continuous batching, so concurrent requests degrade toward serialization, which is exactly the property the rest of this lecture exploits in the other engines.

**PagedAttention is vLLM's core idea, and it is an operating-system idea.** The KV cache (section 5) is allocated per token, and naive servers allocate it as one contiguous block per sequence sized to `max_model_len`. That wastes most of the allocation — a 32k-context allocation serving a 500-token chat is 96% empty — and fragmentation stops new sequences from fitting even when total free memory is large. PagedAttention stores the KV cache in fixed-size blocks, like OS pages, and links them per sequence:

```text
 naive contiguous allocation              paged allocation
┌──────────────────────────────┐   seq A: [blk7] → [blk3] → [blk12]
│ seq A: 500 tokens used       │   seq B: [blk1] → [blk9]
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░ │   seq C: [blk5] → [blk2] → [blk8] → [blk4]
│ ░░ 31k tokens wasted ░░░░░░ │
└──────────────────────────────┘   free list: blk0, blk6, blk10, blk11, ...
      one big hole per idle seq        allocate on demand, share, reclaim free
```

The payoff is not a faster attention kernel in isolation; it is that far more sequences fit in the same VRAM, so the engine can keep a much larger live batch — which is where decode throughput comes from. SGLang's RadixAttention extends the same paging intuition from *within* a sequence to *across* sequences: a radix tree over token prefixes lets requests share cached KV for shared prefixes (section 7). The rule for this workstation: on one 16 GB RTX 5000, the engine choice is most of the concurrency ceiling, which is why Topic 02's "Ollama for development, vLLM for production" line is a capacity statement, not a taste statement.

### 3. Prefill and Decode: Two Phases, Two Bottlenecks

Topic 03 named the two phases; this section explains why they behave like different machines, because every batching, caching, and metric decision downstream follows from the split.

| Property | Prefill | Decode |
|---|---|---|
| What it does | Reads the whole prompt, builds the KV cache | Emits one token per step, reads and extends the KV cache |
| Arithmetic shape | Matrix x matrix (many tokens at once) | Matrix x vector (one token at a time) |
| Bound by | Compute (FLOPs) | Memory bandwidth (weights + KV read per step) |
| Scales with | Prompt length, squared-ish in attention | Sequence length (KV read) and batch size |
| User-visible metric | TTFT | tokens/sec, total time |

In decode, every single generated token requires reading the model's entire weight matrix once per sequence in the batch. That is why a decode step's time barely depends on whether the answer is the first token or the thousandth, and why decode is memory-bound: the GPU spends its time moving weights, not multiplying. Batching amortizes that read across sequences — eight sequences decode nearly as fast as one, because the weights are read once and applied to eight token-vectors. This is the single most important economic fact in local inference: **decode throughput scales with batch size almost for free until compute or KV memory runs out, while per-request latency does not improve.**

Prefill is the opposite: it is compute-bound, it is what TTFT is made of, and it scales with prompt length. A 6,000-token RAG context makes prefill dominate TTFT while leaving decode rate untouched — the exact behavior Topic 03 asked you to recognize in the metrics. The modern bridge between the phases is chunked prefill (vLLM and SGLang both support it): split a long prefill into chunks and interleave them with decode steps of other requests, so one user's huge context cannot stall everyone else's token stream. You do not implement chunked prefill yourself; you choose an engine that has it and you read your TTFT percentiles knowing a long-context request is a prefill event.

### 4. Batching: Static, Dynamic, Continuous

Batching groups independent sequences so one GPU step serves many requests. The three regimes differ in *when* requests are admitted to the batch, and that timing is the whole story:

| Scheme | Admission rule | Strength | Failure mode |
|---|---|---|---|
| **Static batching** | Wait until `batch_size` requests are queued, then run all to completion | Simple; maximal GPU utilization at high load | At low load, request 1 waits for requests 2..N; p95 latency is set by the fill time |
| **Dynamic batching** | Start when a timer fires or a max size is reached | Bounds the fill wait | Still batch-shaped: requests that arrive mid-batch wait for the next batch |
| **Continuous batching** (iteration-level scheduling) | Admit a new request at every decode step; a finished request's slot is refilled immediately | Throughput stays high across all load levels; no fill wait | Scheduling complexity in the engine, not in your application |

The reason continuous batching is the throughput win is the decode loop itself. Generation proceeds one token at a time per sequence, so at every iteration the engine can check: did any sequence just emit EOS (free its slot)? did any new request just arrive (allocate KV blocks and join the batch)? A static batch of 16 holds every slot until the *slowest* sequence finishes; a continuous batch recycles slots the instant they free, so the live batch size tracks actual demand instead of a fixed group. Empirically this is the difference Topic 02 gestured at: the same 7B model serves a handful of users under a non-batching server and dozens under vLLM, because the engine — not the weights — sets the ceiling.

```text
 static batch of 4 (one slow request holds everyone)
 req A ──████████░░░░░░░░░░
 req B ──████░░░░░░░░░░░░░░     █ = decoding   ░ = finished, slot wasted
 req C ──██████████░░░░░░░░
 req D ──██████████████████     D holds the batch open to the end

 continuous batching (iteration-level)
 step  t1   t2   t3   t4   t5   t6
 live  A,B  A,B,C A,B,C A,C,D A,C,D C,D,E ...
       └─ B done → slot refilled with C at the next step; no slot idles
```

Two rules follow. First, **the application never batches** (Topic 03's rule, now with the mechanism): send individual requests and let the engine schedule them; application-level batching reintroduces the fill wait the engine removed. Second, **batch size is a latency trade, not a free knob**: raising the max batch raises aggregate throughput and raises per-request latency, because each sequence waits behind more decode work per step. Raise it against a latency SLO (section 12), never against throughput alone — the exercise's INF005 rule exists because a batch raise with no SLO is an unmeasured trade.

**Micro-batching** is the related pattern outside the GPU: group requests at the API or queue layer into small units for downstream calls (embeddings, rerankers) that accept lists. It smooths bursts and matches list-shaped APIs; it does not replace the engine's continuous batching, and it must be bounded (the Reliability lecture's backpressure rule applies to any micro-batch queue).

### 5. The KV Cache: Sizing Math and VRAM Dominance

The KV cache is the per-layer, per-token memory of keys and values that attention needs so the model never recomputes the prompt. It is created during prefill, extended by one position per decode step, and it is the reason a model that "fits" at rest OOMs under long context or many parallel requests. The sizing formula is exact arithmetic, not a rule of thumb:

```python
def kv_cache_bytes(
    layers: int,  # transformer blocks, e.g. 28 for qwen2.5-coder:7b
    kv_heads: int,  # KV heads after grouped-query attention, e.g. 4
    head_dim: int,  # e.g. 128
    dtype_bytes: float,  # 2.0 for fp16/bf16, 1.0 for fp8/int8 KV
    seq_len: int,  # tokens of context per sequence
    batch: int,  # concurrent sequences
) -> int:
    # the 2 is K and V
    return layers * 2 * kv_heads * head_dim * dtype_bytes * seq_len * batch
```

Worked on this workstation's real local model: `qwen2.5-coder:7b` (the DevMate default, `projects/04-ai-engineering/devmate/src/devmate/config.py:50`) has 28 layers, 4 KV heads (grouped-query attention already shrinks the cache 7x versus full multi-head), and head dimension 128. At fp16 (2 bytes) one token costs `28 x 2 x 4 x 128 x 2 = 57,344` bytes — 56 KiB per token per sequence:

| seq_len (per sequence) | batch 1 | batch 4 | batch 8 |
|---|---|---|---|
| 2,048 | 0.11 GB | 0.44 GB | 0.89 GB |
| 8,192 (DevMate's `ollama_num_ctx`, `config.py:122`) | 0.44 GB | 1.76 GB | 3.52 GB |
| 32,768 | 1.76 GB | 7.04 GB | 14.07 GB |

Read the last cell against the 16 GB card: fp16 KV for eight 32k sequences is 14 GB — more than the model's own int4 weights, with nothing left for the weights, activations, or the CUDA context. This is what "KV cache dominates VRAM at long context" means numerically, and it is why Topic 02's budget formula (weights + KV + activations + overhead) must include the KV term at the *planned batch and context*, not at 1x1.

Three consequences, each a configuration decision:

1. **`max_model_len` is a budget line, not a wish.** The engine must be able to allocate KV up to that length for every sequence it may admit. Doubling `max_model_len` doubles worst-case KV; on 16 GB with a 7B model the sane interactive range is roughly 4k-16k tokens of context with small batches, not 128k.
2. **KV dtype is a separate lever from weight dtype.** Serving with fp16 weights does not force fp16 KV: vLLM's `--kv-cache-dtype fp8` (or int8) halves every cell in the table above at a quality cost that is usually milder than weight quantization — but it is still a quantization and still gets verified (section 6).
3. **Grouped-query attention is already paid for.** Models with MHA (one KV head per query head) multiply every cell by 7 versus this model's GQA; when comparing candidate models for a long-context task on 16 GB, the KV head count is as load-bearing as the parameter count.

### 6. Quantization: Weight-Only, Activation, and Verification

Quantization stores the model's numbers in fewer bits. The first split that matters is *what* gets quantized:

| Family | What is quantized | Formats you will meet | Hardware note (RTX 5000, sm_75) |
|---|---|---|---|
| **Weight-only** | Weights; compute still in fp16 | AWQ, GPTQ, GGUF Q4_K_M / Q5_K_M, INT4/INT8 checkpoints | Works everywhere; dequantize-on-the-fly kernels |
| **W8A8 / activation** | Weights *and* activations | INT8 smooth-quant; FP8 | Turing has no native FP8 path — FP8 is a Hopper/Ada lever, not this card's |
| **KV-cache quant** | The KV cache only | fp8/int8 KV cache in vLLM/SGLang | The independent second lever from section 5 |

Weight-only 4-bit (AWQ, GPTQ, GGUF's Q4_K_M — the family Ollama's `:7b` tags default into) is the reason a 7B model is a 3.5-4 GB download instead of a 14 GB one, and on a 16 GB card it is often the difference between "serves with 8k context and batch 4" and "barely loads." The accuracy cost is real but not uniform, and that non-uniformity is the entire point of this section.

**Verification is a protocol, not a vibe.** "It looks fine" is how a 4-bit regression reaches production. The two-gate protocol:

1. **Perplexity delta on held-out text.** Same tokenizer, same corpus, baseline (fp16/bf16 or a known-good quant) versus candidate. A delta around 0.1-0.5 nats is typical for a good 4-bit quant; a delta of 2+ means the checkpoint is damaged, not "slightly lossy."
2. **Task eval on the golden set.** Perplexity is necessary but not sufficient — the model must still clear the task's quality floor (Model Serving 01's golden set, DevMate's Hit@5/MRR gate as the retrieval-side shape of the same idea). A quant that holds perplexity but fails structured-output or citation checks fails verification.

**When quantization is acceptable versus harmful** is task-dependent, and the fault lines are predictable:

| Workload | 4-bit verdict | Why |
|---|---|---|
| Summarization, classification, casual chat | Usually fine | Tolerant of small logit perturbations |
| Code completion (DevMate's default task) | Usually fine; verify | Repetitive structure that 4-bit handles well — but verify on your own repos |
| Long-context retrieval ("which paragraph says X") | Verify extra; consider 8-bit | Needle-in-haystack behavior degrades first; attention sharpness matters |
| Arithmetic, unit conversion, counting | Known weak spot | Small logit gaps flip digits; keep a bigger model or a tool for math |
| Citation fidelity, religious/legal text (Athar territory) | Highest scrutiny | A hallucinated citation is the failure mode you cannot ship; hold the quality floor on *citation-exact* evals, not general fluency |

The pattern across the table: quantization hurts most where the decision between two candidate tokens is narrow and consequential. Your eval must contain those exact decisions; a general fluency check will pass a quant that fails your actual task.

**KV quantization stays a separate lever** because its cost profile differs: it multiplies capacity (every cell of section 5's table halves) rather than shrinking the model file, its accuracy cost concentrates at long context (where more cached positions are quantized), and it composes with weight quantization — int4 weights plus int8 KV is a legitimate 16 GB configuration, while int4 weights plus int4 KV is usually one quantization too many without evidence.

### 7. Prefix and Prompt Caching

Decode re-reads the KV cache for every token, but prefill is where prompts are paid for — and most RAG and agent prompts are mostly *repeated* text: the same system prompt, the same few-shot block, often the same retrieved documents for related questions. Prefix caching stores the KV blocks computed for a shared prompt prefix and reuses them for any later request whose prompt starts with the same tokens, skipping that portion of prefill entirely.

| Property | Detail |
|---|---|
| What is cached | KV blocks for the token prefix, block-aligned (e.g. 16-token blocks) |
| Match rule (engines today) | **Exact** token-prefix match; fuzzy matching is research, not the default |
| Invalidation | Any change from the first divergent byte/token onward; the unchanged head still hits |
| Who has it | vLLM automatic prefix caching; SGLang RadixAttention; TGI prompt cache |
| What it saves | Prefill FLOPs and TTFT — the RAG-context half of every request |

The RAG win is arithmetic. A prompt of 400 system tokens plus 3,000 retrieved tokens plus a 50-token question is 3,450 prefill tokens on a cold request. A second question that shares the system prompt and the retrieved block re-prefills only its own 50 tokens: roughly a 98% cut of that request's prefill, which on a long context is most of TTFT. The practical design rules:

- **Stable prefix first.** Put the invariant text at the front (system prompt, tool definitions, then retrieved context, then the question). Anything volatile before the shared block destroys the hit.
- **One byte invalidates from there on.** Cache matching is over tokens, in order. A timestamp in the system prompt, non-deterministic chunk ordering, or a retriever that returns documents in a different order every query converts a near-certain hit into a miss. Sort retrieved chunks by a stable key before formatting. DevMate's semantic cache (`config.py:126`, similarity threshold 0.85) is a *different* cache — it skips the LLM call for near-duplicate questions; prefix caching skips the *prefill* of shared text for every question, duplicates or not. Both belong in a RAG stack; neither replaces the other.
- **It is not a license to pad prompts.** Cached tokens still occupy KV cache (section 5's formula does not shrink for a hit; only the compute is saved). Caching changes the *compute* budget, not the *memory* budget.

### 8. Speculative Decoding

Decode is memory-bound on reading the target model's weights per token. Speculative decoding attacks that directly: a tiny *draft* model (or an n-gram/lookahead proposal, which needs no neural net at all) proposes the next k tokens cheaply, then the target model verifies all k in a **single** forward pass — one weight read, k positions checked. Accepted draft tokens cost almost nothing; a rejected token is corrected to the target's own sample and decoding continues from there.

The property that makes this safe: verification uses standard rejection sampling, so the output distribution is *exactly* the target model's distribution — speculative decoding is a lossless speedup, not an approximation. What it approximates is nothing; what it spends is the draft's compute and some verification overhead.

| Situation | Verdict | Why |
|---|---|---|
| Batch of 1-2, low concurrency, interactive | **Helps** | Decode is weight-read-bound; k verified tokens amortize one weight read |
| Highly predictable tokens (code boilerplate, JSON keys, repeated entities) | **Helps** | Draft acceptance rate stays high (0.7-0.9); few rejections |
| Large batch / high load | **Does not help** | The batch already amortizes the weight read; verification adds work for nothing |
| Creative, high-entropy text | Marginal | Low acceptance; most steps degrade to draft-then-reject overhead |
| Already compute-bound (big batch, long prefill mixed in) | **Harmful** | Verification competes for compute the batch was already using |

The batch-size line is sharp enough that the exercise enforces it as a rule (INF007): speculative decoding configured on a service whose steady batch is 8+ is theater. On this workstation the honest configuration is draft-plus-target for the *interactive, low-batch* path — for example a 1.5B draft against DevMate's 7B `qwen2.5-coder:7b` — off under load, or on a second deployment that serves the interactive tier while a batch deployment serves offline jobs. Measure tokens/sec at batch 1 and at your real batch before and after; the speedup that matters is the one at the batch you actually run.

### 9. Structured Output: Constrained Decoding

Any service that parses model output into JSON is running one of three mechanisms, and they fail differently:

| Mechanism | How it works | Format failures | Throughput cost | Failure mode |
|---|---|---|---|---|
| **Schema-constrained decoding** | Mask the logits at every step to tokens allowed by a JSON schema (guided decoding: outlines/xgrammar-style; vLLM guided_json; Ollama's `format` param) | Near zero | Small per-step masking overhead | Schema itself may be unrepresentable or over-constrained; model can still be *semantically* wrong inside valid JSON |
| **Grammar-constrained** (regex / EBNF) | Same masking, but the grammar is any regular/context-free spec, not just JSON | Near zero | Same family as above | You own the grammar; a wrong grammar produces valid-but-wrong shapes |
| **Retry-and-repair** | Prompt for JSON, parse, on failure re-prompt with the error ("here is what you emitted...") | High until retries exhaust | Up to N x cost and latency; burns output tokens on failures | Silent quality cost; a retry loop that always fires is a hidden 2-4x on the bill |

**FACT in this repository:** DevMate already ships the constrained path for its local provider. The Ollama provider passes the Pydantic response model's JSON schema as the request's `format` (`projects/04-ai-engineering/devmate/src/devmate/llm/client.py:579`) and validates the reply with `model_validate_json` (`client.py:606`); the Anthropic and OpenAI providers express the same intent through tool-use / tool-call blocks (`client.py:241-245`, `client.py:420-425`). The application-level Pydantic check stays regardless: constrained decoding guarantees the *shape*, and your validator is what catches a schema-shaped but nonsensical object.

Design rules: prefer schema-constrained decoding wherever the engine supports it (it converts a probabilistic failure into a deterministic one); keep retry-and-repair as the fallback for engines without it, with a hard attempt cap and a budget line (an uncapped repair loop is a cost-ceiling violation in disguise); and do not confuse format validity with answer quality — a perfectly parsed JSON full of invented citations still fails the quality floor from section 1.

### 10. Model Routing

One model for every request is simple and wasteful: the classify-the-button-label traffic pays frontier prices and latency. Routing sends each request to the cheapest model that clears its quality bar. Two families:

| Style | Mechanism | Cost to build | Risk |
|---|---|---|---|
| **Heuristic** | Rules on observable features: length, keywords, "cite sources" flags, tool-use markers | Low — a function | Misroutes at the edges |
| **Classifier-based** | A small fast model (or embedder + threshold) labels the request, then a table routes it | Medium — another model in the path | The router itself errs; needs its own eval and latency budget |

Routing earns its complexity only when the traffic is *heterogeneous and high-volume* — the point where a single strong model's cost or latency is clearly wrong for a large slice of requests. For uniform traffic, Model Serving 01's rule stands: one smallest-model-that-clears-the-bar, no router. The expanded decision table, which doubles as the router's spec:

| Request class | Route | Configuration |
|---|---|---|
| Classify, extract, short rewrite | Small model (1-3B or API-small) | No RAG; schema-constrained output; cached where possible |
| Summarization | Mid model | Prefix-cache the document block; one call per document, not per question |
| Grounded answer with citations (DevMate `/ask`, Athar fatwas) | Strong model + RAG + citations | Retrieval first; quality floor on faithfulness and citation exactness; never the small model |
| Hard reasoning, multi-step code, legal/religious ruling support | Strongest model, possibly cloud | Budget the cost ceiling per request; route only this class to the paid path |

**FACT in this repository:** DevMate's provider fallback chain is the routing pattern's simplest ancestor — the configured default first, then every other registered provider (`projects/04-ai-engineering/devmate/src/devmate/llm/client.py:684-686`), rotated on rate-limit, auth, and timeout errors in `complete()` (`client.py:753-778`). That chain routes on *provider health*; the router in this section routes on *request difficulty*. The two compose: classify the request, then walk the chain for that class.

### 11. Fallbacks: Local, Cloud, Degraded

Routing picks a target; the fallback chain decides what happens when that target is slow, down, or over budget. The Reliability lecture owns the dependency contract (timeout, retry, breaker, fallback, metrics); this section states the LLM-specific ladder, which the router and the fallback chain share:

```text
1. local strong path      qwen2.5-coder:7b via Ollama/vLLM, RAG-grounded, cited
2. cloud strong path      paid model, per-request budget cap, same contract
3. local degraded         smaller model, clearly labeled, no citation claim
4. cached answer          DevMate's semantic cache (config.py:126), labeled stale
5. typed error            Retry-After; never a blank page, never a confident guess
```

Two properties make the ladder safe, both inherited from the Reliability lecture and restated because LLM teams reinvent them badly: every hop carries its own **timeout** so a hung local Ollama cannot eat the request's whole deadline before the cloud hop is tried, and the chain ends in an explicit **terminal degraded state** — a chain of "local, then cloud, then..." with no rung 5 has no answer for "both are down" and will fail confusingly (the exercise enforces this as INF006). Budget caps belong on the cloud hop specifically: a fallback that silently triples the cost per request during an outage is a cost-ceiling breach that only shows up in the bill.

### 12. Measurement: Distributions, Not Averages

Every lever above is only as real as the numbers that confirm it. The five measurements, and what each one is *not*:

| Metric | Definition | Optimizes / detects |
|---|---|---|
| **TTFT** | Request accepted to first streamed token | Prefill length, queueing, prefix-cache hits |
| **Decode tokens/sec** | Output tokens per second while streaming | Batch size, KV bandwidth, engine choice |
| **p95 (and p99) end-to-end latency** | Tail of total request time | The SLO; averages hide exactly the users who churn |
| **Cost per 1k tokens** (or GPU-hours per query) | Money or amortized hardware | The cost ceiling; includes retries and repair loops |
| **Quality score** | Golden-set metric for the task | The floor; the thing latency wins must not spend |

**Benchmark method — fixed, warm, distributional:**

1. **Fixed prompt set.** A representative sample: short and long prompts, RAG and non-RAG, the structured-output path. The same set for every configuration compared — comparing an 8-bit baseline's prompts against a 4-bit candidate's different prompts measures the prompts (Topic 01's same-set discipline, restated for serving).
2. **Warmup.** Discard the first N runs: cold weights, cold CUDA context, cold caches all inflate early numbers. Report the steady state, and say how many warmup runs you dropped.
3. **Fixed generation parameters.** Temperature, max tokens, and seed where the engine supports it, so variance reflects the system, not the sampling.
4. **Report distributions.** p50/p95/p99 for latency, plus min/max; the mean alone is the metric that hides overload. Topic 03's percentile function is the tool; this lecture's rule is that every "X improved by Y%" claim carries the percentiles it was measured on.
5. **Re-measure the whole triple.** A quantization benchmark that reports tokens/sec and omits the golden-set score is half a benchmark. Section 1's triple is the report card.

On this workstation, ground truth beats extrapolation: a 7B int4 model's weights (~3.8 GB) plus its KV at your planned context and batch (section 5's formula) plus ~1-2 GB of runtime overhead is the pre-load budget check; the warm benchmark on the actual RTX 5000 is the post-load truth. Both numbers live in the same ADR (Model Serving 01's decision record).

---

## Common Mistakes to Avoid

### 1. Optimizing Latency Alone

```text
❌ BAD:  "We switched to 4-bit; p95 TTFT dropped 35%."     (quality unmeasured)
✅ GOOD: "4-bit cut p95 TTFT 35%; golden-set MRR moved 0.74 → 0.73,
          still above the 0.70 floor; perplexity delta 0.2. Shipping."
```

### 2. Budgeting Only Weights Against VRAM

```python
# ❌ BAD: 7.6B x 0.5 bytes = 3.8 GB "fits in 16 GB"
weights_gb = params_b * bytes_per_param

# ✅ GOOD: weights + KV at the planned context/batch + runtime overhead
kv_gb = layers * 2 * kv_heads * head_dim * kv_bytes * seq_len * batch / 1e9
total_gb = weights_gb + kv_gb + overhead_gb  # budget against THIS
```

### 3. Trusting "It Looks Fine" After Quantizing

```text
❌ BAD:  load the 4-bit model, ask two questions, declare it fine
✅ GOOD: perplexity delta on held-out text, then the golden-set eval,
         with the quality floor as a hard gate (ci.yml:71-77's shape)
```

### 4. Letting Volatile Text Lead the Prompt

```python
# ❌ BAD: timestamp before the shared block — every request misses the cache
prompt = f"[{datetime.now():%Y-%m-%d %H:%M}]\n{system}\n{docs}\n{question}"

# ✅ GOOD: invariant text first, question last; volatile fields go last or
# disappear into headers the engine does not tokenize into the prefix
prompt = f"{system}\n{sorted_docs}\n{question}"
```

### 5. Enabling Speculative Decoding Under Load

```text
❌ BAD:  spec=true on the production deployment serving batch 8-16
✅ GOOD: spec on the interactive path (batch 1-2), off on the batch tier;
         tokens/sec measured at the REAL batch before and after (INF007)
```

### 6. Raising Batch Size With No Latency SLO

```text
❌ BAD:  max_num_seqs 4 → 16 because throughput looked low
✅ GOOD: raise only while p95 end-to-end stays under the stated SLO;
         record both numbers (INF005 fires on the unmeasured raise)
```

### 7. Retry-and-Repair as the Default JSON Strategy

```python
# ❌ BAD: prompt, parse, re-prompt with the error — uncapped, unmeasured
for _ in range(10):
    text = llm(prompt)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        prompt += f"\nYour output was invalid: {text[:200]}"

# ✅ GOOD: constrained decoding first; capped repair only as fallback
payload["format"] = response_model.model_json_schema()  # client.py:579's move
return response_model.model_validate_json(reply)
```

### 8. A Fallback Chain With No Terminal State

```text
❌ BAD:  local → cloud → (nothing): both down means an unhandled exception
✅ GOOD: local → cloud → labeled degraded cache → typed error with Retry-After
```

---

## Best Practices

1. **Write the triple before the lever** — p95 SLO, cost ceiling, quality floor — and re-measure all three after every optimization change.
2. **Treat the engine as capacity** — PagedAttention plus continuous batching (vLLM, SGLang) is most of a single-GPU concurrency ceiling; Ollama stays the development path.
3. **Read prefill and decode as different machines** — TTFT is prefill (long RAG contexts), tokens/sec is decode (batch and bandwidth); fix each with the lever that addresses its bound.
4. **Let the engine batch** — continuous batching in the server; individual requests from the application; no application-level grouping.
5. **Size the KV cache with the formula** at the planned context *and* batch, before the model loads; `max_model_len` is a budget line.
6. **Quantize weights first, KV second** — int4 weights plus int8 KV is a sound 16 GB configuration; stack more only with evidence.
7. **Verify every quantization with perplexity delta plus task eval**; hold the quality floor on the decisions your task actually makes (citations, needles, digits).
8. **Keep invariant prompt text first** for prefix-cache hits; sort retrieved chunks stably; never lead with a timestamp.
9. **Deploy speculative decoding only where batch size is small** and token predictability is high; measure at your real batch.
10. **Prefer schema-constrained decoding** over retry-and-repair; cap and budget any repair loop.
11. **Route on request difficulty, not habit** — small for classify/extract, mid for summarize, strong+RAG+citations for grounded answers; skip the router until traffic is heterogeneous enough to pay for it.
12. **End every fallback chain in a terminal degraded state** with per-hop timeouts and a budget cap on the cloud hop.
13. **Benchmark with warmup, fixed prompts, and fixed parameters**; report p50/p95/p99, never the mean alone.
14. **Keep the provider behind the interface** (Topics 02-04) so every lever here stays a configuration change, not a rewrite.

---

## Practice Exercises

### Exercise 1: Run the Planner and Fix the BAD Pack
Open `exercises/05-inference-optimization.py` and run it. The BAD pack trips all seven INF rules; the GOOD pack must raise zero. For each finding, state the section of this lecture that explains it, then write your own third pack (a 13B int8 model at batch 8, 16k context, with prefix caching and a quality floor) and drive it to zero findings.

### Exercise 2: Size the KV Cache for Your Own Context Target
Using the `kv_cache_bytes` function, compute the cache for `qwen2.5-coder:7b`'s shape (28 layers, 4 KV heads, head dim 128) at fp16 and int8 KV across 4k, 8k, and 16k context at batch 1, 4, and 8. At which cell does KV alone exceed half of the 16 GB card? What does that cell imply about `max_model_len` and `max_num_seqs` for the DevMate deployment (`ollama_num_ctx` is 8192, `config.py:122`)?

### Exercise 3: Verify a Quantization Claim
Take any two checkpoints of the same model (fp16/bf16 versus a 4-bit quant). Write down the two-gate protocol from section 6: the held-out perplexity delta you will accept and the golden-set metric with its floor. Explain why a quant that passes gate 1 can still fail gate 2, and name the task class from the section 6 table where that gap is most likely.

### Exercise 4: Compute a Prefix-Cache Win for a RAG Prompt
Model a DevMate-style `/ask` prompt: 400-token system prompt + 3,000-token retrieved context + 50-token question. Compute prefill tokens for two consecutive questions sharing the retrieved block, with and without prefix caching, at 16-token blocks. Then change one byte inside the system prompt and recompute. What does the result say about where timestamps and unordered retrieval results belong in the prompt?

### Exercise 5: Audit the Real Service's Serving Config
Export DevMate's actual local serving parameters — Ollama base URL and model (`config.py:49-50`), `ollama_num_ctx` (`config.py:122`), and the intended concurrency — into the JSON format the exercise accepts. Run it through the rules. If your real config trips INF005 or INF006 (no latency SLO; fallback chain without an explicit degraded terminal), decide whether to add the missing policy or accept the finding with a written rationale — but do not silence the rule.

---

## Summary

Inference optimization is one objective viewed from several angles:

1. **The objective is a triple, not a metric** — p95 latency SLO under a cost ceiling above a quality floor; every lever trades among the three, so every change re-measures all three.
2. **The engine is the capacity decision** — PagedAttention's paged KV blocks and continuous batching (vLLM, SGLang, TGI) are why one 16 GB GPU can hold a large live batch; Ollama remains the development path.
3. **Prefill and decode are different machines** — prefill is compute-bound and owns TTFT; decode is memory-bound on weight reads, which is why batching is nearly free throughput and why speculative decoding exists.
4. **The KV cache is the long-context budget** — `layers x 2 x kv_heads x head_dim x dtype_bytes x seq_len x batch` at your planned batch and context; KV quantization is a second, independent lever from weight quantization.
5. **Quantization is verified, not assumed** — perplexity delta plus golden-set task eval; acceptable for chat and code, high-scrutiny for long-context retrieval, arithmetic, and citation fidelity.
6. **Shared prefixes are free compute** — prefix caching turns RAG's repeated system prompt and retrieved context into TTFT wins, at the cost of demanding stable, byte-identical prompt heads.
7. **Speculation and structure are conditional wins** — speculative decoding only at small batch with predictable tokens, verified losslessly; schema-constrained decoding over retry-and-repair for anything that parses.
8. **Routing and fallbacks spend complexity only where traffic earns it** — small/mid/strong tiers for heterogeneous load, a chain ending in a labeled degraded state, per-hop timeouts, and a budget cap on the cloud hop.
9. **Measurement is distributions** — TTFT, tokens/sec, p95/p99, cost per 1k tokens, quality score, on fixed prompts after warmup; the average is the metric that hides overload.

**Next lecture:** Evaluation-driven serving loops — re-running the golden set and the benchmark harness after every lever so the SLO, the cost ceiling, and the quality floor stay true in production, not only at launch.
