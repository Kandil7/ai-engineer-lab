# Prompt Engineering 04: Prompt Evaluation

## 🎯 Topic Overview

A prompt is a hypothesis until it is measured. Prompt evaluation runs the
prompt against test cases, scores the output, and compares variations.
This lecture covers the test cases, the metrics, and the comparison
discipline.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Build test cases from real inputs
2. Score output against the metrics
3. Compare prompt variations
4. Select the best-performing prompt
5. Monitor in production

---

## 1. The Test Cases

Test cases come from real inputs: student questions, user queries, edge
cases. Each case has an expected behavior. The cases are fixed, so
variations are compared on the same inputs. The roadmap's exit test:
"test cases are built from real inputs."

```python
cases = [
    {"input": "ما هو العدد الأولي؟", "expected": "a number with two divisors"},
    {"input": "Explain ice.", "expected": "density + hydrogen bonding"},
]
```

## 2. The Metrics

The metrics score the output: accuracy, relevance, helpfulness, clarity.
Each metric has a target. The roadmap's exit test: "output is scored
against the metrics."

| Metric | Target |
|--------|--------|
| Accuracy | > 95% |
| Relevance | > 90% |
| Helpfulness | > 85% |
| Clarity | > 90% |

## 3. Comparing Variations

Variations are compared on the same test cases: the same input, different
prompts, scored output. The comparison is the evidence for the choice.
The roadmap's exit test: "variations are compared."

## 4. Selecting the Best

The best prompt is the one that scores highest on the metrics, not the
one that reads best. The selection is evidence-based. The roadmap's exit
test: "the best-performing prompt is selected."

## 5. Production Monitoring

The selected prompt is monitored in production with a feedback loop. A
prompt that degrades in production is re-evaluated. The roadmap's exit
test: "the prompt is monitored in production."

## Common Mistakes

- No test cases (quality assumed).
- Scoring without a rubric.
- Comparing variations on different inputs.
- Choosing the prompt that reads best.
- No production monitoring.

## Key Takeaways

1. Test cases come from real inputs.
2. Output is scored against the metrics.
3. Variations compare on the same cases.
4. The best prompt is the best-scoring one.
5. Production is monitored with feedback.