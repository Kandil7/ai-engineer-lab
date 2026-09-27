# Prompt Engineering 02: Few-Shot

## 🎯 Topic Overview

Few-shot examples show the model the expected input-output pattern. A
couple of well-chosen examples teach the format and the reasoning better
than a paragraph of instructions. This lecture covers example selection,
the pattern, and the cost.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Choose examples that cover the pattern
2. Write examples in the target format
3. Explain the token cost of examples
4. Avoid example bias
5. Use zero-shot when examples do not help

---

## 1. What Few-Shot Does

Few-shot examples demonstrate the input-output pattern. The model
generalizes from the examples — it learns the format and the reasoning by
imitation. The roadmap's exit test: "few-shot examples are used."

```markdown
## Example 1
**Problem:** Solve for x: 2x + 5 = 15
**Solution:**
1. Subtract 5: 2x = 10
2. Divide by 2: x = 5
**Answer:** x = 5
```

## 2. Choosing Examples

Examples are chosen to cover the pattern, not the volume. Two examples
that show different cases — an easy one and a hard one — teach more than
five similar ones. The roadmap's exit test: "examples cover the pattern."

## 3. The Format

Examples are written in the exact target format. The model imitates the
format — a sloppy example teaches sloppy output. The roadmap's exit test:
"examples match the target format."

## 4. The Cost

Every example consumes tokens. A long prompt with many examples costs more
per call and can exceed the context budget. The cost is the tradeoff
against the quality gain. The roadmap's exit test: "the token cost is
considered."

## 5. Example Bias

Examples bias the model toward the demonstrated pattern. If all examples
are math, the model answers everything like math. The bias is managed by
covering the range of expected inputs.

## Common Mistakes

- Too many similar examples.
- Sloppy example format.
- Ignoring the token cost.
- Examples that bias the output.
- Few-shot when zero-shot suffices.

## Key Takeaways

1. Examples teach the pattern by imitation.
2. Cover the pattern, not the volume.
3. Examples match the target format.
4. Examples cost tokens.
5. Examples bias the output.