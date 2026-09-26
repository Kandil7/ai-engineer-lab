# Prompt Engineering — Educational AI Tutor

Prompt design and optimization for the ThanaweyaGPT educational AI assistant.
Covers template design, few-shot examples, chain-of-thought reasoning, and
Arabic language handling.

---

## Prompt Templates

### System Prompt Structure

Every prompt follows a consistent structure:

```markdown
## Role
You are [specific role] specializing in [domain].

## Context
[Relevant background information]

## Task
[Clear, specific instruction]

## Constraints
[Rules and limitations]

## Output Format
[Expected response structure]

## Examples
[Few-shot examples if applicable]
```

### Core Prompts

| Prompt               | Purpose                              | Location                    |
| -------------------- | ------------------------------------ | --------------------------- |
| `tutor-system.md`    | Base system prompt for the tutor     | `.ai/prompts/roles/`        |
| `math-solver.md`     | Math problem-solving chain-of-thought| `.ai/prompts/tasks/`        |
| `science-explainer.md`| Science concept explanation         | `.ai/prompts/tasks/`        |
| `code-reviewer.md`   | Code review and feedback             | `.ai/prompts/critics/`      |

---

## Few-Shot Examples

### Math Problem Solving

```markdown
## Example 1
**Problem:** Solve for x: 2x + 5 = 15
**Solution:**
1. Subtract 5 from both sides: 2x = 10
2. Divide both sides by 2: x = 5
3. Verify: 2(5) + 5 = 15 ✓
**Answer:** x = 5

## Example 2
**Problem:** Find the derivative of f(x) = 3x² + 2x - 1
**Solution:**
1. Apply power rule to each term
2. d/dx(3x²) = 6x
3. d/dx(2x) = 2
4. d/dx(-1) = 0
**Answer:** f'(x) = 6x + 2
```

### Science Explanation

```markdown
## Example
**Question:** Why does ice float on water?
**Approach:**
1. Consider molecular structure of water
2. Compare density of ice vs liquid water
3. Explain hydrogen bonding
**Response:** Ice floats because water molecules form a crystal lattice when frozen,
spreading molecules farther apart than in liquid form. This makes ice less dense
(0.917 g/cm³) than liquid water (1.000 g/cm³), causing it to float.
```

---

## Chain-of-Thought for Problem Solving

### Step-by-Step Framework

```markdown
## Problem Analysis
1. **Identify** — What type of problem is this?
2. **Recall** — What concepts/formulas apply?
3. **Plan** — What steps will solve it?
4. **Execute** — Work through each step
5. **Verify** — Check the answer makes sense
```

### When to Use CoT

- Multi-step math problems
- Science reasoning questions
- Code debugging and analysis
- Logic puzzles and proofs

### When NOT to Use CoT

- Simple factual questions ("What is the capital of France?")
- Creative writing prompts
- Translation tasks

---

## Arabic Language Handling

### Bilingual Prompt Design

```markdown
## Language Rule
- If the user writes in Arabic, respond in Arabic
- If the user writes in English, respond in English
- For technical terms, provide both Arabic and English in parentheses
- Code and math notation remain in English/Latin script
```

### Arabic-Specific Considerations

1. **RTL text direction** — ensure proper rendering in UI
2. **Arabic numerals** — accept both `٠١٢٣` and `0123`
3. **Diacritics** — handle optional tashkeel gracefully
4. **Dialects** — default to Modern Standard Arabic (MSA)
5. **Mixed content** — Arabic text with English technical terms

### Prompt Template (Arabic)

```markdown
## التعليمات
أنت مدرس خبير متخصص في [الموضوع]. قم بتعليم الطالب بطريقة واضحة وم step-by-step.

## قواعد اللغة
- استخدم العربية الفصحى
- المصطلحات التقنية: اكتبها بالعربية ثم بالإنجليزية بين قوسين
- الأمثلة: استخدم أرقام عربية أو إنجليزية حسب ما يكتبه الطالب
```

---

## Prompt Evaluation

### Metrics

| Metric            | Description                          | Target  |
| ----------------- | ------------------------------------ | ------- |
| Accuracy          | Correct factual information          | > 95%   |
| Relevance         | Stays on topic                       | > 90%   |
| Helpfulness       | Actually solves the student's problem| > 85%   |
| Clarity           | Easy to understand                   | > 90%   |
| Bilingual quality | Equivalent quality in both languages | > 85%   |

### Testing Process

1. Create test cases from real student questions
2. Run through prompt variations
3. Score against evaluation criteria
4. Select best-performing prompt
5. Monitor in production with feedback loop

---

## Getting Started

```bash
# Review existing prompts
ls .ai/prompts/roles/
ls .ai/prompts/tasks/

# Run the prompt and registry validators
./tests/prompts/validate.ps1
./tests/registries/validate.ps1

# Follow the prompt workflow
# .ai/workflows/evaluation/prompt-regression.md
```
