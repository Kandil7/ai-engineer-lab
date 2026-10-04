# Prompt Engineering Cheat Sheet

## Prompting Techniques

### Zero-Shot Prompting
```markdown
Classify the following text as positive, negative, or neutral:
"The product works well but the shipping was slow."
```

### Few-Shot Prompting
```markdown
Classify the sentiment of customer messages.

Examples:
Message: "Absolutely love this product!" → Positive
Message: "Terrible quality, want a refund." → Negative
Message: "It works as expected." → Neutral

Now classify:
Message: "The product works well but the shipping was slow."
```

### Chain-of-Thought (CoT)
```markdown
Solve this problem step by step:
A store sells shirts for $25 each. If you buy 3 or more, you get a 10% discount. 
How much do 5 shirts cost?

1. Base price: 5 × $25 = $125
2. Discount: 10% of $125 = $12.50
3. Final: $125 - $12.50 = $112.50
```

---

## Structured Output

### JSON Output
```markdown
Extract information as JSON:
{
  "name": "string",
  "email": "string", 
  "company": "string",
  "role": "string"
}
```

### Table Output
```markdown
Compare databases in a table:
| Feature | PostgreSQL | MySQL | SQLite |
|---------|------------|-------|--------|
| Type | | | |
| Best For | | | |
```

---

## Token Budgeting

### Estimating Tokens
- 1 token ≈ 4 characters (English)
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words
- For 4,000 token limit: system ~500, input ~1,500, output ~2,000

### Efficient Prompting
```markdown
# Bad
Please carefully analyze the following text and provide a detailed summary 
of the main points, making sure to include all important information while 
keeping it concise and easy to understand.

# Good
Summarize this text in 3 bullet points: [text]
```

---

## Role Design

### Expert Persona
```markdown
You are a senior backend engineer with 10 years of experience.
Specializing in Python, PostgreSQL, and distributed systems.
Focus on: performance, security, maintainability.
```

### Domain Expert
```markdown
You are a financial analyst specializing in SaaS metrics.
You understand: MRR, ARR, churn, LTV, CAC, burn rate.
```

### Teacher Persona
```markdown
You are a patient technical instructor.
Explain concepts from simple to complex.
Use analogies and real-world examples.
```

---

## Anti-Hallucination Patterns

### Grounding with Sources
```markdown
Answer based ONLY on the provided context. If the answer isn't in the context, 
say "I don't have enough information."

Context: [document]
Question: What is the company's revenue?
```

### Confidence Indicators
```markdown
Answer the question and rate your confidence (high/medium/low):
- High: Information is explicitly stated
- Medium: Inferred from multiple sources
- Low: Based on general knowledge
```

### Fallback Patterns
```markdown
If you're not sure, say "I'm not certain" rather than guessing.

Use phrases like:
- "Based on the provided information..."
- "The data suggests..."
- "One possible interpretation is..."
```

---

## Advanced Patterns

### Prompt Chaining
```markdown
Step 1: Extract key facts from this complaint: [complaint]
Step 2: Classify severity (low/medium/high): [facts]
Step 3: Generate response at [severity] level: [facts + severity]
```

### Template Variables
```markdown
You are helping a {role} at a {company_size} {industry} company.
Challenge: {challenge}
Resources: {resources}
```

### Meta-Prompting
```markdown
Here is a prompt I'm using: [prompt]

Improve this prompt by:
1. Making it clearer
2. Adding specificity
3. Reducing ambiguity
4. Adding constraints where helpful
```

---

## Common Patterns

### Code Review
```markdown
Review this code for:
1. Bugs and logic errors
2. Performance issues
3. Security vulnerabilities
4. Code style and readability
5. Error handling

For each issue: severity, line numbers, description, suggested fix
```

### Data Extraction
```markdown
Extract fields from this text:
- Entity name, Date, Amount, Status

Return as JSON. If missing, use null.
```

### Summarization
```markdown
Summarize this document:
- Executive summary (1 paragraph)
- Key points (3-5 bullets)
- Action items (if any)
```

---

## Evaluation Metrics

### Prompt Quality Score
Rate on 1-5: Clarity, Specificity, Completeness, Efficiency, Robustness

### Output Quality Metrics
Evaluate: Accuracy, Relevance, Completeness, Format, Tone

---

## This Repo's Prompt Architecture

### Directory Structure
```
prompts/
├── templates/           # Base templates
├── workflows/           # Multi-step prompts
├── evaluations/         # Eval scores
└── variants/            # A/B test variants
```

### Naming Convention
```
{category}-{purpose}-{version}.md

Examples:
- code-review-backend-v1.md
- data-extraction-customer-v2.md
- summarization-technical-v1.md
```

### Metadata Header
```markdown
---
id: code-review-backend-v1
category: code-review
purpose: Review Python backend code
version: 1
tokens: 850
eval_score: 4.2/5
created: 2024-01-15
updated: 2024-01-20
---
```

---

## Quick Reference

| Technique | Use Case |
|-----------|----------|
| Zero-shot | Simple, clear tasks |
| Few-shot | Complex patterns |
| CoT | Reasoning tasks |
| Structured output | JSON, tables, lists |
| Role design | Domain expertise |
| Anti-hallucination | Fact-sensitive tasks |

---

*Last updated: 2026-08-06*
