# 🏋️ Module 1 Practice Workbook — LLM Fundamentals & API Integration

> Companion practice for the Week-1 lecture: [`../lectures/01-llm-fundamentals.md`](../lectures/01-llm-fundamentals.md).
> Format and mastery protocol: [`README.md`](README.md). Per [ADR-0006](../../decisions/0006-adopt-master-ai-engineering-curriculum.md),
> curriculum content is production-focused and anchored to DevMate — `../../../projects/04-ai-engineering/devmate/`.
> Track context: [`../../roadmap/active-track-10-week.md`](../../roadmap/active-track-10-week.md) — Week 1, Milestone A2.

**How to use** — (1) Do sections 1.1 → 1.4 in order; each section's real-world problem is the lens — read it before the topics. (2) Every topic has three levels — Level 1 must pass before Level 2, Level 2 must produce a repo artifact before Level 3; a level isn't done until its **Verify** command proves it. (3) Every failure you hit goes into `../../../projects/04-ai-engineering/devmate/mistakes.md` — that file is a deliverable, not a diary.

**Local command note (this workstation):** `make` and `poetry` are not installed here. Wherever a command says `poetry run python ...`, run `& .venv\Scripts\python.exe ...` from `projects/04-ai-engineering/devmate/` instead (see the repo `AGENTS.md`). The `devmate/labs/` scratch folder exists for the drill scripts below.

**Week-1 Definition of Done (roadmap §4 — cite this when you finish):** *every LLM call appears as a Langfuse trace with token count and cost; you can state the cost of one `devmate ask` in dollars.*

| Lecture section | Topics covered here | Workbook section |
|---|---|---|
| 1.1 How LLMs Work | tokenization · transformer · sampling · training objectives | [§1.1](#-11-how-llms-work) |
| 1.2 API Integration Patterns | request structure · streaming · structured outputs | [§1.2](#-12-api-integration-patterns) |
| 1.3 Production Patterns | retries · cost tracking · fallback · timeouts | [§1.3](#-13-production-patterns) |
| 1.4 Prompt Engineering for Production | system prompts · few-shot · versioning · CoT | [§1.4](#-14-prompt-engineering-for-production) |

**Targets you are training against (lecture case study):** P50 latency 1.2 s · streaming TTFT 300 ms · cost $0.002–0.015/query · 99.9% uptime with fallback · zero prompt-injection incidents.

---

## 📚 1.1 How LLMs Work

**Real-world problem — legal-tech contract Q&A.** A legal-tech startup ships a Q&A bot over 200-page contracts using Claude 3.5 Sonnet (200k context). Production shows three failures: (1) the model "forgets" page 1 of a 180-page contract — the input silently exceeds the window and the SDK truncates the front; (2) engineering counted tokens by characters and budgeted 4× less than reality, so the monthly bill is 3× the forecast; (3) `temperature=0.7` was left at a sample default, so two identical questions return differently-worded legal answers and the legal team refuses to sign off. The engineer must decide which mechanics (tokenization math, context budgeting, sampling, what training actually bought you) to master before choosing models and defaults for the rewrite. Everything in this section is a tool that decision needs.

### Topic 1.1.a — Tokenization: tokens ≠ words, vocabulary, context window, tiktoken

**Mastery =** you can predict token counts within ±10% before sending, compute a context-window budget (input + output) with the off-by-one handled, explain why tokens ≠ words, and debug truncation and `max_tokens` errors from a token-count screenshot.

**Level 1 — Drill** (mechanics, 20–45 min)

Save as `projects/04-ai-engineering/devmate/labs/tokenization_drill.py` (scratch folder, not a tracked deliverable) and run with `poetry run python labs/tokenization_drill.py` from the DevMate folder:

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

# 1. Verified tokens for a known string
toks = enc.encode("Hello, world!")
print("tokens:", toks)  # expect [9906, 11, 1917, 0]
print("count:", len(toks))  # expect 4

# 2. Tokens per English word (rule of thumb ≈ 1.3)
prose = ("The quick brown fox jumps over the lazy dog " * 10).strip()  # 80 words
words = len(prose.split())
tokens = len(enc.encode(prose))
print(
    f"words={words} tokens={tokens} ratio={tokens / words:.2f}"
)  # expect ratio ≈ 1.2–1.5

# 3. Context-window budget with the off-by-one handled
CONTEXT = 200_000  # claude-3-5-sonnet-20241022
max_output_tokens = 4_096  # devmate config default
available_for_input = CONTEXT - max_output_tokens
print("available_for_input:", available_for_input)  # expect 195_904 (NOT 200_000)


# 4. Estimate-before-send guard (the trap: forgetting the system prompt and a margin)
def would_overflow(messages, max_tokens, context=CONTEXT, margin=256):
    prompt_tokens = sum(len(enc.encode(m["content"])) for m in messages)
    return prompt_tokens + max_tokens + margin > context


msgs = [
    {"role": "system", "content": "You are a contract assistant. " * 20_000}
]  # ~140k tokens
print("overflow:", would_overflow(msgs, 4_096))  # expect True
print(
    "fits:", would_overflow([{"role": "user", "content": "hi"}], 4_096)
)  # expect False
```

Assertions: `count == 4`; `1.1 <= ratio <= 1.6`; `available_for_input == 195_904`; both overflow flags exact.

**Level 2 — Applied** (DevMate, 1–3 h)

Add a context-window guard to the real client. Modify `projects/04-ai-engineering/devmate/src/devmate/llm/client.py`:

- Add `CONTEXT_WINDOWS = {"claude-3-5-sonnet-20241022": 200_000, "gpt-4o": 128_000}` and a function `ensure_within_context(messages, model, max_tokens, margin=256)` that uses the provider's `count_tokens` and raises `LLMError` with `"Prompt tokens X + max_tokens Y + margin exceed context window Z (model W)"` before any token is sent.
- Call it at the top of `LLMClient.complete` (the method at client.py:537) and keep `LLMClient.count_tokens` (client.py:585) as the single counting path.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_context_window.py`: a 195_905-token prompt + 4_096 max_tokens raises; 195_904 fits; an unknown model uses the documented fallback window you choose.

**Deliverable:** modified `client.py`, new test file. **Acceptance:** `make test` passes with the new tests green, `make types` and `make lint` pass, and a scratch script building a ~200k-token `messages` list fails with *your typed guard message* — not a provider 400.

**Level 3 — Stretch** (production-grade, 3–6 h)

The estimation-accuracy problem: DevMate's `count_tokens` uses tiktoken `cl100k_base` for Anthropic (approximation, ±5–20% error on code and non-English text) and `encoding_for_model` for OpenAI. Options: (A) offline tiktoken everywhere (cheap, fast, sometimes wrong); (B) call Anthropic's exact `count_tokens` endpoint before every request (exact; +1 API call, +latency, +$); (C) hybrid — offline estimate pre-send for guardrails, exact count cached per prompt prefix for billing reconciliation. Decide which protects the legal-tech use case (hard token ceiling, billing accuracy) at the lowest cost. **Write an ADR-style justification** (Context, Decision Drivers, Options Considered, Decision, Consequences — template at `../../../templates/adr.template.md`) into `docs/decisions/` as `00NN-token-estimation-strategy.md` (Status: Proposed), with error rates you measure on this repo's own source files.

**Verify:** `poetry run python labs/tokenization_drill.py` prints the four expected values; `make test` green; the ADR file exists with a non-empty Consequences section.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Model "forgets" the start of a long document | Input exceeded the context window; truncated silently | Estimate before send; raise typed error (your L2 guard) |
| Bill is 3× forecast | Counting characters instead of tokens (~4 chars ≈ 1 token) | Always count via tiktoken, never `len(text)` |
| `max_tokens` too large → 400 | Output cap exceeds model max | Cap `max_tokens` per model; remember it is *output* only |
| `encoding_for_model` raises KeyError | Model name not in tiktoken registry (Anthropic models) | Fall back to `cl100k_base` (DevMate already does, client.py:140) |
| Budget math off by one | Forgot the system prompt or a margin | Budget = input + output + margin; never `context - max_tokens` alone |

**Interview:** "How do you estimate tokens before sending a request, and why does it matter?" A strong answer covers: tokens ≠ words (~1.3/word; code is denser); tiktoken vs exact `count_tokens` and the approximation trade-off; the budget formula input + max_tokens + margin ≤ context; where the failure shows up (silent truncation vs 400 vs cost); and that you guard *before* send with a typed error, never after.

### Topic 1.1.b — Transformer architecture: embeddings, positional encoding, self-attention, causal masking

**Mastery =** you can explain the data flow (embeddings → positional encoding → N×(attention → FFN) → next-token probabilities), implement a causal mask and a single attention head in numpy, and connect each mechanism to a real API behavior (why `max_tokens` exists, why streaming yields tokens in order, why `tool_choice` works).

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/attention_drill.py`, run with `poetry run python labs/attention_drill.py`:

```python
import numpy as np

rng = np.random.default_rng(7)

# 1. Causal mask: position i may attend only to j <= i. Exact expected matrix:
n = 4
causal = np.tril(np.full((n, n), 0.0), k=0) - np.triu(np.full((n, n), np.inf), k=1)
print(causal)
# expect:
# [[ 0. -inf -inf -inf]
#  [ 0.  0.  -inf -inf]
#  [ 0.  0.   0.  -inf]
#  [ 0.  0.   0.   0. ]]

# 2. One attention head, tiny dims
X = rng.normal(size=(4, 8))  # 4 tokens, 8-d embeddings
Wq, Wk, Wv = (rng.normal(size=(8, 4)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv
scores = Q @ K.T / np.sqrt(4)  # scaled dot-product
scores = scores + causal  # causal masking BEFORE softmax
attn = np.softmax(scores, axis=-1)
out = attn @ V

assert attn.shape == (4, 4)
assert np.allclose(attn.sum(axis=1), 1.0)  # rows are distributions
assert np.allclose(attn[1, 2:], 0.0)  # no attending to the future
assert np.allclose(attn[0, 1:], 0.0)  # token 0 sees only itself
print("attention row sums:", attn.sum(axis=1))  # [1. 1. 1. 1.]
print("output shape:", out.shape)  # (4, 4)
```

The assert suite is the expected output: any assertion failure means the mechanism is wrong.

**Level 2 — Applied** (DevMate, 1–3 h)

Write the internal explainer `projects/04-ai-engineering/devmate/docs/llm-internals.md`: a walkthrough mapping each mechanism to a real decision in this repo's code, citing real line numbers:

- Input embeddings → why `schemas.py` models message content as text and why `client.py` separates `system` from `messages` (Anthropic top-level `system`, client.py:167–184).
- Causal masking / autoregression → why `max_tokens` exists as an *output* budget (config.py default 4096) and why a stream arrives in order and must be consumed in order (`_stream_complete` yields deltas as they arrive, client.py:265–309).
- Temperature → why config.py defaults to `0.1` and temperature lives on the request, not in the prompt.
- Next-token distribution → why structured outputs are a *sampling* feature (`tool_choice` forces one branch of the distribution, client.py:187–194).

**Deliverable:** the doc + a 2-minute recorded English explanation of the flow (track §7). **Acceptance:** the file exists, contains at least one real `client.py`/`config.py`/`schemas.py` line reference per mechanism, and links are valid (note: `make docs-check` scans `docs/` only — self-check links inside `devmate/docs/`).

**Level 3 — Stretch** (production-grade, 3–6 h)

The quadratic-attention cost problem: attention is O(n²), so a 200k-token prompt costs ~100× the compute of a 20k prompt — in latency *and* $ — before the model writes one word. Your legal-tech product must summarize 200-page contracts. Options: (A) truncate to fit (loses page 1 — the failure from the section problem); (B) chunk-and-map-reduce (multiple calls, loses cross-chunk reasoning); (C) prompt caching for the repeated prefix (one full pass per document version, cheap re-reads); (D) a long-context model tier for the full-document path, short-context for everything else. Design the context architecture with measured token math per option. **Write an ADR-style justification** into `docs/decisions/` including an O(n²) cost-curve table for 20k/60k/120k/200k tokens.

**Verify:** drill prints the exact causal-mask matrix and all asserts pass; `devmate/docs/llm-internals.md` exists with line references; ADR exists with Consequences.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Long requests slow *before* the first token | O(n²) attention over the whole prefix | Shrink input, cache the prefix, or tier the model |
| "Model only knows the last N pages" | Implicit truncation by a gateway/SDK, not your code | Assert on actual prompt tokens, not assumptions |
| Streaming output seems out of order | Concurrent or chunk-buffered consumption | Consume the generator in order (client `aiter_lines` already does) |
| Confusing context window with output cap | `max_tokens` is one half of the budget | Budget both sides; window = input + output |
| Softmax over full scores instead of masked | Attention sees the future; trained behavior leaks | Mask before softmax, always |

**Interview:** "Explain how a transformer generates the next token, from tokenization to sampling." A strong answer covers: tokens → embeddings + positional encoding; self-attention with causal masking; stacked layers ending in a logits projection + softmax; sampling (temperature/top-p) picks from that distribution; the output token is appended and the loop repeats — and you tie each stage to an API parameter (`max_tokens`, `temperature`, streaming order).

### Topic 1.1.c — Sampling: temperature, top-p, when each matters

**Mastery =** you can pick `temperature`/`top_p` per task type with justification, predict determinism vs creativity behavior, and debug flaky tests or wrong answers caused by sampling.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/sampling_drill.py`:

```python
import numpy as np

rng = np.random.default_rng(42)
logits = np.array([2.0, 0.5, -1.0, 3.5, 0.0])  # token 3 is the argmax


def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()


def sample(logits, temperature=1.0, top_p=1.0):
    probs = softmax(logits / temperature)
    if top_p < 1.0:  # nucleus filtering
        order = np.argsort(probs)[::-1]
        cum = np.cumsum(probs[order])
        keep = order[cum <= top_p]
        if len(keep) == 0:
            keep = order[:1]
        probs[~np.isin(np.arange(len(probs)), keep)] = 0.0
        probs /= probs.sum()
    return probs


p_greedy = sample(logits, temperature=1e-9)  # ≈ argmax
p_cold = sample(logits, temperature=0.2)
p_hot = sample(logits, temperature=2.0)
p_nucleus = sample(logits, temperature=1.0, top_p=0.5)


def entropy(p):
    return float(-(p * np.log(p + 1e-12)).sum())


print("greedy argmax:", int(np.argmax(p_greedy)))  # expect 3
print("cold entropy:", round(entropy(p_cold), 4))  # low
print("hot entropy: ", round(entropy(p_hot), 4))  # higher than cold
print("nucleus support:", int((p_nucleus > 0).sum()))  # expect 2 tokens at top_p=0.5

assert np.argmax(p_greedy) == 3
assert entropy(p_cold) < entropy(p_hot)  # temperature spreads probability
assert (p_nucleus > 0).sum() == 2
draws = [
    int(rng.choice(len(logits), p=sample(logits, temperature=t)))
    for t in (0.2, 0.2, 2.0)
]
assert draws[0] == draws[1]  # same seed + same T → same draw
print("draws (0.2, 0.2, 2.0):", draws)
```

The asserts are the expected output: greedy → 3; cold entropy < hot entropy; nucleus support exactly 2; same-seed same-T draws equal.

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate hardcodes `temperature=0.1` in `config.py` and threads it through `client.py`. Production reality: different tasks want different sampling (code analysis → 0.0–0.1; explanation prose → 0.3; brainstorming → 0.7). Implement a preset layer:

- New file `projects/04-ai-engineering/devmate/src/devmate/llm/sampling.py`: `TEMPERATURE_PRESETS = {"analysis": 0.0, "explain": 0.3, "creative": 0.7, "default": 0.1}` and `resolve_temperature(task, explicit)` — explicit wins; unknown task → default.
- Modify `LLMClient.complete` in `client.py` to accept `task: str | None = None` and use `resolve_temperature` when `temperature` was not passed.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_sampling.py`: explicit overrides preset; unknown task falls back to 0.1; each preset value is correct.

**Deliverable:** `sampling.py`, `client.py` change, test file. **Acceptance:** `make test`, `make types`, `make lint` all green.

**Level 3 — Stretch** (production-grade, 3–6 h)

The evaluation-reproducibility problem: your 10 golden cases must prove a prompt change is better — but at `temperature=0.1` the same prompt gives different answers run to run, so you can't tell signal from noise. Options: (A) force `temperature=0` for eval (deterministic; masks production variance — and Anthropic exposes no seed); (B) n-sample each case (k=3–5 draws, compare distributions) at k× token cost; (C) replay recorded cassettes (deterministic, but tests the evaluator, not the model); (D) tolerance metrics (semantic similarity, not string equality). Design the eval policy for the golden set, including the budget it implies (k × cases × tokens × $/token using `MODEL_PRICING`). **Write an ADR-style justification** into `docs/decisions/`.

**Verify:** drill prints all four expected values and passes asserts; `make test` green; ADR file exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Flaky golden-case results | String-exact assertions on a sampling process | Semantic/tolerance assertions or temperature 0 for the eval run |
| Legal/finance answers vary word-for-word | Temperature left at provider default (often 1.0) | Set 0.0–0.1 for factual tasks; document why per task |
| "More creative" feels random, not creative | Temperature raised without top-p tuning | top-p for vocabulary focus; temperature for spread |
| Output changes when fallback fires | Same temperature ≠ same distribution across models | Per-model sampling params; re-tune on the fallback |
| Structured output occasionally invalid | High temperature on tool calls | Structured paths get temperature 0–0.2 or `tool_choice` alone |

**Interview:** "When would you set temperature to 0, and when would you raise it? How does top-p differ?" A strong answer covers: temperature scales logits (0 ≈ greedy; >1 flattens the distribution); top-p cuts the low-probability tail (nucleus sampling); the guidance low-for-factual/structured, moderate-for-prose, higher-for-ideation; and reproducibility for tests and evals — providers expose no seed, so you engineer around it (temperature 0, tolerance metrics, or n-sampling).

### Topic 1.1.d — Training objectives: pre-training vs fine-tuning vs RLHF/RLAIF

**Mastery =** you can explain what each training phase buys you, map a business requirement to "API + prompt engineering" vs "fine-tune", and defend the choice with cost math.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/training_drill.py` — a classification exercise with exact expected answers:

```python
# For each scenario choose "prompt" (frontier API + prompt engineering) or "ft" (fine-tune).
# Reference table (lecture §1.1):
#   Pre-training: next-token prediction on trillions of tokens (you never do this).
#   Fine-tuning:  instruction following on curated data (domain format, style, skills).
#   RLHF/RLAIF:   preference alignment (helpfulness, harmlessness — the API already has it).


def classify(case: str) -> str:
    ft_cases = {
        "legal_contract_extraction",
        "startup_brand_voice_tweets",
        "medical_coding_icd10",
        "low_latency_embedding_style_router",
    }
    return "ft" if case in ft_cases else "prompt"


scenarios = {
    "legal_contract_extraction": "ft",  # fixed format, proprietary domain, high volume
    "general_code_assistant": "prompt",  # frontier models excel; prompts adapt fast
    "startup_brand_voice_tweets": "ft",  # a specific style the base model lacks
    "medical_coding_icd10": "ft",  # narrow, high-accuracy, labeled data
    "silly_haiku_for_internal_tool": "prompt",  # cost of ft >> prompt value
    "low_latency_embedding_style_router": "ft",  # need small+fast; frontier is overkill
}
for case, expected in scenarios.items():
    assert classify(case) == expected, (
        f"{case}: got {classify(case)}, expected {expected}"
    )
print("classification: all 6 scenarios correct")
```

Expected output: `classification: all 6 scenarios correct`. Then, in 2–3 sentences each, write the rationale for the two borderline cases (medical coding, brand voice) — the drill forces the decision, your notes force the reasoning.

**Level 2 — Applied** (DevMate, 1–3 h)

Write the decision memo `projects/04-ai-engineering/devmate/docs/fine-tune-or-not.md`: should DevMate fine-tune a small model for code explanation, or keep the frontier API + prompt engineering? Required content:

- Quantified baseline: 10,000 `devmate ask`/day at ~2,000 prompt + ~500 completion tokens per query. Using `MODEL_PRICING` from `src/devmate/obs/cost.py`, compute $/day and $/month for `claude-3-5-sonnet-20241022` and for a cascade using `claude-3-5-haiku-20241022` on simple questions.
- What fine-tuning would buy (format adherence, latency if self-hosted) vs what it costs (data curation, eval burden, drift, ops).
- The RLHF point: the frontier API's alignment is already paid for; a fine-tuned small model must re-earn safety behaviors.
- A one-paragraph recommendation with the number that would flip it (volume, quality gap, latency SLO).

**Deliverable:** the memo. **Acceptance:** file exists; ≥3 quantified comparisons traceable to `MODEL_PRICING`; ends with a recommendation and a flip-condition.

**Level 3 — Stretch** (production-grade, 3–6 h)

Build the full build-vs-buy model for the legal-tech scenario: 200k-token documents, 50k queries/month, quality requirement, latency SLO 4 s P95, and a data-privacy constraint (client contracts must not leave the VPC). Compare: (A) frontier API + prompt engineering + caching; (B) fine-tuned small model self-hosted on GPU; (C) hybrid — frontier for hard cases, small model for easy ones, behind a router. Include a cost table (API $/month vs GPU lease + engineering), latency, privacy posture, and an eval plan to decide routing quality. **Write an ADR-style justification** into `docs/decisions/` with explicit revisit conditions (e.g., "revisit when volume > X or quality gap < Y").

**Verify:** drill prints the classification line and all asserts pass; `devmate/docs/fine-tune-or-not.md` exists; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Fine-tuned model still follows prompts badly | Fine-tuning didn't fix a system-prompt/format problem | Fix prompt + eval first; fine-tune only for domain/format |
| Fine-tune improves golden set, fails in prod | Overfit to curated data distribution | Eval on production traffic sample; keep a held-out set |
| "We need RLHF" as a project plan | Confusing alignment with instruction following | Alignment is already in the API you call |
| Privacy breach | Fine-tuning on customer data without controls | Data governance before training; or keep data in the API under a DPA |
| Cost of fine-tune never recouped | No volume/price model before starting | Do the L3 cost table before any training run |

**Interview:** "Your startup is on GPT-4-class APIs and wants to cut cost — fine-tune or prompt-engineer? Walk me through the decision." A strong answer covers: the three phases and what each buys (pre-training is never yours; RLHF is in the API; fine-tuning is for domain/format); the decision inputs — volume, quality gap, latency, privacy, eval burden; the math (monthly API spend vs training + serving + engineering); and the process — measure the prompt-engineered baseline *first*, then fine-tune only against a defined gap, with an eval gate and revisit conditions.

---

## 📚 1.2 API Integration Patterns

**Real-world problem — fintech support bot with a broken UX.** A fintech deploys a support bot: answers arrive as one blob 8–12 s after the user asks (users abandon; their own data shows 60% drop-off after 6 s); the UI needs structured JSON (intent, answer, action buttons) but receives markdown paragraphs; and requests behave differently in dev vs prod because payloads are assembled by hand in three places. The engineer must standardize the request contract (model/system/messages/max_tokens/temperature), move to streaming for perceived latency, and force structured outputs so the frontend never parses prose. Targets from the lecture case study: TTFT ≤ 300 ms, P50 total ≤ 1.2 s.

### Topic 1.2.a — Basic request structure: model, system, messages, max_tokens, temperature

**Mastery =** you can build a correct request for Anthropic and OpenAI from one internal spec, know which fields are required vs optional per provider, and debug 400s from payload mistakes.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/request_drill.py`:

```python
from typing import List, Dict


def anthropic_payload(
    system: str,
    messages: List[Dict[str, str]],
    model: str,
    max_tokens: int,
    temperature: float,
) -> dict:
    return {
        "model": model,
        "system": system,  # top-level, NOT inside messages
        "messages": messages,  # must alternate user/assistant, first = user
        "max_tokens": max_tokens,  # REQUIRED by Anthropic
        "temperature": temperature,
    }


def openai_payload(
    system: str,
    messages: List[Dict[str, str]],
    model: str,
    max_tokens: int,
    temperature: float,
) -> dict:
    return {
        "model": model,
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }


def validate_roles(messages: List[Dict[str, str]]) -> None:
    roles = [m["role"] for m in messages]
    assert roles and roles[0] == "user", "first message must be user"
    for a, b in zip(roles, roles[1:]):
        assert a != b, f"roles must alternate, got {a} then {b}"


sys = "You are a financial assistant."
msgs = [
    {"role": "user", "content": "What is my balance?"},
    {"role": "assistant", "content": "Your balance is $1,234.56."},
    {"role": "user", "content": "And my last 3 transactions?"},
]

assert anthropic_payload(sys, msgs, "claude-3-5-sonnet-20241022", 1024, 0.1) == {
    "model": "claude-3-5-sonnet-20241022",
    "system": sys,
    "messages": msgs,
    "max_tokens": 1024,
    "temperature": 0.1,
}
assert openai_payload(sys, msgs, "gpt-4o", 1024, 0.1)["messages"][0] == {
    "role": "system",
    "content": sys,
}
validate_roles(msgs)  # OK

try:
    validate_roles([{"role": "user", "content": "a"}, {"role": "user", "content": "b"}])
    raise SystemExit("should have raised")
except AssertionError:
    pass
print("request structure: all assertions pass")
```

Expected output: `request structure: all assertions pass`. Add a written note of the Anthropic-vs-OpenAI system-message difference — that is the classic 400 cause.

**Level 2 — Applied** (DevMate, 1–3 h)

Harden the request contract. `LLMRequest` already exists in `projects/04-ai-engineering/devmate/src/devmate/llm/schemas.py` (messages, model, max_tokens=4096, temperature=0.1, stream, response_format). Add validation:

- A `model_validator(mode="after")` on `LLMRequest`: messages non-empty; roles ⊆ {system, user, assistant}; first non-system role is `user`; `max_tokens` ∈ [1, 8192] (claude-3-5-sonnet's output ceiling); `temperature` ∈ [0, 2].
- Create `projects/04-ai-engineering/devmate/tests/unit/test_request_schema.py`: one positive test; three negative tests asserting `ValidationError` for empty messages, consecutive user roles, and `max_tokens=0`.

**Deliverable:** modified `schemas.py`, new test file. **Acceptance:** `make test` passes with the new tests; `make types`, `make lint` green.

**Level 3 — Stretch** (production-grade, 3–6 h)

Cross-provider request normalization: one internal spec (`LLMRequest`) must produce correct payloads for Anthropic (system top-level, `max_tokens` required, alternating roles) and OpenAI (system as message, different `tool_choice` nesting) — DevMate's providers build payloads by hand in `client.py` (two copies). Options: (A) keep per-provider builders behind `BaseLLMProvider` (current state — drift risk, as the streaming-usage gap in 1.3.b demonstrates); (B) a central translator `to_provider_payload(provider, spec)` with per-provider normalizers; (C) schema-driven: each provider declares a transformation spec, verified by cross-provider contract tests that send the *same* `LLMRequest` through both builders and assert semantic equivalence. **Write an ADR-style justification** into `docs/decisions/` for the normalization boundary you choose, including the contract-test matrix (fields × providers).

**Verify:** drill prints the pass line; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| 400 on Anthropic: `max_tokens` field required | Required on Anthropic, optional on OpenAI | Always pass it (DevMate: `settings.max_tokens`, 4096) |
| 400: roles must alternate | Two user messages in a row | Validate before send (your L2 validator) |
| System instructions ignored | System passed inside `messages` to Anthropic | Top-level `system` field (client.py:167–184 already does this) |
| Dev and prod behave differently | Payloads assembled in three places | Single validated `LLMRequest` as the contract |
| Temperature > 2 → 400 | Out-of-range param | Clamp/validate in the schema |

**Interview:** "Walk me through the fields of a chat completion request and what each one does." A strong answer covers: model (capability + cost + window); system vs messages roles (and the Anthropic/OpenAI difference); max_tokens (output budget, required on Anthropic); temperature (sampling); stream (delivery mode); tools/tool_choice (structured behavior); and validating the contract once so dev == prod.

### Topic 1.2.b — Streaming: sync + async, text_stream, cancellation, UX latency perception

**Mastery =** you can implement sync and async streaming, measure TTFT correctly, handle cancellation cleanly, and explain why TTFT drives perceived quality.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/stream_drill.py`:

```python
import asyncio, time


async def fake_stream(text: str, delay: float = 0.1):
    for ch in text:  # simulate token deltas
        await asyncio.sleep(delay)
        yield ch


async def consume(stream, stop_at_chars: int | None = None):
    start = time.perf_counter()
    ttft = None
    buf = []
    async for ch in stream:
        if ttft is None:
            ttft = time.perf_counter() - start  # FIRST token, not last
        buf.append(ch)
        if stop_at_chars and len(buf) >= stop_at_chars:
            break
    return "".join(buf), ttft, time.perf_counter() - start


async def main():
    text, ttft, total = await consume(fake_stream("streaming works", 0.05))
    assert text == "streaming works"
    assert ttft is not None and ttft < total  # TTFT is a fraction of total
    print(f"ttft={ttft:.3f}s total={total:.3f}s text={text!r}")

    # Cancellation: consumer stops, generator cleanup must run
    async def stream_with_cleanup():
        try:
            for ch in "abcdef":
                await asyncio.sleep(0.01)
                yield ch
        finally:
            print("cleanup ran")  # must print on cancel

    task = asyncio.create_task(_drain(stream_with_cleanup()))
    await asyncio.sleep(0.025)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


async def _drain(stream):
    async for _ in stream:
        pass


asyncio.run(main())
```

Expected output: a line like `ttft=0.050s total=0.700s text='streaming works'` (TTFT ≈ one delay, total ≈ 14 delays) and `cleanup ran`. The asserts encode the lesson: TTFT measures the first token; cancellation must unwind the generator.

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate already streams (`_stream_complete`, client.py:265–309) and the CLI prints chunks as they arrive (`_ask_async` in `src/devmate/cli/main.py`). The gap: nobody can see the latency/cost of a streamed call. Add observability to the stream:

- Modify the `ask` command in `projects/04-ai-engineering/devmate/src/devmate/cli/main.py` to accept `--metrics` (boolean, default False).
- When enabled: measure TTFT (request start → first chunk), total time, token usage from the final `StreamingChunk` (carried at `is_final=True`), and $ cost — read it from `cost_tracker` (`src/devmate/obs/cost.py` — `get_recent_requests(1)` after the call, or `estimate_cost`).
- Print `[metrics] ttft=0.31s total=1.14s tokens=812 cost=$0.0042` at the end.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_stream_metrics.py`: a fake stream of 3 chunks with known delays; assert TTFT ≈ first-chunk delay and the metrics string contains `ttft=`, `tokens=`, `cost=`.

**Deliverable:** modified `cli/main.py`, new test. **Acceptance:** `make test` green; when infra is up (`make up` + API keys), `make cli ARGS="ask \"What does devmate do?\" --metrics"` prints the metrics line — TTFT should be far under the P50 total, targeting the lecture's 300 ms.

**Level 3 — Stretch** (production-grade, 3–6 h)

The mid-stream failure problem: a stream is half-delivered when the provider dies. You cannot retry a stream the user already saw. Options: (A) fail fast — show an error marker + partial text (honest, simple); (B) buffer-then-splice — keep a short rolling buffer, retry once, splice from the last emitted token (complex; risk of duplicated/skipped tokens); (C) two-phase — stream a fast cheap model, swap to a better model if the user waits (2× cost, better long answers); (D) SSE event IDs + client-side resume at the API layer. Design the strategy for DevMate's API layer (`src/devmate/api/main.py` exists; SSE lands week 4) with the UX contract ("partial answer + retry button" vs "invisible retry"). **Write an ADR-style justification** into `docs/decisions/` including what the client receives on failure and the implication for the 99.9% uptime target.

**Verify:** drill prints the TTFT/total line and `cleanup ran`; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Nothing appears until the end | `print(..., end="")` without `flush=True`, or chunk buffering | Flush per token; yield as you receive (client already does) |
| TTFT reported in seconds | Measuring total, not first token | Start timer at request, stop at first chunk (your L2) |
| Cancellation hangs | Generator never closed on `CancelledError` | `async with` / `finally` cleanup (drill proves it) |
| Usage is 0 on OpenAI streams | OpenAI sends `usage` only when `stream_options={"include_usage": true}` | Pass it — DevMate's OpenAI `_stream_complete` currently gets usage=0: fix or document |
| Server overwhelms client | No flow control on SSE | Bounded queue + asyncio backpressure between generator and consumer |

**Interview:** "Why does TTFT matter more than total latency for chat UX, and how do you implement streaming correctly?" A strong answer covers: perceived latency (first visible token vs full answer); async iteration + incremental yield; correct TTFT measurement; cancellation/cleanup; per-provider protocol differences (SSE framing, `[DONE]`, usage-in-final-chunk quirks); and the streaming × retries trade-off (you can't retry what the user saw).

### Topic 1.2.c — Structured outputs: tool use / function calling with Pydantic schemas, forced tool_choice, malformed handling

**Mastery =** you can force a schema via `tool_choice`, validate with Pydantic, classify every malformed-output failure, and decide the repair policy (retry once vs fail fast).

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/structured_drill.py`:

```python
import json
from pydantic import BaseModel, ValidationError
from typing import List


class CodeExplanation(BaseModel):
    language: str
    complexity: str  # "simple" | "moderate" | "complex"
    key_concepts: List[str]
    summary: str


def parse_and_validate(content: str, model):
    """Accept JSON text or the Anthropic {'input': {...}} tool-use shape."""
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "input" in data:
            data = data["input"]
        return model(**data)
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid json: {e}") from e
    except ValidationError as e:
        raise ValueError(f"schema mismatch: {e}") from e


valid = json.dumps(
    {
        "language": "python",
        "complexity": "moderate",
        "key_concepts": ["recursion", "memoization"],
        "summary": "Fibonacci.",
    }
)
fixtures = [
    (valid, "valid"),
    (
        json.dumps(
            {
                "input": {
                    "language": "python",
                    "complexity": "simple",
                    "key_concepts": [],
                    "summary": "ok",
                }
            }
        ),
        "tool_use_shape",
    ),
    (json.dumps({"language": "python", "complexity": "moderate"}), "missing_field"),
    (
        json.dumps(
            {
                "language": "python",
                "complexity": "impossible",
                "key_concepts": [],
                "summary": "x",
            }
        ),
        "wrong_enum",
    ),
    (
        json.dumps(
            {
                "language": "python",
                "complexity": "simple",
                "key_concepts": "notalist",
                "summary": "x",
            }
        ),
        "wrong_type",
    ),
    ("{not json at all", "invalid_json"),
]
outcomes = []
for content, name in fixtures:
    try:
        parse_and_validate(content, CodeExplanation)
        outcomes.append((name, "ok"))
    except ValueError:
        outcomes.append((name, "error"))
print(outcomes)
assert outcomes == [
    ("valid", "ok"),
    ("tool_use_shape", "ok"),
    ("missing_field", "error"),
    ("wrong_enum", "error"),
    ("wrong_type", "error"),
    ("invalid_json", "error"),
]
```

Expected output: the 6-tuple outcomes list above — exactly two parse, four fail, each in a distinct category.

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate passes `response_model` to providers and raises `LLMValidationError` on schema mismatch (client.py:234–237 and 418–419) — but a single failure fails the request. Add a **repair-once-then-fail** loop:

- Add `complete_structured(messages, response_model, ...)` to `projects/04-ai-engineering/devmate/src/devmate/llm/client.py` (or extend `LLMClient.complete` with `repair_attempts: int = 1`): on `LLMValidationError`, append a user-role message `"Your previous output failed validation: {error}. Return valid JSON matching the schema."` and call the provider once more; a second failure raises `LLMValidationError`.
- Do NOT trigger provider fallback on repair failure (validation errors must not silently switch providers — matches the existing rule at client.py:576–579).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_structured_output.py` with a fake provider returning a malformed tool_use first and a valid one second; assert exactly 2 provider calls and a parsed `CodeExplanation`; a second test asserts the error propagates after 2 failures.

**Deliverable:** `client.py` change, new test. **Acceptance:** `make test`, `make types`, `make lint` green.

**Level 3 — Stretch** (production-grade, 3–6 h)

Guaranteed JSON under hostile conditions (the fintech bot): a single malformed output is a product incident. Design the reliability stack: forced `tool_choice` (DevMate already forces it, client.py:194); strict Pydantic (`extra="forbid"` — decide forbid vs ignore); an output-token budget that guarantees the JSON closes (`max_tokens` high enough to finish the schema — truncated JSON is the #1 malformation); repair-once with error feedback; and a last-resort repair pass (fence stripping + `json.loads` attempts) before failing. Also decide what the *user* sees on final failure. **Write an ADR-style justification** into `docs/decisions/` covering the stack order and the cost of each layer (extra retries ≈ extra tokens).

**Verify:** drill prints the exact 6-outcome list; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| JSON truncated mid-string | `max_tokens` ran out during generation | Budget output tokens ≥ expected schema size |
| Markdown fences around JSON | Model wrapped output in ```json | Strip fences as a pre-parse repair step |
| Missing/wrong-typed fields | Model skipped fields or hallucinated enums | Pydantic validation → categorized error → repair retry with the error text |
| Tool call ignored | Some models ignore `tool_choice` for complex schemas | Validate post-hoc always; never trust `tool_choice` alone |
| Validation passes, data wrong | Permissive schema (extra fields, loose enums) | `extra="forbid"` + `Literal` enums; semantic checks beyond the schema |

**Interview:** "How do you guarantee structured output from an LLM, and what do you do when it's malformed?" A strong answer covers: forced tool_choice/function calling with a Pydantic-derived schema; why you validate everything post-hoc; the failure taxonomy (truncation, fences, schema mismatch, wrong types, wrong values); the repair policy (one feedback-driven retry, then a typed error, no provider fallback); and the token cost of the reliability stack.

---

## 📚 1.3 Production Patterns

**Real-world problem — Black Friday copilot with a $40k bill and no safety net.** An e-commerce support copilot serves peak traffic: (1) during Black Friday, 429s and 5xx dominate — every client retries at the same moment and makes it worse; (2) finance asks why the monthly bill jumped to $40k and *nobody can answer* — usage is recorded nowhere; (3) a 3-hour Anthropic incident takes the entire product down because there is no fallback; (4) users see raw `HTTPStatusError: 503` text because errors are untyped. The engineer must build the reliability + cost layer: retries that don't herd, per-request cost visibility with budgets, a fallback chain, and a typed error taxonomy — targeting 99.9% uptime (lecture case study).

### Topic 1.3.a — Retries: exponential backoff + jitter, retryable vs non-retryable errors

**Mastery =** you can classify any error as retryable or not, implement backoff + jitter with caps, respect `Retry-After`, and defend the retry budget against thundering herds.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/retry_drill.py`:

```python
import random


def backoff_schedule(initial=1.0, multiplier=2.0, max_wait=30.0, attempts=5):
    return [min(initial * (multiplier**i), max_wait) for i in range(attempts)]


def jittered(base, seed=1):
    rng = random.Random(seed)
    return [b * (0.5 + rng.random()) for b in base]  # full jitter: 0.5x–1.5x


base = backoff_schedule()
print("base:", base)  # [1.0, 2.0, 4.0, 8.0, 16.0]
assert base == [1.0, 2.0, 4.0, 8.0, 16.0]
assert backoff_schedule(attempts=8)[-1] == 30.0  # cap applies

j = jittered(base)
for b, w in zip(base, j):
    assert 0.5 * b <= w <= 1.5 * b  # jitter bounds
print("jitter ok, sample:", [round(x, 2) for x in j])

# Retryability classification — the table that prevents waste
RETRYABLE = {429, 408, 500, 502, 503, 504}
for code, expected in [
    (429, True),
    (500, True),
    (502, True),
    (503, True),
    (504, True),
    (408, True),
    (400, False),
    (401, False),
    (403, False),
    (404, False),
    (422, False),
]:
    assert (code in RETRYABLE) == expected, code
print("classification: 11 status codes classified")
```

Expected output: `base: [1.0, 2.0, 4.0, 8.0, 16.0]`, the jitter line, and the classification line — plus a written note: 429 should also respect the server's `Retry-After` header when present.

**Level 2 — Applied** (DevMate, 1–3 h)

Find and fix a real gap: in `projects/04-ai-engineering/devmate/src/devmate/llm/client.py` the tenacity policy (client.py:148–153) retries only `httpx.TimeoutException` and `httpx.NetworkError`. A 429 raises `LLMRateLimitError` (client.py:205–206) *inside* the decorated function, which tenacity's predicate does not match — so **429s are never retried**; they immediately trigger provider fallback, burning the fallback (and its cost/latency) on a transient limit.

- Extend the policy: `retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError, LLMRateLimitError))`, keeping `wait_exponential_jitter(initial=1, max=30)` and `stop_after_attempt(3)`.
- Add `LLMRateLimitError.retry_after: Optional[float]`, populate it from the `Retry-After` header, and make the wait respect it (hint: compose a custom `wait` that returns `max(backoff, retry_after)` when the exception carries it, or log it in a `before_sleep` hook).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_retry.py` using `httpx.MockTransport`: a transport returning 429, 429, then 200; assert 3 requests hit the wire and the final response succeeds; monkeypatch `asyncio.sleep` to record waits and assert the first wait ≥ the `Retry-After: 2` header value.

**Deliverable:** `client.py` change, new test. **Acceptance:** `make test`, `make types`, `make lint` green. Also log to `mistakes.md`: "429s were falling through to provider fallback without a retry" — a real break-it-on-purpose finding.

**Level 3 — Stretch** (production-grade, 3–6 h)

The coordinated retry storm (Black Friday): 10k clients all receive 429 at once; even with jitter, a naive 3-attempt policy multiplies load 3× into the same rate-limited window — and the fallback chain routes the whole herd to the second provider, which then rate-limits too. Design the full defense: (A) full jitter (0–base, not 0.5–1.5×); (B) `Retry-After` respect everywhere; (C) a client-side token-bucket limiter per model so you never exceed your own share of the limit; (D) a circuit breaker per provider (trip after N consecutive failures, half-open probe, cooldown) so degraded providers are skipped, not hammered; (E) fail-fast policy — interactive chat should degrade to a graceful message rather than consume 3 attempts × 2 providers. **Write an ADR-style justification** into `docs/decisions/` covering the retry budget (max attempts, max total wait, when to give up to the user) and how the pieces compose.

**Verify:** drill prints the three expected lines; `make test` green (retry test shows 3 wire requests); ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Same errors repeat forever | Retrying 400/401/403 | Classify: only 429, 408, 5xx, timeouts are retryable |
| Herd: everyone retries at once | Fixed delay or no jitter | Full jitter + Retry-After |
| Fallback always fires on 429 | 429 not in the retry policy (DevMate's actual gap) | Retry 429 with backoff first; fallback only after attempts are spent |
| Account locked | Retrying 401 with backoff | Never retry auth errors; alert instead |
| Duplicate side effects | Retry of a request that succeeded server-side | Idempotency keys for writes; for LLM reads, track the duplicate cost |

**Interview:** "Which errors do you retry, and how? What happens when everyone retries at once?" A strong answer covers: the retryable set (429/408/5xx/timeouts) vs the fatal set (400/401/403 — retry is waste); exponential backoff with full jitter and caps; `Retry-After`; the retry budget (attempts, max wait); and scale behavior — jitter alone isn't enough; you add client-side rate limiting and circuit breakers so the herd doesn't become a stampede.

### Topic 1.3.b — Token counting & cost tracking: per-request usage, pricing tables, budgets, alerts, $/query

**Mastery =** you can record per-request usage, compute cost per model with a pricing table, set budgets with alerts, and state the $ cost of a single query — including for streamed calls.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/cost_drill.py` — imports the real table DevMate uses (`MODEL_PRICING` in `src/devmate/obs/cost.py`, tuples of $ per 1M input/output tokens):

```python
from devmate.obs.cost import MODEL_PRICING, TokenUsage


def calculate_cost(model: str, usage: TokenUsage) -> float:
    input_price, output_price = MODEL_PRICING.get(model, (0.0, 0.0))
    return (usage.prompt_tokens / 1_000_000) * input_price + (
        usage.completion_tokens / 1_000_000
    ) * output_price


cases = [
    ("gpt-4o", TokenUsage(100_000, 20_000, 120_000), 0.80),
    ("claude-3-5-sonnet-20241022", TokenUsage(100_000, 20_000, 120_000), 0.60),
    ("claude-3-5-haiku-20241022", TokenUsage(100_000, 20_000, 120_000), 0.16),
    ("gpt-4o-mini", TokenUsage(100_000, 20_000, 120_000), 0.027),
]
for model, usage, expected in cases:
    got = calculate_cost(model, usage)
    print(f"{model}: ${got:.4f}  (expect ${expected:.4f})")
    assert abs(got - expected) < 1e-9, model

# $/query and scale: 2,000 prompt + 500 completion on sonnet
q = calculate_cost("claude-3-5-sonnet-20241022", TokenUsage(2_000, 500, 2_500))
print(f"cost per devmate ask (sonnet): ${q:.4f}")  # expect $0.0135
print(f"10k asks/day (sonnet): ${q * 10_000:,.0f}/day")  # expect $135/day
q_haiku = calculate_cost("claude-3-5-haiku-20241022", TokenUsage(2_000, 500, 2_500))
print(f"cost per devmate ask (haiku): ${q_haiku:.4f}")  # expect $0.0036
assert abs(q - 0.0135) < 1e-6 and abs(q_haiku - 0.0036) < 1e-6
```

Expected output: the four model lines ($0.8000, $0.6000, $0.1600, $0.0270), `cost per devmate ask (sonnet): $0.0135`, `10k asks/day (sonnet): $135/day`, `cost per devmate ask (haiku): $0.0036`. Note the $0.002–0.015/query target from the case study: sonnet sits at the top of the range, haiku in the middle.

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate already records usage and cost (`cost_tracker.record_usage` in both providers, `devmate cost` CLI command). The Week-1 DoD demands you can *state the cost of one `devmate ask` in dollars* — and a budget with alerts doesn't exist yet. Add it:

- Extend `projects/04-ai-engineering/devmate/src/devmate/obs/cost.py`: a `Budget` dataclass (`limit_usd: float`, `alert_threshold: float = 0.8`), `CostTracker.set_budget(...)`, `CostTracker.check_budget() -> str` returning `"ok" | "warn" | "exceeded"` (based on `total_cost_usd` vs `limit * threshold`), and `CostTracker.cost_per_query() -> float` (total cost / total requests).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_budget.py` (extend the existing `tests/unit/test_cost.py` patterns): record calls until the threshold and budget are crossed; assert the three states in sequence; assert `cost_per_query()` matches a hand-computed value.
- Then prove the DoD: run one real `devmate ask` (requires `make up` + API keys) and record its $ cost from `make cli ARGS="cost --days 1"` into `mistakes.md` or `notes.md` — that number is the week's deliverable.

**Deliverable:** extended `cost.py`, new test, a written $/query number. **Acceptance:** `make test` green; `make cli ARGS="cost --days 1"` prints a totals table; you can state the cost of one `devmate ask` in dollars.

**Level 3 — Stretch** (production-grade, 3–6 h)

The $40k mystery: nobody can explain the bill. Build the cost-observability stack: (1) attribution — tags per feature/call site so cost rolls up by product area, not just model (extend `CostRecord` with `tags`); (2) per-user tracking for abusive usage patterns; (3) alerting — daily budget + weekly trend + anomaly (cost-per-query > 3× baseline); (4) failed/retried requests counted separately (retries double-bill — your 1.3.a work changes this number); (5) cost levers — semantic cache (`src/devmate/cache/semantic_cache.py`, threshold 0.85) and model cascading (haiku first, escalate on confidence) to move the average query down the $0.002–0.015 range. **Write an ADR-style justification** into `docs/decisions/` covering which levers you enable, the measured before/after $/query, and the alert thresholds you set.

**Verify:** drill prints the five expected cost lines; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Cost reported as $0 | Unknown model name → pricing `(0.0, 0.0)` (DevMate's `test_unknown_model_cost_is_zero` documents this) | Maintain the pricing table; alert on unknown models instead of silently zeroing |
| Usage 0 on streamed OpenAI calls | `stream_options={"include_usage": true}` missing | Set it (DevMate OpenAI `_stream_complete` gap) |
| Bill 2× expected | Retries counted per attempt, not per request | Tag attempts; report unique requests + retry overhead separately |
| Pricing drift | Provider changed prices; table hand-maintained | Centralize `MODEL_PRICING` (done), version it, re-check monthly |
| Budget exceeded silently | No thresholds, no alerts | `set_budget` + `check_budget` before calls (your L2) |

**Interview:** "Your bill doubled. How do you find out why, and what do you build so it never surprises you again?" A strong answer covers: per-request usage captured at the call site (prompt + completion tokens, both providers, including streams); a central pricing table; attribution tags; budgets + alerts; distinguishing retries from unique requests; and the reduction levers — caching, cascading, prompt compression — each with a measured $/query before/after.

### Topic 1.3.c — Provider fallback chain: primary → cheaper → graceful error, auth/rate-limit aware

**Mastery =** you can build a fallback chain, decide which errors must NOT fall back, prevent cascading provider outages with a degraded-state mechanism, and craft the final graceful error.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/fallback_drill.py`:

```python
from dataclasses import dataclass


class RateLimited(Exception):
    pass


class AuthFailed(Exception):
    pass


class ValidationFailed(Exception):
    pass


@dataclass
class FakeProvider:
    name: str
    behavior: str  # "ok" | "rate_limited" | "auth_failed" | "validation"


def call(provider: FakeProvider):
    if provider.behavior == "rate_limited":
        raise RateLimited(f"{provider.name} 429")
    if provider.behavior == "auth_failed":
        raise AuthFailed(f"{provider.name} 401")
    if provider.behavior == "validation":
        raise ValidationFailed(f"{provider.name} bad schema")
    return f"{provider.name}:ok"


def complete_with_fallback(providers, skip=None):
    last = None
    for p in providers:
        if skip and p.name in skip:
            continue
        try:
            return call(p)
        except (RateLimited, AuthFailed) as e:  # transient/config: fall back
            last = e
            continue
        except ValidationFailed as e:  # NEVER fall back on validation
            raise e
    raise RuntimeError(f"all providers failed: {last}")


primary = FakeProvider("anthropic", "rate_limited")
backup = FakeProvider("openai", "ok")
assert complete_with_fallback([primary, backup]) == "openai:ok"  # fallback works
assert (
    complete_with_fallback([FakeProvider("a", "ok"), backup]) == "a:ok"
)  # primary wins

try:
    complete_with_fallback([FakeProvider("a", "validation"), backup])
    raise SystemExit("should have raised")
except ValidationFailed:
    pass
try:
    complete_with_fallback(
        [FakeProvider("a", "auth_failed"), FakeProvider("b", "rate_limited")]
    )
    raise SystemExit("should have raised")
except RuntimeError as e:
    assert "all providers failed" in str(e)
print(
    "fallback: primary-wins, fallback-on-transient, no-fallback-on-validation, final error — all pass"
)
```

Expected output: the pass line — the four invariants every fallback system must hold.

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate's `LLMClient` has the chain `[ANTHROPIC, OPENAI]` (client.py:500–503) and catches `(LLMRateLimitError, LLMAuthError, LLMTimeoutError, httpx.TimeoutException)` for fallback (client.py:571). Strengthen it:

- Add a degraded-provider mechanism in `projects/04-ai-engineering/devmate/src/devmate/llm/client.py`: after 3 consecutive failures on a provider, mark it degraded and skip it for 60 s (in-memory), then re-probe on first request after cooldown.
- Record every fallback event on the trace span (attribute `provider.fallback_from` / `fallback_to`) — the tracer lives in `src/devmate/obs/tracing.py` and is already wrapped around `llm.complete`.
- When ALL providers fail, raise `LLMError("All providers failed: <last_error>")` (exists) — ensure it reaches the CLI as a user-readable message (ties to 1.3.d).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_fallback.py` with fake providers (subclass `BaseLLMProvider`): assert fallback-to-backup on rate limit; assert a degraded provider is skipped and recovered after cooldown (monkeypatch `time.time`); assert validation errors do NOT fall back.

**Deliverable:** `client.py` changes, new test. **Acceptance:** `make test`, `make types`, `make lint` green.

**Level 3 — Stretch** (production-grade, 3–6 h)

The capability-aware routing problem: a naive chain silently degrades quality and leaks cost — falling back from `claude-3-5-sonnet` to `gpt-4o-mini` for a complex refactoring task is a different *product*, and routing everything through the expensive primary wastes the cheap tier. Design a routing matrix for DevMate: per-task model map (analysis → sonnet, simple Q&A → haiku/mini, structured extraction → whichever supports forced tool use), fallback order per tier, degraded-state handling per provider, cost/latency scoring on `LLMResponse` (DevMate already records `latency_ms` and usage), and what happens when the *whole* matrix is down (cache → canned response → graceful error, per the week-7 roadmap chain "primary → cheaper → cached → graceful error"). **Write an ADR-style justification** into `docs/decisions/` covering the matrix, the routing signals, and the 99.9% uptime claim.

**Verify:** drill prints the pass line; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Bugs hidden by fallback | Falling back on validation errors | Never fall back on `LLMValidationError` (DevMate already exempts it, client.py:576–579) |
| Every request pays failure latency | No degraded-state tracking | Circuit-breaker-lite: skip a provider after N failures (your L2) |
| Provider outage becomes YOUR outage | All providers in the same region/cloud | Diverse providers AND a degraded path (cache/canned answer) |
| Quality drop unnoticed | Silent fallback to a weaker model | Log fallback events + span attributes; alert on fallback rate |
| API key leaked in logs | Printing exception text with headers | Redact keys; log only status codes and provider names |

**Interview:** "Design a multi-provider fallback system. What do you log, what do you avoid falling back on, and how do you prevent a provider outage from becoming your outage?" A strong answer covers: ordered chain + degraded-state/circuit breaker; the fallback set (transient + auth/config) vs the never-fallback set (validation); capability-aware per-task routing instead of one global chain; observability (fallback events, per-provider error rates, latency); and the last-resort degradation path (cache, canned answer, typed user-facing error).

### Topic 1.3.d — Timeouts & error taxonomy: connect/read/write timeouts, typed errors, user-facing messages

**Mastery =** you can map every provider/HTTP failure to a typed error, set per-phase timeouts, and produce user-facing messages that never leak internals.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/errors_drill.py`:

```python
class LLMError(Exception):
    pass


class LLMRateLimitError(LLMError):
    pass


class LLMAuthError(LLMError):
    pass


class LLMTimeoutError(LLMError):
    pass


class LLMValidationError(LLMError):
    pass


class LLMConnectionError(LLMError):
    pass


# Simulated httpx exception types (real ones subclass httpx.TimeoutException)
class ConnectTimeout(Exception):
    pass


class ReadTimeout(Exception):
    pass


class WriteTimeout(Exception):
    pass


USER_MESSAGES = {
    LLMRateLimitError: "We're busy right now — try again in a moment.",
    LLMTimeoutError: "The request took too long. Please try again.",
    LLMConnectionError: "We couldn't reach the AI service. Try again shortly.",
    LLMAuthError: "Service configuration error. Contact support.",
    LLMValidationError: "We couldn't process the response. Please rephrase.",
    LLMError: "Something went wrong. Please try again.",
}


def classify(e: Exception) -> LLMError:
    if isinstance(e, (ConnectTimeout, ReadTimeout, WriteTimeout)):
        return LLMTimeoutError("timeout")
    if isinstance(e, ConnectTimeout):
        return LLMConnectionError("connect failed")  # dead branch trap: order matters!
    raise LLMError(f"unclassified: {e}")


def user_message(e: Exception) -> str:
    return USER_MESSAGES[type(e)]


assert isinstance(classify(ConnectTimeout("c")), LLMTimeoutError)  # connect = timeout
assert isinstance(classify(ReadTimeout("r")), LLMTimeoutError)
assert isinstance(classify(WriteTimeout("w")), LLMTimeoutError)
assert (
    user_message(LLMRateLimitError()) == "We're busy right now — try again in a moment."
)
print("error taxonomy: mapping and user messages pass")


# Timeout policy builder
def timeout_policy(connect=10.0, read=60.0, write=30.0, pool=5.0):
    return {"connect": connect, "read": read, "write": write, "pool": pool}


assert timeout_policy() == {"connect": 10.0, "read": 60.0, "write": 30.0, "pool": 5.0}
print("timeout policy: 4 phases configured")
```

Expected output: the two pass lines. (The dead-branch comment teaches the ordering trap: `ConnectTimeout` must be checked as part of the timeout family first.)

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate defines `LLMRateLimitError`, `LLMAuthError`, `LLMTimeoutError`, `LLMValidationError` (client.py:41–57) — but nothing ever *raises* `LLMTimeoutError`; timeouts propagate as raw `httpx.TimeoutException` into the fallback chain, and the CLI shows raw errors. Fix both ends:

- In both providers' `complete` (client.py:204–209 and 387–392), catch `httpx.TimeoutException` and raise `LLMTimeoutError(str(e))` (connect vs read vs write can be distinguished via the `.connect`/`.read`/`.write` hints on `httpx.TimeoutException`).
- In `src/devmate/cli/main.py` `_ask_async`, wrap the RAG query in try/except over the typed `LLMError` subclasses and print user-facing messages (e.g., rate limit → "We're busy right now — try again in a moment."), never raw exception text.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_errors.py`: with a mocked transport that raises `httpx.ReadTimeout`, assert the provider raises `LLMTimeoutError`; assert the CLI handler maps each typed error to its message.

**Deliverable:** `client.py` + `cli/main.py` changes, new test. **Acceptance:** `make test`, `make types`, `make lint` green.

**Level 3 — Stretch** (production-grade, 3–6 h)

The error contract at platform scale: define the full contract for DevMate's API layer — HTTP status codes (429/502/503 for the API itself), a JSON error body with `request_id` (DevMate already has `ErrorResponse` in `schemas.py`), per-operation timeouts (streaming vs batch vs embeddings), and the policy table: retry vs fallback vs fail-fast per error type. Then define SLOs from the 99.9% uptime target and an error budget (e.g., 43 min/month of downtime; budget split: 50% provider failure, 30% rate limit, 20% our bugs) with alerting per bucket. **Write an ADR-style justification** into `docs/decisions/` covering the contract, the policy table, and the error-budget allocation.

**Verify:** drill prints both pass lines; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Users see `HTTPStatusError: 503 ...` | Raw exceptions surface to the UI | Typed errors → friendly messages (your L2) |
| Requests hang for minutes | No connect timeout (`timeout=None`) | Per-phase policy: connect/read/write/pool |
| Everything times out together | One giant timeout for all phases | Distinguish connect (10 s) from read (60 s) |
| Bare `except Exception` hides bugs | Over-broad handlers | Typed hierarchy; catch subclasses explicitly |
| Retrying what already succeeded | Write-timeout on a request that landed | For writes: idempotency; for LLM reads: accept duplicate cost, track it |

**Interview:** "What's your error taxonomy for LLM calls, and how does each error type flow through retry, fallback, and user-facing layers?" A strong answer covers: the typed hierarchy (rate limit, auth, timeout with connect/read/write phases, validation, connection); which errors retry (timeouts, 429, 5xx), which fall back (transient + auth), which fail fast (validation, 400); per-phase timeout policy; the user-facing message per type with no internals leaked; and the error contract + error budget for the platform.

---

## 📚 1.4 Prompt Engineering for Production

**Real-world problem — support automation with an unversioned prompt regression.** A support-automation startup routes tickets to cheap vs expensive models based on prompt output. A prompt change shipped silently — the template lived inline in code, unversioned, untested — and ticket deflection dropped 14% in a week; nobody could roll back, and nobody could say *which change* caused it. Meanwhile, the routing decision itself is only as good as the prompt's output format. The engineer must systematize prompt engineering: a designed system prompt, few-shot examples that measurably help, versioned Jinja2 templates with a regression gate, and chain-of-thought used only where its cost is justified.

### Topic 1.4.a — System prompt design: role, guidelines, output format, anti-patterns

**Mastery =** you can write a system prompt with the three required sections (role, guidelines, output format), audit any prompt against an anti-pattern checklist, and defend it against basic injection.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/system_prompt_drill.py`:

```python
# Rubric: a production system prompt must state (1) ROLE, (2) GUIDELINES
# (concrete, non-contradictory), (3) OUTPUT FORMAT. Anti-patterns: ambiguity,
# contradiction, over-constraint, no output format, leaking secrets, "you must
# never" without a fallback behavior.
REQUIRED_SECTIONS = ("role", "guidelines", "output format")


def audit(prompt: str) -> dict:
    p = prompt.lower()
    return {
        "role": any(k in p for k in ("you are", "your role", "you're a")),
        "guidelines": any(k in p for k in ("guidelines", "rules", "always", "never")),
        "output format": any(
            k in p for k in ("output format", "respond with", "format your")
        ),
        "contradiction": ("always" in p and "never" in p and "unless" not in p),
    }


good = """You are an expert software engineer specializing in Python.
Guidelines:
1. Provide accurate, concise answers with code examples when helpful.
2. Flag security concerns and anti-patterns.
3. If unsure, say so rather than guessing.
Output format: Markdown with code blocks."""
bad = """Help the user. Give the best answer. Do not think too much."""

g, b = audit(good), audit(bad)
assert all(g[s] for s in REQUIRED_SECTIONS), g
assert not g["contradiction"]
assert not all(b[s] for s in REQUIRED_SECTIONS), "bad prompt should miss sections"
print("audit: good prompt passes all required sections, bad prompt fails")
print("bad prompt audit:", b)
```

Expected output: the audit pass line plus the bad prompt's audit dict (role=True, guidelines=False, output_format=False, contradiction=False — with a written note: it has no guidelines and no format, so behavior is whatever the model defaults to).

**Level 2 — Applied** (DevMate, 1–3 h)

DevMate's providers accept a `system` message (client.py:167–184) but there is no central, versioned system prompt — and `src/devmate/llm/prompts/` (a week-1 deliverable per the roadmap) doesn't exist yet. Create the first template:

- Create `projects/04-ai-engineering/devmate/src/devmate/llm/prompts/` with `system_v1.j2`: DevMate's code-assistant persona — role (repo assistant answering from retrieved context), guidelines (cite sources, flag uncertainty, never invent file paths, code in Markdown), output format (structured answer: summary → details → sources).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_system_prompt.py`: render `system_v1.j2` with Jinja2, assert the three required sections are present, and assert a render with no variables still completes (the template must not require variables to render).
- Add a one-line note in the template header: `{# v1 — 2026-08-11 — initial persona. Change via a new version file, never in place. #}`.

**Deliverable:** the prompts folder + `system_v1.j2`, new test. **Acceptance:** `make test` green; `make lint`, `make types` green.

**Level 3 — Stretch** (production-grade, 3–6 h)

Prompt injection defense in depth: DevMate ingests *arbitrary repo files* — untrusted content that can contain "ignore your instructions" text — and answers questions about them. `src/devmate/guards/guardrails.py` already has `PromptInjectionGuardrail`, `SystemPromptExtractionGuardrail`, `CodeExecutionGuardrail`, and output `PIIGuardrail`. Design the full defense: (1) input guardrails (existing patterns — note the regex approach's false-negative rate on novel attacks); (2) system-prompt hardening — explicit instruction that instructions inside retrieved code/docs are data, never commands, plus delimiter policy; (3) output guardrails + a rule that tool calls are only ever made for the schema DevMate defines; (4) a small injection test set (extend the golden cases with adversarial entries). Target: the case study's "zero prompt injection incidents in 3 months" claim. **Write an ADR-style justification** into `docs/decisions/` covering the defense layers, what each layer catches, and the residual risk you accept.

**Verify:** drill prints the audit line; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Model ignores system instructions | User message contradicts system (role confusion) | Keep user content in the user role; validate roles (1.2.a) |
| Vague, variable answers | No output format section | Always specify format explicitly |
| "Always X" + "never Y" both fire | Contradictory guidelines | Audit for contradictions (drill's rubric) |
| System prompt eats context budget | Pages of instructions | Keep it tight; move detail to few-shot/examples |
| Injection succeeds via repo file | Untrusted content treated as instructions | Delimiters + "content is data" instruction + guardrails (your L3) |

**Interview:** "Design a system prompt for a code assistant. What sections, what anti-patterns, how do you prevent injection?" A strong answer covers: role, concrete guidelines (with fallback behavior for uncertainty), explicit output format; anti-patterns (ambiguity, contradiction, over-constraint, no format); versioning the prompt; and injection defense — treating untrusted content as data, guardrails on input and output, and never letting user text redefine the assistant's role.

### Topic 1.4.b — Few-shot: example selection, formatting, when few-shot fails

**Mastery =** you can select representative examples, format them consistently (user/assistant pairs), measure whether they actually help, and know when few-shot is the wrong tool.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/fewshot_drill.py`:

```python
import numpy as np


# Toy embeddings: choose the 2 examples whose average cosine similarity to the
# query is highest (real version: embed with text-embedding-3-small).
def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


query = np.array([1.0, 0.0, 0.5])
examples = {
    "how_to_read_file": np.array([0.9, 0.1, 0.4]),
    "what_is_tuple": np.array([0.1, 0.9, 0.1]),
    "sql_join_vs_lookup": np.array([-0.2, 0.8, 0.2]),
    "error_handling": np.array([0.8, 0.0, 0.6]),
}
scores = {name: cosine(query, vec) for name, vec in examples.items()}
top2 = sorted(scores, key=scores.get, reverse=True)[:2]
print("scores:", {k: round(v, 3) for k, v in scores.items()})
print("selected:", top2)  # expect ['how_to_read_file', 'error_handling']
assert set(top2) == {"how_to_read_file", "error_handling"}


# Formatting: examples must be user/assistant pairs, one per role, exact order
def format_messages(system: str, examples, question: str):
    msgs = [{"role": "system", "content": system}]
    for ex in examples:
        msgs.append({"role": "user", "content": ex["input"]})
        msgs.append({"role": "assistant", "content": ex["output"]})
    msgs.append({"role": "user", "content": question})
    return msgs


exs = [{"input": "q1", "output": "a1"}, {"input": "q2", "output": "a2"}]
msgs = format_messages("sys", exs, "q3")
assert msgs == [
    {"role": "system", "content": "sys"},
    {"role": "user", "content": "q1"},
    {"role": "assistant", "content": "a1"},
    {"role": "user", "content": "q2"},
    {"role": "assistant", "content": "a2"},
    {"role": "user", "content": "q3"},
]
print("formatting: exact user/assistant structure")
```

Expected output: the scores dict, `selected: ['how_to_read_file', 'error_handling']`, and the formatting pass line.

**Level 2 — Applied** (DevMate, 1–3 h)

This topic produces the week's measurement artifact — the 10 golden cases:

- Create `evaluations/prompts/golden-cases/devmate.jsonl` (10 lines, JSONL) with **real questions about this repo** and expected properties, e.g.: `{"id": "gc-001", "question": "What does devmate stats print?", "expected_props": {"contains": ["chunks", "functions"], "not_contains": ["error"], "min_words": 10}, "model": "claude-3-5-sonnet-20241022"}`. Cover: stats, ask flow, chunking, vector store, cost tracking, fallback, guardrails, semantic cache, config, CLI — one per line.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_golden_cases.py`: parse the JSONL; assert exactly 10 entries; assert each has `id`, `question`, `expected_props`, `model`; assert `contains`/`not_contains` are lists.
- Also create `src/devmate/llm/prompts/few_shot_v1.j2` with 1–2 question→answer examples for the `ask` flow (answer with sources, Markdown), rendering as user/assistant pairs.

**Deliverable:** `devmate.jsonl` + few-shot template + test. **Acceptance:** `make test` green; `poetry run python -c "import json; print(len([json.loads(l) for l in open('../../../evaluations/prompts/golden-cases/devmate.jsonl')]))"` prints `10` (adjust the relative path from the DevMate folder).

**Level 3 — Stretch** (production-grade, 3–6 h)

Dynamic few-shot selection: your golden set proves static examples help, but each example costs tokens (a 200-token example × 5 = 1,000 tokens ≈ +$0.003 on sonnet per query) and irrelevant examples actively hurt. Build the dynamic path: embed the query (DevMate's `text-embedding-3-small`, config.py:77) and retrieve the top-k examples by cosine similarity (the semantic-cache code in `src/devmate/cache/semantic_cache.py` already shows the cosine pattern); measure accuracy on the golden set for k=0, 1, 3, 5 and the token cost per k. **Write an ADR-style justification** into `docs/decisions/` with the measured accuracy-vs-cost table and the k you ship.

**Verify:** drill prints the three expected lines; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Examples teach the wrong format | Inconsistent example formatting | Examples must be byte-identical in format to what you want back |
| Token budget eaten by examples | Too many/long examples | Measure lift per example (L3); keep k small |
| Eval scores inflated | Golden-case questions appear in the prompt | Never let eval questions leak into few-shot sets |
| Examples hurt (worse than zero-shot) | Irrelevant or contradictory examples | Similarity-selected, domain-matched examples only |
| Works on golden set, fails live | Overfit to example patterns | Production sample in the eval set, not just hand-made cases |

**Interview:** "When do you use few-shot vs zero-shot, and how do you know your examples actually help?" A strong answer covers: when the format is unusual or the domain is narrow; example selection (representative, similar to real queries, clean format); the measurement discipline — golden set before/after, and the token cost per example; and when few-shot fails — when the model's priors are wrong, examples contradict, or the real distribution differs from the example set (then fine-tune or better grounding instead).

### Topic 1.4.c — Prompt versioning: Jinja2 templates, versioned in git, regression on change

**Mastery =** you can build versioned Jinja2 templates, validate variables before render, estimate tokens before send, and roll back a prompt change via git.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/versioning_drill.py` (requires `jinja2`, available in the DevMate env):

```python
from jinja2 import Environment, BaseLoader, StrictUndefined

env = Environment(loader=BaseLoader(), undefined=StrictUndefined)

TEMPLATES = {
    "code_explanation_v1": """
You are a code explainer. Analyze the following {{ language }} code:
```{{ language }}
{{ code }}
```
Provide: 1. One-sentence summary 2. Key concepts 3. Time/space complexity
""",
    "code_explanation_v2": """
You are a senior engineer reviewing {{ language }} code for production.
Focus on: correctness, performance, security, maintainability.
""",
}
VERSION_DEFAULT = {"code_explanation": "code_explanation_v1"}

def render(name: str, variables: dict) -> str:
    if name not in TEMPLATES:
        raise KeyError(f"template {name} not found")
    return env.from_string(TEMPLATES[name]).render(**variables).strip()

v1 = render("code_explanation_v1", {"language": "python", "code": "def f(): pass"})
v2 = render("code_explanation_v2", {"language": "python"})
assert "senior engineer" in v2 and "You are a code explainer" in v1
assert "{{" not in v1 and "}}" not in v1                    # all variables substituted
try:
    render("code_explanation_v1", {"language": "python"})   # missing "code"
    raise SystemExit("should have raised")
except Exception:
    pass                                                    # StrictUndefined → error, not silent "Undefined"
print("v1:", v1.replace(chr(10), " | "))
print("v2:", v2)
print("versioning: strict render, missing variable raises, default version registered")
```

Expected output: the two rendered lines and the pass line. The lesson: with `StrictUndefined`, a missing variable fails loudly instead of rendering "Undefined" into a prompt.

**Level 2 — Applied** (DevMate, 1–3 h)

Build the versioned prompt system from the roadmap deliverable `devmate/src/devmate/llm/prompts/`:

- Create the three templates from the lecture case study: `code_explanation_v1.j2`, `rag_query_v1.j2`, `agent_planning_v1.j2` (each with a `{# v1 — date — change via new version #}` header).
- Create `projects/04-ai-engineering/devmate/src/devmate/llm/prompts/registry.py`: a `PromptRegistry` that discovers `*.j2` files, keeps a `name → version → template` map with a default version per name, renders with `StrictUndefined`, validates that all declared variables are present before render, and offers `estimate_tokens(rendered: str, model: str) -> int` delegating to `LLMClient.count_tokens` (client.py:585).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_prompts.py`: render each template with sample variables and assert no `{{`/`}}` remain; missing variable raises; unknown template raises; `estimate_tokens` returns a positive int.
- Commit the templates as their own git commit (track rule: commit daily; versioned prompts must have history).

**Deliverable:** `src/devmate/llm/prompts/` (3 templates + `registry.py`) + test. **Acceptance:** `make test`, `make types`, `make lint` green; `git log --oneline` shows the template commit.

**Level 3 — Stretch** (production-grade, 3–6 h)

The regression gate (the section's real-world problem): a prompt change must prove itself before shipping. Build the mini-eval: `projects/04-ai-engineering/devmate/eval/prompt_regression.py` — runs the 10 golden cases (`evaluations/prompts/golden-cases/devmate.jsonl`) through the old and new template versions, checks `expected_props` (contains/not_contains/min_words), and writes a pass/fail report to `evaluations/prompts/reports/` with a verdict line `"SHIP v2 (9/10)"` or `"ROLLBACK (6/10)"`. Then the change policy: PR + eval gate + rollback via git revert. **Write an ADR-style justification** into `docs/decisions/` covering the prompt change-management process (who/what gates a prompt change, what the eval covers, what it can't catch — e.g., distribution shift).

**Verify:** drill prints both rendered lines and the pass line; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Prompt "Undefined" rendered into output | Jinja default lenient undefined | `StrictUndefined` (drill) |
| Template change shipped silently | Edits in place, no version file | New version file per change + git history (your L2 commit) |
| Rollback impossible | No git history / no default-version map | Registry with default version; `git revert` |
| Context overflow after prompt change | Bigger template, no token estimate | `estimate_tokens` before send (registry) |
| Eval passes, production degrades | Eval set too narrow | Golden cases + production sample + regression gate (L3) |

**Interview:** "How do you version prompts and know a change didn't regress quality?" A strong answer covers: Jinja2 templates as files, versioned in git, never edited in place; a registry with default versions; strict variable validation and token estimation before send; a golden-case regression gate with a ship/rollback verdict; and the honest limits — eval catches format regressions, not distribution drift, so you also monitor production quality signals.

### Topic 1.4.d — Chain-of-thought: when to ask for reasoning, structured CoT output, cost/latency trade-off

**Mastery =** you can decide when reasoning earns its cost, force structured CoT output (reasoning + answer), parse it reliably, and quantify the latency/$ premium.

**Level 1 — Drill** (mechanics, 20–45 min)

`projects/04-ai-engineering/devmate/labs/cot_drill.py`:

```python
from devmate.obs.cost import MODEL_PRICING, TokenUsage

COT_SYSTEM = """Answer with two sections:
Reasoning: <your step-by-step thinking>
Final: <the answer only>"""

def parse_cot(text: str) -> str:
    """Extract the Final section; raise if absent."""
    import re
    m = re.search(r"Final:\s*(.+)", text, re.DOTALL)
    if not m:
        raise ValueError("no Final section")
    return m.group(1).strip()

fixtures = [
    ("Reasoning: Step 1: check the index.\nStep 2: run the test.\nFinal: It is O(n).", "It is O(n)."),
    ("Reasoning: compare fields.\nFinal: use UUID as the key.", "use UUID as the key."),
    ("Final: 42", "42"),
    ("Reasoning: no conclusion reached.", None),      # missing Final → error
]
for text, expected in fixtures:
    try:
        got = parse_cot(text)
        assert got == expected, (got, expected)
    except ValueError:
        assert expected is None
print("CoT parsing: 4 fixtures classified (3 ok, 1 error)")

# Cost trade-off: forcing reasoning adds ~300 output tokens on sonnet
def cost(model: str, prompt: int, completion: int) -> float:
    ip, op = MODEL_PRICING.get(model, (0.0, 0.0))
    return prompt / 1_000_000 * ip + completion / 1_000_000 * op

direct = cost("claude-3-5-sonnet-20241022", 2_000, 500)
cot = cost("claude-3-5-sonnet-20241022", 2_000, 800)   # +300 reasoning tokens
print(f"direct=${direct:.4f} cot=${cot:.4f} premium=${cot - direct:.4f}")
assert abs((cot - direct) - 0.0045) < 1e-6             # 300/1e6 * $15
```

Expected output: the CoT parsing line, `direct=$0.0135 cot=$0.0180 premium=$0.0045`, all asserts pass.

**Level 2 — Applied** (DevMate, 1–3 h)

Give DevMate a structured CoT path:

- Add to `projects/04-ai-engineering/devmate/src/devmate/llm/schemas.py`:
  ```python
  class ReasonedAnswer(BaseModel):
      reasoning: str  # step-by-step thinking, never shown in final UI
      answer: str  # the user-facing answer
  ```
- Create `projects/04-ai-engineering/devmate/src/devmate/llm/reasoning.py`: `complete_with_reasoning(client, messages, model=None)` — calls `client.complete(..., response_model=ReasonedAnswer)` (the client already forces `tool_choice` when `response_model` is set, client.py:187–194) and returns the validated `ReasonedAnswer`.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_reasoning.py` with a fake provider returning a tool_use input `{"reasoning": "...", "answer": "..."}`; assert the parsed object's fields; assert a malformed tool_use (missing `answer`) raises `LLMValidationError`.

**Deliverable:** `schemas.py` addition, new `reasoning.py`, test. **Acceptance:** `make test`, `make types`, `make lint` green.

**Level 3 — Stretch** (production-grade, 3–6 h)

The reasoning policy: forcing CoT on every request costs +$0.0045/query and +latency on sonnet (drill numbers) — the case study's $0.002–0.015 range only survives if reasoning is used selectively. Design a router: task-complexity signals (question length, retrieved-context size, uncertainty heuristics) decide between a cheap direct path (haiku, no CoT), a direct path (sonnet, no CoT), and a reasoned path (sonnet + `ReasonedAnswer`). Measure on the golden cases: accuracy by path, latency by path, $/query by path, and the blended $/query at a realistic mix (e.g., 60% haiku / 30% sonnet / 10% reasoned). **Write an ADR-style justification** into `docs/decisions/` covering the policy, the signals, and the revisit conditions.

**Verify:** drill prints the two expected lines; `make test` green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| User sees the reasoning | Parsed the whole CoT text as the answer | Structured `ReasonedAnswer`; UI renders `answer` only (your L2) |
| Latency doubles on simple queries | CoT everywhere | Router: cheap/direct path for simple tasks (L3) |
| Reasoning contradicts the final answer | Model talked itself into a corner | Keep reasoning private; final answer is what ships; validate on golden cases |
| Small models can't force tool_choice | Model lacks tool-use reliability | Only send CoT schemas to capable models; fallback path returns plain text |
| Cost blowup | CoT output tokens unaccounted | Track reasoning premium in cost records (1.3.b) |

**Interview:** "When do you use chain-of-thought in production, how do you structure it, and what does it cost?" A strong answer covers: when it helps (multi-step, math, planning, ambiguity) vs when it's wasted (lookup, formatting); structured CoT via a schema (reasoning + answer) so the UI never shows reasoning; the cost model — reasoning tokens × output price, plus latency; and the router — a cheap direct path for simple queries, reasoned path only where it measurably improves golden-case scores.

---

## 🚀 Definition of done for this workbook

Work through the checklist top-to-bottom; every box needs evidence, not "I understand it".

- [ ] **§1.1** — All 4 drills pass (`tokenization_drill`, `attention_drill`, `sampling_drill`, `training_drill`); Applied artifacts exist (`ensure_within_context` in `client.py`, `devmate/docs/llm-internals.md`, `sampling.py`, `devmate/docs/fine-tune-or-not.md`); 4 Stretch ADRs written.
- [ ] **§1.2** — All 3 drills pass; Applied artifacts exist (validated `LLMRequest` in `schemas.py`, `--metrics` in `cli/main.py`, repair-once in `client.py`); 3 Stretch ADRs written.
- [ ] **§1.3** — All 4 drills pass; Applied artifacts exist (429 retry policy, `Budget` in `obs/cost.py`, degraded-provider fallback, typed errors + CLI messages); 4 Stretch ADRs written.
- [ ] **§1.4** — All 4 drills pass; Applied artifacts exist (`system_v1.j2`, `evaluations/prompts/golden-cases/devmate.jsonl` with exactly 10 cases, `prompts/registry.py` with 3 versioned templates committed to git, `ReasonedAnswer` + `reasoning.py`); 4 Stretch ADRs written.
- [ ] **Week-1 Definition of Done (roadmap §4):** every LLM call appears as a Langfuse trace with token count and cost — verified in Langfuse (`make up` + `LANGFUSE_*` keys, `src/devmate/obs/tracing.py` exports spans with `usage.prompt_tokens`, `usage.completion_tokens`, `latency_ms`).
- [ ] **Week-1 Definition of Done:** you can state the cost of one `devmate ask` in dollars — written in `notes.md`/`mistakes.md` with the command output that produced it (`make cli ARGS="cost --days 1"`).
- [ ] **Break-it-on-purpose experiments (roadmap §4) logged to `projects/04-ai-engineering/devmate/mistakes.md`:** kill the network mid-stream; send a 200k-token prompt; force a malformed structured output. Each entry: what broke, the symptom, the fix.
- [ ] **Quality gates:** `make test`, `make types`, `make lint` all green after every Applied task; `make ci` green at the end of the week.
- [ ] **Interview practice:** all 15 Interview questions answered out loud, 2-minute recordings, per track §7 (Technical English).

*Workbook created 2026-08-11 under ADR-0006 — every topic traces to a DevMate concept or an interview answer.*
