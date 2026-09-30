# Prompt Engineering 01: Prompt Structure

## Topic Overview

A prompt is a contract with the model. It specifies what role to play,
what context to use, what task to perform, what constraints to follow,
and what output to produce. A well-structured prompt makes the model's
behavior predictable; a poorly structured one produces inconsistent,
unparseable output.

The difference between a good and a bad prompt is not magic — it is
structure. Five sections, consistently applied: role, context, task,
constraints, output format. Each section has a purpose, and omitting one
creates a specific failure mode.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write the five prompt sections with clear purpose
2. Make the task instruction specific and verifiable
3. State constraints explicitly (bounds, tone, exclusions)
4. Specify the output format for parseability
5. Diagnose prompt failures by identifying the missing section
6. Keep structure consistent across a prompt library
7. Connect prompt structure to downstream evaluation

## Prerequisites

- None (this is a foundational topic)

---

## 1. The Five Sections

### Overview

```
┌─────────────────────────────────────────┐
│ ## Role          → who the model is     │
│ ## Context       → background info      │
│ ## Task          → what to do           │
│ ## Constraints   → bounds and rules     │
│ ## Output Format → the shape of output  │
└─────────────────────────────────────────┘
```

Each section answers a specific question the model needs answered.

---

### Section 1: Role

**Purpose:** Establishes the persona, expertise, and behavior pattern.

```markdown
## Role
You are an Islamic jurisprudence (فقه) assistant specializing in
the Hanafi school of law. You answer with evidence from the Quran
and Sunnah.
```

**Why it matters:** The role primes the model's behavior. A "teacher"
gives explanations; a "scholar" gives rulings; a "friend" gives casual
answers. The role determines tone, depth, and style.

**Failure when missing:** The model has no persona. It answers as a
generic assistant — no domain expertise, no appropriate tone.

---

### Section 2: Context

**Purpose:** Supplies the background information the model needs.

```markdown
## Context
The user is asking about travel prayer rules. The following passage
from the source text is available:

{retrieved_passage}
```

**Why it matters:** Without context, the model relies on its parametric
knowledge. For grounded generation (RAG), context is the evidence — the
model should answer from it, not from memory.

**Failure when missing:** The model hallucinates or gives generic
answers instead of using the provided evidence.

---

### Section 3: Task

**Purpose:** States the specific instruction — what to do.

```markdown
## Task
Answer the user's question about the travel prayer ruling. Reference
the evidence passage. If the passage does not contain the answer, state
that you cannot answer.
```

**Why it matters:** The task is the core instruction. It must be specific
enough that the output is verifiable. "Answer the question" is vague;
"answer the question citing the evidence passage, abstain if unsupported"
is specific.

**Failure when missing:** The model does something, but not what you
wanted. Vague task → vague output.

**What makes a task specific:**
| Vague | Specific |
|-------|----------|
| "Summarize this" | "Summarize in 3 sentences, focusing on the ruling" |
| "Answer the question" | "Answer citing the passage, abstain if unsupported" |
| "Explain this" | "Explain to a first-year student in 2 paragraphs" |

---

### Section 4: Constraints

**Purpose:** Bounds the output — length, tone, exclusions, requirements.

```markdown
## Constraints
- Answer in Arabic (MSA)
- Maximum 3 sentences
- Every claim must cite a passage reference
- Do not speculate or add information not in the passage
- If uncertain, say "لا أستطيع الإجابة من النص المقدم"
```

**Why it matters:** Without constraints, the model improvises. It might
answer in English, write 5 paragraphs, or add unsourced claims. The
constraints define the acceptable output space.

**Failure when missing:** The output is unconstrained — wrong language,
wrong length, missing citations, hallucinated content.

**Constraint types:**
| Type | Example |
|------|---------|
| Language | "Answer in Arabic" |
| Length | "Maximum 3 sentences" |
| Format | "Every claim must cite" |
| Content | "Do not speculate" |
| Tone | "Formal scholarly tone" |
| Abstention | "If unsupported, say you cannot answer" |

---

### Section 5: Output Format

**Purpose:** Specifies the exact shape of the response.

```markdown
## Output Format
Return a JSON object:
{
    "answer": "the answer text",
    "citations": ["b3:p12:0"],
    "confidence": 0.95
}
```

**Why it matters:** Structured output is parseable. The application can
extract fields, validate them, and use them programmatically. Free-form
output requires fragile parsing.

**Failure when missing:** The output is free-form text. The application
cannot reliably extract the answer, citations, or confidence.

**Format options:**
| Format | Use case |
|--------|----------|
| JSON | Programmatic consumption |
| Markdown | Human-readable display |
| Numbered list | Step-by-step reasoning |
| Key-value pairs | Simple extraction |
| Structured text with markers | Custom parsing |

---

## 2. The Complete Template

```markdown
## Role
You are [specific role] specializing in [domain].
[One sentence about behavior/tone.]

## Context
[Relevant background information.]
[Retrieved passages or data if using RAG.]

## Task
[Clear, specific instruction.]
[What to do with the input.]
[What to do if the input is insufficient.]

## Constraints
- [Rule 1]
- [Rule 2]
- [Rule 3]

## Output Format
[Expected response structure.]
```

---

## 3. Prompt Examples

### Example 1: RAG answer generation

```markdown
## Role
You are an Islamic jurisprudence assistant specializing in the Hanafi
school. You provide rulings with evidence from the Quran and Sunnah.

## Context
The user asks about travel prayer rules. The following evidence passage
is available:

"القصر هو رفع بعض الصلاة للمسافر. قال النبي ﷺ: 'ليس على المسافر
صيام' والقصر جائز للمسافر مسيرة ثلاثة أيام."

## Task
Answer the user's question using ONLY the evidence passage. Reference
the passage for each claim. If the passage does not answer the question,
state that you cannot answer from the provided text.

## Constraints
- Answer in Arabic (MSA)
- Maximum 3 sentences
- Every claim must reference the passage
- Do not add information not in the passage
- If unsupported, say "لا أستطيع الإجابة من النص المقدم"

## Output Format
JSON: {"answer": "...", "citations": ["..."], "abstained": false}
```

### Example 2: Code review

```markdown
## Role
You are a senior Python developer reviewing code for production quality.

## Context
This code is part of a RAG pipeline for Arabic text retrieval.

## Task
Review the following code for correctness, security, and performance.
For each issue, provide severity (CRITICAL/HIGH/MEDIUM/LOW) and a fix
direction. Do not rewrite the full code.

## Constraints
- Focus on correctness and security first
- Maximum 5 findings
- Each finding must have: severity, location, issue, fix direction

## Output Format
Markdown list with severity tags.
```

---

## 4. Diagnosing Prompt Failures

When output is wrong, identify which section is failing:

| Symptom | Missing section | Fix |
|---------|----------------|-----|
| Wrong tone/persona | Role | Add role section |
| Ignoring provided data | Context | Add retrieved passages |
| Doing the wrong thing | Task | Make task specific |
| Wrong length/language | Constraints | Add explicit constraints |
| Unparseable output | Output Format | Add format specification |
| Hallucinating | Constraints | Add "only from context" rule |
| Not abstaining | Constraints | Add abstention rule |

### The diagnostic process

1. **Identify the symptom** (wrong language, missing citations, etc.)
2. **Map to the section** (see table above)
3. **Add or fix that section**
4. **Test with the same input**
5. **Compare outputs**

---

## 5. Consistency Across a Prompt Library

### Why consistency matters

When you have 10+ prompts (for different tasks), inconsistent structure
makes them hard to maintain, test, and improve. Consistency enables:
- **Comparison:** Test prompt A vs prompt B on the same cases
- **Maintenance:** Fix a section in all prompts at once
- **Evaluation:** Score all prompts with the same rubric

### The library standard

Every prompt in the library must:
1. Use the five-section structure
2. Use the same section headers
3. Include an output format specification
4. Have at least one constraint
5. Be tested with at least one example

### Prompt versioning

```markdown
## Metadata
- ID: answer-generation-v2
- Version: 2.1
- Last updated: 2026-09-29
- Tested: 50 golden queries, faithfulness 0.94
```

---

## 6. Connection to Evaluation

The output format enables evaluation. When the answer is JSON with
citations, you can:
- Extract citations and check validity
- Parse the answer into claims
- Check each claim for support
- Compute faithfulness and citation precision

Without structured output, evaluation requires free-text parsing —
fragile and unreliable. The output format is the bridge between the
prompt and the eval.

---

## Real-World Application

In the Athar project:
1. The system prompt (role) identifies the Islamic jurisprudence domain.
2. Context carries the retrieved passage (from RAG).
3. Task instructs: answer with citations, abstain if unsupported.
4. Constraints enforce: Arabic MSA, max length, no speculation.
5. Output format: JSON with answer, citations, abstained flag.
6. The output is parsed and validated against the context (citation validity).
7. Faithfulness is computed on the claims.

The prompt structure is the contract between the user, the system, and
the model. Get it right and everything downstream works.

---

## Common Mistakes

1. **No role** — the model has no persona or domain expertise.

2. **Vague task** — "answer the question" without specifying how.

3. **No constraints** — the model improvises language, length, tone.

4. **No output format** — the application gets free text, cannot parse.

5. **Mixing concerns** — one section tries to do multiple things (e.g.,
   putting constraints in the task).

6. **Inconsistent structure** — different prompts use different sections.

7. **No abstention rule** — the model hallucinates instead of saying
   "I cannot answer."

---

## Key Takeaways

1. Five sections: role, context, task, constraints, output format.
2. Each section answers a question the model needs.
3. The task must be specific and verifiable.
4. Constraints define the acceptable output space.
5. Output format enables parsing and evaluation.
6. Missing sections cause predictable failures.

---

## Self-Check Questions

1. What are the five prompt sections and what does each do?
2. What failure mode results from a missing constraints section?
3. How does the output format enable evaluation?
4. What makes a task instruction "specific"?
5. How would you diagnose a prompt that produces wrong-language output?

---

## Further Reading / Connections

- **prompt-engineering 02** — Few-shot examples (extending the structure)
- **prompt-engineering 03** — Chain-of-thought (task specialization)
- **prompt-engineering 04** — Prompt evaluation (testing variations)
- **ai-evaluation 02** — Faithfulness (measuring output quality)
- **rag-system 05** — Abstention and citations (the constraints)