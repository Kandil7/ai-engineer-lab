# Prompt Engineering 01: Prompt Structure

## 🎯 Topic Overview

A prompt is a contract with the model. A consistent structure — role,
context, task, constraints, output format — makes the contract explicit
and the output predictable. This lecture covers the five sections and the
discipline of structured prompts.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write the five prompt sections
2. Make the task instruction specific
3. State the constraints explicitly
4. Specify the output format
5. Keep the structure consistent

---

## 1. The Five Sections

A structured prompt has five sections: role, context, task, constraints,
and output format. The role sets the behavior; the context supplies the
background; the task states the instruction; the constraints bound the
output; the format shapes it. The roadmap's exit test: "prompts follow a
consistent structure."

```markdown
## Role
You are a tutor specializing in [domain].

## Context
[Relevant background]

## Task
[Clear, specific instruction]

## Constraints
[Rules and limitations]

## Output Format
[Expected response structure]
```

## 2. The Task

The task is the core instruction. It must be specific: what to do, with
what input, toward what result. A vague task produces a vague output. The
roadmap's exit test: "the task instruction is specific."

## 3. The Constraints

Constraints bound the output: length, tone, what to avoid, what to
include. Without constraints, the model improvises the bounds. The
roadmap's exit test: "constraints are explicit."

## 4. The Output Format

The output format shapes the response: a list, a JSON object, a
step-by-step answer. A specified format makes the output parseable and
predictable. The roadmap's exit test: "the output format is specified."

## 5. Consistency

The same structure across prompts makes them maintainable and testable. A
consistent structure is the foundation of prompt evaluation — variations
are compared within the same shape.

## Common Mistakes

- A prompt with no structure.
- A vague task instruction.
- No constraints (the model improvises bounds).
- No output format (unparseable output).
- Inconsistent structure across prompts.

## Key Takeaways

1. Five sections: role, context, task, constraints, format.
2. The task must be specific.
3. Constraints bound the output.
4. The format shapes the output.
5. Consistency enables evaluation.