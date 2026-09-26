# Module 1: LLM Fundamentals & API Integration

**Week 1 of Active Track** | **Duration: 3-4 hours theory + 4-5 hours practice**

> 🏋️ **Practice workbook:** [`../practice/01-llm-fundamentals-practice.md`](../practice/01-llm-fundamentals-practice.md) —
> every section has a real-world problem and every topic has Drill → Applied (DevMate) → Stretch levels with verification.

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Explain** how LLMs work at a high level (tokenization, attention, training objectives)
2. **Integrate** LLM APIs (Anthropic, OpenAI) with proper error handling, retries, and streaming
3. **Design** effective prompts using system prompts, few-shot examples, and structured outputs
4. **Implement** token counting, cost tracking, and latency monitoring
5. **Build** a production-ready LLM client with fallback providers
6. **Debug** common API issues (rate limits, timeouts, validation errors)

---

## 📚 Lecture Content

### 1.1 How LLMs Work (The 20% You Need)

#### Tokenization
```
Text → Tokenizer → [Token IDs] → Model → [Token IDs] → Detokenizer → Text
```

Key concepts:
- **Tokens ≠ Words**: ~1.3 tokens per English word
- **Context Window**: Max tokens (input + output) the model can process
- **Vocabulary**: Fixed set of tokens the model understands (e.g., 100K for GPT-4)

```python
import tiktoken

# Count tokens for any model
encoding = tiktoken.encoding_for_model("gpt-4")
tokens = encoding.encode("Hello, world!")
print(f"Tokens: {tokens}")  # [9906, 11, 1917, 0]
print(f"Count: {len(tokens)}")  # 4
```

#### The Transformer Architecture (Simplified)
```
Input Embeddings → Positional Encoding → 
  [Attention → FeedForward → Add&Norm] × N layers →
Output Projection → Softmax → Next Token Probabilities
```

**What you need to know:**
- **Self-Attention**: Each token attends to all other tokens
- **Causal Masking**: Prevents attending to future tokens (autoregressive)
- **Temperature**: Controls randomness in sampling (0 = deterministic, 1 = creative)

#### Training Objectives
| Phase | Objective | Data | Compute |
|-------|-----------|------|---------|
| Pre-training | Next token prediction | Trillions of tokens | Massive (GPU months) |
| Fine-tuning | Instruction following | Curated datasets | Moderate |
| RLHF/RLAIF | Human preference alignment | Preference pairs | Moderate |

---

### 1.2 API Integration Patterns

#### Basic Request Structure
```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0.1,
    system="You are a helpful code assistant.",
    messages=[{"role": "user", "content": "Explain dependency injection in Python"}],
)

print(response.content[0].text)
```

#### Streaming Responses (Essential for UX)
```python
import asyncio
import anthropic


async def stream_response(prompt: str):
    client = anthropic.AsyncAnthropic()

    async with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()  # Newline at end


# Usage
asyncio.run(stream_response("Write a haiku about debugging"))
```

#### Structured Outputs (Function Calling / Tool Use)
```python
from pydantic import BaseModel
from typing import List


class CodeExplanation(BaseModel):
    language: str
    complexity: str  # "simple", "moderate", "complex"
    key_concepts: List[str]
    summary: str
    line_by_line: List[str]


# With Anthropic
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        {
            "name": "explain_code",
            "description": "Explain code with structured output",
            "input_schema": CodeExplanation.model_json_schema(),
        }
    ],
    tool_choice={"type": "tool", "name": "explain_code"},
    messages=[
        {
            "role": "user",
            "content": "Explain this: def fib(n): return n if n<2 else fib(n-1)+fib(n-2)",
        }
    ],
)

# Parse structured result
tool_use = response.content[0]
explanation = CodeExplanation(**tool_use.input)
```

---

### 1.3 Production Patterns

#### 1. Retry with Exponential Backoff
```python
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter


class ResilientLLMClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)

    @retry(
        wait=wait_exponential_jitter(initial=1, max=30),
        stop=stop_after_attempt(3),
        retry=lambda e: isinstance(e, (httpx.TimeoutException, httpx.NetworkError)),
    )
    async def complete(self, messages, model, **kwargs):
        response = await self.client.post(
            "https://api.anthropic.com/v1/messages",
            json={"model": model, "messages": messages, **kwargs},
            headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
        )
        response.raise_for_status()
        return response.json()
```

#### 2. Token Counting & Cost Tracking
```python
from dataclasses import dataclass
from typing import Dict


@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


# Pricing per 1M tokens (update regularly)
PRICING = {
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def calculate_cost(model: str, usage: TokenUsage) -> float:
    pricing = PRICING.get(model, {"input": 0, "output": 0})
    input_cost = (usage.prompt_tokens / 1_000_000) * pricing["input"]
    output_cost = (usage.completion_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost


# Track every call
class CostTracker:
    def __init__(self):
        self.total_cost = 0.0
        self.call_count = 0

    def record(self, model: str, usage: TokenUsage):
        cost = calculate_cost(model, usage)
        self.total_cost += cost
        self.call_count += 1
        return cost
```

#### 3. Provider Fallback Chain
```python
from enum import Enum


class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class MultiProviderClient:
    def __init__(self):
        self.providers = {
            Provider.ANTHROPIC: AnthropicProvider(),
            Provider.OPENAI: OpenAIProvider(),
        }
        self.fallback_order = [Provider.ANTHROPIC, Provider.OPENAI]

    async def complete(self, messages, **kwargs):
        last_error = None

        for provider in self.fallback_order:
            try:
                return await self.providers[provider].complete(messages, **kwargs)
            except RateLimitError:
                print(f"{provider.value} rate limited, trying next...")
                continue
            except AuthError:
                print(f"{provider.value} auth failed, trying next...")
                continue
            except Exception as e:
                last_error = e
                print(f"{provider.value} error: {e}")
                continue

        raise Exception(f"All providers failed. Last error: {last_error}")
```

---

### 1.4 Prompt Engineering for Production

#### System Prompt Template
```python
SYSTEM_PROMPT = """You are an expert software engineer specializing in {domain}.

Guidelines:
1. Provide accurate, concise answers with code examples when helpful
2. Always explain your reasoning for non-trivial solutions
3. Flag security concerns, performance issues, or anti-patterns
4. Use {language} for code examples unless otherwise specified
5. If unsure, say so rather than guessing

Output format: {output_format}
"""
```

#### Few-Shot Examples
```python
FEW_SHOT_EXAMPLES = [
    {
        "input": "How do I read a file in Python?",
        "output": "Use `open()` with a context manager:\n\n```python\nwith open('file.txt', 'r') as f:\n    content = f.read()\n```",
    },
    {
        "input": "What's the difference between list and tuple?",
        "output": "**List**: Mutable, ordered, allows duplicates. `[1, 2, 3]`\n**Tuple**: Immutable, ordered, allows duplicates. `(1, 2, 3)`\n\nUse tuples for fixed collections, lists for dynamic ones.",
    },
]


def build_prompt(user_question: str) -> List[Dict]:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.format(
                domain="Python backend development",
                language="Python",
                output_format="Markdown with code blocks",
            ),
        }
    ]

    for ex in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": ex["input"]})
        messages.append({"role": "assistant", "content": ex["output"]})

    messages.append({"role": "user", "content": user_question})
    return messages
```

#### Prompt Versioning (Critical for Production)
```python
# Store prompts as Jinja2 templates
PROMPT_TEMPLATES = {
    "code_explanation_v1": """
You are a code explainer. Analyze the following {{ language }} code:

```{{ language }}
{{ code }}
```

Provide:
1. One-sentence summary
2. Key concepts used
3. Time/space complexity
4. Potential improvements
""",
    "code_explanation_v2": """
You are a senior engineer reviewing {{ language }} code for a production system.

Code to review:
```{{ language }}
{{ code }}
```

Focus on:
- Correctness & edge cases
- Performance & scalability
- Security vulnerabilities
- Maintainability & readability
- Testability

Format as structured review with severity levels.
""",
}
```

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Token** | Basic unit of text processing (subword, word, or character) |
| **Context Window** | Maximum tokens a model can process in one request |
| **Temperature** | Sampling randomness parameter (0-2, lower = more deterministic) |
| **Top-p / Nucleus Sampling** | Alternative to temperature, samples from top cumulative probability |
| **System Prompt** | Persistent instructions that define model behavior |
| **Few-Shot** | Providing examples in the prompt to guide behavior |
| **Function Calling** | Model outputs structured JSON to invoke predefined functions |
| **Streaming** | Receiving response tokens incrementally as generated |
| **Rate Limit** | Maximum requests/tokens per time window |
| **Exponential Backoff** | Retry strategy with increasing delays between attempts |
| **Jitter** | Random delay added to prevent thundering herd |
| **Prompt Injection** | Attack where user input manipulates model behavior |
| **Hallucination** | Model generating plausible but incorrect information |
| **Grounding** | Constraining model output to verified sources |
| **Top-k Sampling** | Samples from the k most likely tokens; 1 = greedy |
| **Frequency Penalty** | Logit penalty proportional to a token's repeat count (−2 to 2, OpenAI) |
| **Presence Penalty** | One-time logit penalty if a token appeared at all (−2 to 2, OpenAI) |
| **Open Weights** | Downloadable weights; check the license (Apache/MIT vs community-use terms) |
| **Self-Hosted Inference** | Serving a model on your own GPU (e.g., Ollama); VRAM decides what fits |
| **Inference Provider** | Hosted API serving open-weight models (e.g., HF Inference Providers routing) |
| **Safety Identifier** | Salted hash of an end-user ID sent for abuse attribution; never raw PII |

---

## 🏋️ Exercises

### Exercise 1.1: Basic API Client (30 min)
Build a simple wrapper around Anthropic/OpenAI API with:
- Sync and async methods
- Token counting
- Basic error handling

```python
# Starter code
class SimpleLLMClient:
    def __init__(self, api_key: str, provider: str = "anthropic"):
        pass
    
    def complete(self, prompt: str, **kwargs) -> str:
        pass
    
    async def acomplete(self, prompt: str, **kwargs) -> str:
        pass
    
    def count_tokens(self, text: str) -> int:
        pass
```

### Exercise 1.2: Streaming with Progress (45 min)
Create a streaming client that:
- Yields tokens as they arrive
- Shows a progress indicator
- Handles cancellation

```python
async def stream_with_progress(client, prompt):
    """Stream response with token-by-token display."""
    # Implement
    pass
```

### Exercise 1.3: Structured Output Parser (45 min)
Implement a robust parser for structured outputs that:
- Validates against Pydantic schema
- Handles malformed responses gracefully
- Retries on validation failure

### Exercise 1.4: Cost-Aware Client (60 min)
Extend your client to:
- Track cumulative cost per session
- Warn when approaching budget
- Support model routing (cheap model for simple tasks)

```python
class CostAwareClient:
    def __init__(self, budget_usd: float = 10.0):
        self.budget = budget_usd
        self.spent = 0.0
    
    async def complete(self, prompt: str, model: str = None) -> str:
        # Auto-select model based on remaining budget
        # Track and report cost
        pass
    
    def get_usage_report(self) -> dict:
        pass
```

### Exercise 1.5: Prompt Template System (45 min)
Build a versioned prompt template system:
- Jinja2-based templates
- Variable validation
- Version management
- Token estimation before sending

### Exercise 1.6: Model-Choice Spike + Local Fallback Probe (60 min)
Score two models for one DevMate path using the §1.5.a rubric (no API key needed —
pricing pages plus your latency notes), then probe local inference:
- `ollama pull llama3.2`, then call `generate` with a JSON-schema `format` and
  `options={"temperature": 0.0}`; assert the parsed keys
- Record the VRAM verdict for your card (Q4 rule of thumb: ~0.5 GB per 1B params
  plus context) and which DevMate paths may run locally

---

## ❓ Quiz

### Question 1
What does the `temperature` parameter control in LLM APIs?
- A) Maximum response length
- B) Randomness/creativity of output
- C) API timeout duration
- D) Model version selection

### Question 2
Which HTTP status code indicates rate limiting?
- A) 400
- B) 401
- C) 429
- D) 500

### Question 3
What is the purpose of `stream=True` in LLM API calls?
- A) Compress the response
- B) Receive tokens incrementally as generated
- C) Enable function calling
- D) Use a different model

### Question 4
Why is exponential backoff with jitter recommended for retries?
- A) It's faster than fixed delays
- B) Prevents thundering herd when many clients retry simultaneously
- C) Reduces API costs
- D) Improves response quality

### Question 5
What is "prompt injection"?
- A) Injecting code into the prompt
- B) User input designed to override system instructions
- C) Adding few-shot examples
- D) Streaming the prompt

### Question 6
How many tokens approximately equal one English word?
- A) 0.5
- B) 1.0
- C) 1.3
- D) 2.0

### Question 7
What is the difference between `top_p` and `temperature`?
- A) They're the same thing
- B) `top_p` samples from top cumulative probability, `temperature` scales logits
- C) `temperature` is for OpenAI, `top_p` for Anthropic
- D) `top_p` controls length, `temperature` controls creativity

### Question 8
Why should you version your prompts?
- A) To track which prompt produced which output
- B) To enable rollback when quality degrades
- C) For A/B testing different prompts
- D) All of the above

### Question 9
What is the difference between `frequency_penalty` and `presence_penalty`?
- A) They're aliases for the same parameter
- B) Frequency scales with repeat count, presence applies once per repeated token
- C) Presence only works with streaming
- D) Frequency controls length, presence controls creativity

### Question 10
A 7B model in Q4 quantization needs roughly how much VRAM, and does it fit a 16 GB card?
- A) ~14 GB, barely fits
- B) ~500 MB, fits dozens
- C) ~5 GB with context overhead, fits comfortably
- D) VRAM doesn't matter for inference

### Question 11
Why does `InferenceClient(provider="auto")` require a model argument?
- A) Routing looks up the provider mapping for that model
- B) It doesn't; the provider is always fixed
- C) The model name is the API key
- D) Auto mode only works locally

### Question 12
What should you send as OpenAI's `safety_identifier`?
- A) The user's raw email address
- B) Your organization's API key
- C) A salted hash of a per-user ID (username hash, email hash, session ID)
- D) Nothing; the field doesn't exist

### Question 13
Your agent repeats the same tool call. What bounds the worst-case cost?
- A) Raising `frequency_penalty` to 2.0
- B) The step cap and loop detection; penalties only soften repetition
- C) Lowering temperature to 0
- D) Switching to a bigger model

---

## 💻 Code Challenge

### Challenge: Build a Multi-Provider LLM Gateway

**Requirements:**
1. Support Anthropic and OpenAI with unified interface
2. Automatic fallback on rate limits / errors
3. Per-request cost tracking with daily/monthly budgets
4. Request/response logging with correlation IDs
5. Streaming support for both providers
6. Structured output validation with Pydantic
7. Prompt template versioning

**Bonus:**
- Add Redis caching for repeated prompts
- Implement semantic caching (similar queries return cached results)
- Add request timeout and cancellation
- Build a simple CLI to test the gateway

**Evaluation Criteria:**
- Clean architecture with dependency injection
- Proper error handling and retry logic
- Comprehensive tests (unit + integration)
- Documentation with usage examples
- Cost tracking accuracy verified against provider dashboards

---

## 📋 Case Study: DevMate LLM Layer

**Context**: Building the LLM abstraction layer for DevMate (Week 1 deliverable)

**Decisions Made:**
1. **Provider**: Anthropic primary (better code reasoning), OpenAI fallback
2. **Streaming**: Mandatory - users perceive latency differently
3. **Structured Outputs**: Pydantic schemas for all internal tool calls
4. **Observability**: Langfuse tracing from day one
5. **Cost Tracking**: Per-request, aggregated by model/provider

**Code Structure:**
```
devmate/llm/
├── client.py          # Multi-provider client with fallback
├── schemas.py         # Pydantic models for structured outputs
├── prompts/           # Versioned Jinja2 templates
│   ├── rag_query_v1.j2
│   ├── code_explanation_v1.j2
│   └── agent_planning_v1.j2
├── cost.py            # Token counting + cost calculation
└── tracing.py         # Langfuse integration
```

**Key Metrics Achieved:**
- P50 latency: 1.2s (streaming TTFT: 300ms)
- Cost per query: $0.002-0.015 depending on complexity
- 99.9% uptime with fallback
- Zero prompt injection incidents in 3 months

---

## 🚀 Production Checklist

- [ ] API keys stored in secret manager (not code)
- [ ] Retry logic with exponential backoff + jitter
- [ ] Streaming implemented for all user-facing calls
- [ ] Structured outputs validated with Pydantic
- [ ] Cost tracking per request + alerts at thresholds
- [ ] Request/response logging (no PII)
- [ ] Rate limit handling with user-friendly messages
- [ ] Prompt injection detection on input
- [ ] PII detection/redaction on output
- [ ] Fallback provider configured and tested
- [ ] Prompt templates versioned in git
- [ ] Integration tests with mocked providers
- [ ] Load testing completed
- [ ] Documentation with examples

---

## 📚 Further Reading

1. **Anthropic API Docs**: https://docs.anthropic.com
2. **OpenAI API Docs**: https://platform.openai.com/docs
3. **Prompt Engineering Guide**: https://promptingguide.ai
4. **"AI Engineering" by Chip Huyen** - Chapters 1-3
5. **Langfuse Docs**: https://langfuse.com/docs
6. **Tenacity Retry Library**: https://github.com/jd/tenacity