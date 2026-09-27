# Prompt Engineering 03: Chain-of-Thought

## 🎯 Topic Overview

Chain-of-thought (CoT) asks the model to reason step by step before
answering. The intermediate steps improve accuracy on multi-step problems.
This lecture covers the CoT prompt, when it helps, and when it does not.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write a CoT prompt
2. Explain why the steps improve accuracy
3. Choose when CoT helps
4. Avoid CoT where it does not help
5. Keep the reasoning visible

---

## 1. What CoT Does

CoT asks the model to show its reasoning before the answer. The steps
force the model to work through the problem instead of jumping to a
guess. The roadmap's exit test: "chain-of-thought is used for multi-step
problems."

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

## 2. Why It Helps

Multi-step problems have intermediate states. A model that reasons through
them is less likely to make a compounding error. The steps are the
scratchpad — the model checks its own work. The roadmap's exit test: "the
reasoning is visible."

## 3. When CoT Helps

CoT helps on multi-step problems: math, science reasoning, code
debugging, logic. It does not help on simple factual questions, creative
writing, or translation. The roadmap's exit test: "CoT is used where it
helps."

## 4. When CoT Does Not Help

A simple factual question does not need steps — CoT adds tokens without
accuracy. Creative writing and translation are not reasoning tasks. The
discipline is to match the technique to the task.

## 5. The Cost

CoT consumes tokens for the reasoning. The cost is justified when the
accuracy gain is real. The roadmap's exit test: "the token cost is
considered."

## Common Mistakes

- CoT for simple factual questions.
- No steps (the model jumps to the answer).
- Hidden reasoning (no scratchpad).
- CoT for non-reasoning tasks.
- Ignoring the token cost.

## Key Takeaways

1. CoT shows the reasoning before the answer.
2. The steps are the scratchpad.
3. CoT helps on multi-step problems.
4. CoT does not help on simple or creative tasks.
5. The token cost is considered.