# Prompt Engineering 02: Few-Shot

## Topic Overview

Few-shot examples show the model the expected input-output pattern by demonstration. A couple of
well-chosen examples often teach the format and the reasoning better than a paragraph of
instructions, because the model imitates what it sees rather than interpreting what it is told.
Examples are the strongest signal in a prompt and the easiest to get wrong.

This lecture covers what few-shot does, how to select examples that cover the pattern rather than
the volume, why the examples must match the target format exactly, the token cost, and the bias
examples introduce. The recurring lesson is that examples teach by imitation, so a sloppy or
unrepresentative set teaches sloppy or unrepresentative behavior.

Few-shot is not always the answer. When a clear instruction suffices, zero-shot is cheaper and
equally good, and the discipline is to use examples only when the model demonstrably needs them.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what few-shot examples teach.
2. Choose examples that cover the pattern, not the volume.
3. Write examples in the exact target format.
4. Account for the token cost of examples.
5. Recognize and manage example bias.
6. Decide when zero-shot is sufficient.

## Prerequisites

- Prompt Engineering 01 (prompt structure) for the role, context, and format.

---

## 1. What Few-Shot Does

### Teaching by imitation

Few-shot examples demonstrate the input-output pattern. The model generalizes from them: it
learns the format and the reasoning by imitation rather than by inference from instructions.
This is why a good example can do more than a paragraph of prose:

```markdown
## Example 1
**Problem:** Solve for x: 2x + 5 = 15
**Solution:**
1. Subtract 5: 2x = 10
2. Divide by 2: x = 5
**Answer:** x = 5
```

### Why imitation is powerful and risky

Imitation is powerful because the model copies structure faithfully. It is risky for the same
reason: whatever the examples do, correct or not, the model will do. The examples are the
specification.

### The relationship to the format

Few-shot and the output format are linked. The examples are the format, demonstrated. A format
described in prose and contradicted by the examples will lose to the examples.

## 2. Choosing Examples

### Coverage, not volume

Examples are chosen to cover the pattern, not to fill space. Two examples showing different
cases (an easy one and a hard one) teach more than five similar ones:

```python
def covers_pattern(examples, cases):
    """Examples cover the pattern when each case appears."""
    covered = {e["case"] for e in examples}
    return cases <= covered
```

### The failure of redundancy

Five near-identical examples cover one case and teach the model that the pattern is narrow. The
model then fails on the cases the examples did not show. Coverage is the goal; volume is not.

### Selecting the cases

Choose the cases that represent the real input distribution and its edge cases. For an Arabic
task, that means examples across the query types the system sees, not five phrasings of the same
question.

## 3. The Format

### Exact match

Examples are written in the exact target format. The model imitates the format, so a sloppy
example teaches sloppy output. If every example has a citation, the model produces citations; if
some omit it, the model treats the citation as optional.

```python
assert covers_pattern(examples, {"easy", "hard"})
```

### Consistency across examples

All examples share one format. Mixing formats (some with a chain of thought, some without) teaches
the model that the format is variable, which produces variable output. The example set is a
contract with the model.

## 4. The Cost

### Tokens per example

Every example consumes tokens:

```python
def token_cost(examples, tokens_per_example):
    return len(examples) * tokens_per_example
```

Two examples at 100 tokens each cost 200; five cost 500. The cost is paid on every call, so it
multiplies across the system's lifetime.

### The tradeoff

The cost is traded against the quality gain. Examples are worth their tokens when they measurably
improve the output (Prompt Engineering 04); adding examples that do not improve output is pure
cost.

### The budget interaction

Examples count against the context budget (RAG System 09). A prompt stuffed with examples leaves
less room for retrieved evidence, which can lower the answer quality even as the format improves.
The whole prompt is one budget.

## 5. Example Bias

### The bias

Examples bias the model toward the demonstrated pattern. If all examples are math, the model
answers everything like math; if all are formal, the tone is formal. This is the same imitation
that makes few-shot work, seen from the other side.

### Managing it

Manage the bias by covering the range of expected inputs: include the easy and the hard, the
short and the long, the formal and the casual, if all appear in production. The example set
should look like the input distribution.

### Uncovering it

Bias is uncovered by testing on inputs unlike the examples. If the model fails on those, the
example set is too narrow, and the fix is coverage, not more instructions.

## 6. When Zero-Shot Suffices

### The test

Zero-shot is cheaper: no examples, fewer tokens. Use it when a clear instruction produces the
right output. Add examples only when the measurement (Prompt Engineering 04) shows they help.

### Why the default is zero-shot

Examples are a cost and a bias. Starting zero-shot and adding examples only where they are needed
keeps the prompt lean and the bias minimal. The discipline is evidence, not habit.

### The escalation

If zero-shot fails on format or reasoning, add one or two covering examples. If it still fails,
the problem may be the task, not the prompt.

## Real-World Application

- Adding two examples (one easy, one hard) to teach an Arabic answer format that zero-shot got
  wrong.
- Writing examples that all carry a citation so the model learns citations are mandatory.
- Measuring that a third example does not improve output and dropping it to save tokens.
- Checking that examples cover the corpus's query types so the model does not over-fit to one.

## Common Mistakes

1. **Too many similar examples.** Redundancy without coverage.
2. **Sloppy example format.** The model imitates the sloppiness.
3. **Ignoring the token cost.** Every call pays for the examples.
4. **Examples that bias the output.** A narrow set produces narrow behavior.
5. **Few-shot when zero-shot suffices.** Cost and bias for no gain.
6. **Mixed formats across examples.** The model learns that format is optional.

## Key Takeaways

1. Few-shot teaches the pattern by imitation, which is powerful and risky.
2. Cover the pattern, not the volume; redundant examples teach a narrow behavior.
3. Examples must match the target format exactly; they are the specification.
4. Examples cost tokens on every call and bias the output; both are managed by coverage and
   measurement.
5. Start zero-shot and add examples only when the measurement shows they help.

## Self-Check Questions

1. Why is imitation both the strength and the risk of few-shot?
2. Why do two covering examples beat five similar ones?
3. How do examples interact with the context budget?
4. How do you uncover and fix example bias?
5. When should you not use few-shot?

## Further Reading / Connections

- Prompt Engineering 01 (prompt structure) — where examples sit in the prompt.
- Prompt Engineering 03 (chain-of-thought) — often demonstrated through examples.
- Prompt Engineering 04 (prompt evaluation) — measuring whether examples help.
- RAG System 09 (long context processing) — the context budget examples consume.
