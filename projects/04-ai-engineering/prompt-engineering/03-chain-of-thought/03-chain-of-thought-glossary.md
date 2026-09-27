# Prompt Engineering 03: Chain-of-Thought — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Chain-of-thought | Reasoning step by step before the answer | scratchpad |
| Scratchpad | The visible intermediate steps | self-check |
| Multi-step problem | Requires intermediate states | math, logic |
| Compounding error | An early mistake amplified | prevented by steps |
| Token cost | The reasoning consumes tokens | justified by gain |
| Non-reasoning task | No steps needed | creative, translation |
| Visible reasoning | The steps are shown | checkable |

---

## Alphabetical Glossary

### Chain-of-thought

**Definition:** Asking the model to reason step by step before answering.
The intermediate steps improve accuracy on multi-step problems.

**Example:**
```markdown
## Task
Solve step by step, then give the answer.
```

**Related concepts:** Scratchpad

---

### Compounding error

**Definition:** An early mistake amplified by later steps. The scratchpad
reduces it by making each step checkable.

**Example:**
```python
# a wrong first step propagates through the rest
```

**Related concepts:** Chain-of-thought

---

### Multi-step problem

**Definition:** A problem with intermediate states: math, science
reasoning, code debugging, logic.

**Example:**
```markdown
# solve for x in a multi-step equation
```

**Related concepts:** Chain-of-thought

---

### Non-reasoning task

**Definition:** A task that does not need steps: simple facts, creative
writing, translation. CoT adds tokens without accuracy.

**Example:**
```markdown
# "What is the capital of France?" needs no steps
```

**Related concepts:** Chain-of-thought

---

### Scratchpad

**Definition:** The visible intermediate steps. The model checks its own
work through them.

**Example:**
```markdown
## Steps
1. Subtract 5
2. Divide by 2
```

**Related concepts:** Chain-of-thought

---

### Token cost

**Definition:** The reasoning consumes tokens. Justified when the accuracy
gain is real.

**Example:**
```python
# 5 reasoning steps x 20 tokens = 100 extra tokens
```

**Related concepts:** Chain-of-thought

---

### Visible reasoning

**Definition:** The steps are shown, making the reasoning checkable.

**Example:**
```markdown
## Steps
1. ...
2. ...
```

**Related concepts:** Scratchpad

---

## Related Concepts

- **Prompt structure**: CoT is a task instruction (topic 01)
- **Few-shot**: examples can demonstrate the steps (topic 02)
- **Prompt evaluation**: CoT is compared against direct answering (topic 04)

## Key Takeaways

1. CoT shows the reasoning before the answer.
2. The steps are the scratchpad.
3. CoT helps on multi-step problems.
4. CoT does not help on simple or creative tasks.
5. The token cost is considered.