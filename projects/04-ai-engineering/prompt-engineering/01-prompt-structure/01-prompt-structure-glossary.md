# Prompt Engineering 01: Prompt Structure — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Role | The behavior the model adopts | tutor |
| Context | The background information | domain facts |
| Task | The core instruction | specific |
| Constraints | The output bounds | length, tone |
| Output format | The response shape | JSON, list |
| Structured prompt | The five-section contract | consistent |
| Vague task | An unspecific instruction | bad output |

---

## Alphabetical Glossary

### Constraints

**Definition:** The output bounds: length, tone, what to avoid, what to
include. Without them the model improvises the bounds.

**Example:**
```markdown
## Constraints
- Answer in Arabic
- Max 3 sentences
- No speculation
```

**Related concepts:** Task

---

### Context

**Definition:** The background information the model needs to answer. The
second section of the structured prompt.

**Example:**
```markdown
## Context
The student is in grade 10.
```

**Related concepts:** Role

---

### Output format

**Definition:** The response shape: a list, a JSON object, a step-by-step
answer. Makes the output parseable and predictable.

**Example:**
```markdown
## Output Format
Return a JSON object with "answer" and "steps".
```

**Related concepts:** Constraints

---

### Role

**Definition:** The behavior the model adopts. The first section of the
structured prompt.

**Example:**
```markdown
## Role
You are a tutor specializing in physics.
```

**Related concepts:** Context

---

### Structured prompt

**Definition:** The five-section contract: role, context, task,
constraints, output format. Consistent structure enables evaluation.

**Example:**
```markdown
## Role ... ## Context ... ## Task ... ## Constraints ... ## Output Format ...
```

**Related concepts:** Task

---

### Task

**Definition:** The core instruction: what to do, with what input, toward
what result. Must be specific.

**Example:**
```markdown
## Task
Explain why ice floats, in two sentences.
```

**Related concepts:** Constraints

---

### Vague task

**Definition:** An unspecific instruction that produces vague output.

**Example:**
```markdown
## Task
Explain ice.
```

**Related concepts:** Task

---

## Related Concepts

- **Few-shot**: examples extend the structure (topic 02)
- **Chain-of-thought**: the task asks for reasoning (topic 03)
- **Prompt evaluation**: structure enables comparison (topic 04)

## Key Takeaways

1. Five sections: role, context, task, constraints, format.
2. The task must be specific.
3. Constraints bound the output.
4. The format shapes the output.
5. Consistency enables evaluation.