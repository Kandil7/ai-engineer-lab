# Prompt Engineering 02: Few-Shot — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Few-shot | Examples demonstrating the pattern | input-output pairs |
| Zero-shot | No examples, instruction only | the baseline |
| Example selection | Cover the pattern, not the volume | easy + hard |
| Target format | The exact output shape | imitated |
| Token cost | The context budget consumed | per example |
| Example bias | The model over-follows the examples | all math |
| Pattern coverage | The range of expected inputs | managed bias |

---

## Alphabetical Glossary

### Example bias

**Definition:** The model over-follows the demonstrated pattern. If all
examples are math, the model answers everything like math.

**Example:**
```python
# all math examples -> math-style answers to everything
```

**Related concepts:** Pattern coverage

---

### Example selection

**Definition:** Choosing examples that cover the pattern. Two different
cases teach more than five similar ones.

**Example:**
```python
# one easy case, one hard case
```

**Related concepts:** Pattern coverage

---

### Few-shot

**Definition:** Demonstrating the input-output pattern with examples. The
model generalizes by imitation.

**Example:**
```markdown
## Example 1
**Problem:** 2x + 5 = 15
**Answer:** x = 5
```

**Related concepts:** Zero-shot

---

### Pattern coverage

**Definition:** The range of expected inputs the examples span. Manages
the bias.

**Example:**
```python
# math, science, and code examples
```

**Related concepts:** Example bias

---

### Target format

**Definition:** The exact output shape the examples demonstrate. The model
imitates it — a sloppy example teaches sloppy output.

**Example:**
```markdown
## Answer: x = 5
```

**Related concepts:** Few-shot

---

### Token cost

**Definition:** The context budget consumed by the examples. Long prompts
cost more per call.

**Example:**
```python
# 5 examples x 100 tokens = 500 tokens per call
```

**Related concepts:** Few-shot

---

### Zero-shot

**Definition:** No examples, instruction only. The baseline to compare
few-shot against.

**Example:**
```markdown
## Task
Solve for x.
```

**Related concepts:** Few-shot

---

## Related Concepts

- **Prompt structure**: examples extend the five sections (topic 01)
- **Chain-of-thought**: examples can demonstrate reasoning (topic 03)
- **Prompt evaluation**: few-shot is compared against zero-shot (topic 04)

## Key Takeaways

1. Examples teach the pattern by imitation.
2. Cover the pattern, not the volume.
3. Examples match the target format.
4. Examples cost tokens.
5. Examples bias the output.