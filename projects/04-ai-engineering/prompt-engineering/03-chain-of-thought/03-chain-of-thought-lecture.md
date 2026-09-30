# Prompt Engineering 03: Chain-of-Thought

## Topic Overview

Chain-of-thought (CoT) asks the model to reason step by step before giving the answer. On
multi-step problems, the intermediate reasoning improves accuracy, because the model works
through the problem instead of jumping to a guess, and the steps act as a scratchpad it can check
against. It is one of the highest-leverage prompt techniques for reasoning tasks and one of the
most misapplied.

This lecture covers the CoT prompt, why it helps, when it helps, when it does not, and the token
cost. The discipline is to match the technique to the task: CoT on a multi-step problem is a
large accuracy gain for a modest cost, and CoT on a simple lookup is pure cost for no gain.

There is also a design choice about whether the reasoning is shown to the user or kept internal,
which matters for latency, cost, and the nature of the product.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write a chain-of-thought prompt.
2. Explain why intermediate steps improve accuracy.
3. Choose when CoT helps and when it does not.
4. Account for the token cost of the reasoning.
5. Decide whether to show or hide the reasoning.
6. Combine CoT with few-shot examples where useful.

## Prerequisites

- Prompt Engineering 01 (prompt structure) and 02 (few-shot) for the surrounding techniques.

---

## 1. What CoT Does

### The step-by-step instruction

CoT asks the model to show its reasoning before the answer:

```markdown
## Task
Solve the problem step by step, then give the answer.

## Steps
1. Identify the problem type
2. Recall the relevant concepts
3. Plan the solution
4. Execute each step
5. Verify the answer
```

### Why steps help

Multi-step problems have intermediate states. A model that reasons through them is less likely to
make a compounding error, because each step can be checked against the previous one. The steps
are the model's scratchpad, and the scratchpad reduces the chance of a silent wrong turn.

### The mechanism

The model generates tokens conditioned on its own prior tokens. Reasoning tokens become context
for the answer token, so the model that writes the steps is a model that reads them. This is why
the reasoning is not decoration; it changes the computation.

## 2. Why Its Helps

### Compounding errors

A wrong intermediate state propagates. CoT reduces the chance of skipping an intermediate state
entirely, which is the most damaging failure on a multi-step problem. It does not make the model
infallible; it makes the common failure mode less likely.

### The scratchpad

The visible steps are the model's working memory for the problem. They let the model hold
sub-results without relying on a single forward pass, which is exactly what multi-step problems
need.

### The verification step

A final verify step ("check the answer") catches some errors before they are emitted. It is not
reliable on its own, but it is cheap and it helps.

## 3. When CoT Helps

### The tasks

CoT helps on multi-step, reasoning-heavy tasks:

```python
MULTI_STEP = {"math", "science_reasoning", "code_debugging", "logic"}
assert cot_helps("math")
assert cot_helps("logic")
```

These are tasks with intermediate states where a wrong step can be caught.

### Why these tasks

They have structure the model can reason over, and they have a correct answer that the reasoning
can reach. The steps are load-bearing.

## 4. When CoT Does Not Help

### The non-reasoning tasks

CoT does not help on simple factual questions, creative writing, or translation:

```python
assert not cot_helps("simple_fact")   # no steps needed
assert not cot_helps("translation")   # not a reasoning task
```

### Why not

A simple lookup has no intermediate state, so the reasoning adds tokens and latency for no
accuracy. Creative writing and translation are not stepwise reasoning; the steps add structure
where the task wants fluency.

### The cost of misapplication

CoT on a non-reasoning task is pure cost: more tokens, more latency, and sometimes worse output,
because the imposed structure fights the task.

## 5. The Cost

### Tokens for reasoning

CoT consumes tokens for the reasoning:

```python
def token_cost(steps, tokens_per_step):
    return steps * tokens_per_step
```

Five steps at twenty tokens each is a hundred extra tokens per call, paid every time.

### The tradeoff

The cost is justified when the accuracy gain is real, which is measured (Prompt Engineering 04),
not assumed. A CoT prompt that does not improve accuracy on the task is cost without benefit.

### The budget interaction

The reasoning competes with retrieved evidence for the context budget (RAG System 09). On a
budget-tight RAG prompt, CoT reasoning can crowd out the evidence and lower quality, so the
trade must be measured in the full pipeline, not in isolation.

## 6. Show or Hide the Reasoning

### Showing

Showing the reasoning lets the user follow the logic and builds trust, and it can be required for
auditability. It also spends output tokens and latency.

### Hiding

Some providers support a hidden reasoning mode where the model reasons internally and emits only
the answer. This saves output tokens and can reduce latency, at the cost of transparency.

### The decision

The choice is a product decision: transparency against cost and latency. For a grounded
knowledge task, showing the reasoning that cites evidence is often valuable; for a high-volume
lookup, hiding it saves cost.

## 7. CoT with Few-Shot

### Demonstrating the reasoning

The most effective CoT prompts often demonstrate the reasoning through examples (Prompt
Engineering 02): the examples show the steps in the target format, and the model imitates the
step-by-step style.

### The combination

Few-shot teaches the format and the reasoning pattern; CoT ensures the reasoning happens. Together
they are stronger than either alone on a well-matched task.

### The caution

The examples must show the reasoning the model should use. An example that jumps to the answer
teaches the model to jump.

## Real-World Application

- Using CoT for a DevMate task that requires multi-step code reasoning, and verifying the
  accuracy gain on the eval set.
- Avoiding CoT for a simple Athar verse lookup, where the steps add cost for no gain.
- Hiding the reasoning for a high-volume extraction task to save output tokens.
- Demonstrating the step-by-step format through few-shot examples for a structured reasoning task.

## Common Mistakes

1. **CoT for simple factual questions.** Cost with no accuracy gain.
2. **No steps at all.** The model jumps to a guess.
3. **CoT for non-reasoning tasks.** Structure imposed where it does not help.
4. **Ignoring the token cost.** The reasoning is paid on every call.
5. **Reasoning that crowds out evidence.** The budget is spent on steps, not sources.
6. **Examples that skip the reasoning.** The model learns to skip it.

## Key Takeaways

1. CoT shows reasoning before the answer, and the steps act as a scratchpad that reduces
   compounding errors.
2. It helps on multi-step tasks (math, logic, code debugging) and not on simple, factual, or
   creative tasks.
3. The reasoning costs tokens on every call; measure the gain against the cost.
4. The reasoning competes with evidence for the context budget in a RAG prompt.
5. Showing or hiding the reasoning is a product tradeoff, and few-shot examples are the strongest
   way to demonstrate the step-by-step format.

## Self-Check Questions

1. Why do intermediate steps improve accuracy on a multi-step problem?
2. Give one task where CoT helps and one where it does not, with the reason.
3. How does the reasoning interact with the RAG context budget?
4. When would you hide the reasoning, and what does it cost?
5. How does few-shot interact with CoT, and what is the caution?

## Further Reading / Connections

- Prompt Engineering 02 (few-shot) — demonstrating the reasoning.
- Prompt Engineering 04 (prompt evaluation) — measuring whether CoT helps.
- RAG System 09 (long context processing) — the budget the reasoning consumes.
- AI Evaluation 04 (LLM-as-judge) — grading reasoning quality.
