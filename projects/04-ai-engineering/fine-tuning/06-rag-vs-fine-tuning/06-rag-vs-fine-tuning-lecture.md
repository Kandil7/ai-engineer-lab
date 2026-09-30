# Fine-Tuning 06: RAG vs Fine-Tuning

## Topic Overview

RAG and fine-tuning solve different problems. RAG supplies knowledge at query time;
fine-tuning shapes behavior at training time. Choosing between them, or combining them, is
a design decision with measurable consequences, not a fashion choice. Getting it wrong is
expensive in both directions: fine-tuning for a knowledge problem produces a model that
memorizes a few facts and hallucinates the rest, and reaching for RAG to fix a formatting
problem produces a retriever bolted onto a model that still will not follow the format.

The clean way to decide is the knowledge/behavior split. If the problem is "the model does
not know this fact", the tool is retrieval. If the problem is "the model does not follow
this format, tone, or constraint", the tool is fine-tuning. In production the two usually
combine: retrieval supplies the facts, and a fine-tuned model shapes how the answer is
presented.

This lecture covers what each tool is good at, the cost and transparency tradeoffs, the
hybrid shape, and why the decision belongs in an ADR.

## Learning Objectives

By the end of this lecture, you will be able to:

1. State what RAG is good at and what it is not.
2. State what fine-tuning is good at and what it is not.
3. Classify a problem as knowledge, behavior, or hybrid.
4. Design the hybrid: retrieval for facts, fine-tuning for behavior.
5. Compare the cost and transparency of the two tools.
6. Record the decision as an ADR.

## Prerequisites

- Fine-Tuning 01 (SFT) for what fine-tuning changes.
- A working understanding of RAG retrieval and generation.

---

## 1. What RAG Is Good At

### Knowledge at query time

RAG supplies knowledge at query time from a corpus that can change without retraining. It is
good when:

- **The knowledge changes** (new sources, corrections, updated documents).
- **The knowledge is too large to train in** (a whole library, not a handful of facts).
- **Every answer must cite its source** (retrieval makes citations possible).

### What RAG does not do well

RAG does not reliably change the model's style, tone, or format. If the model does not cite
its sources or does not follow the house format, retrieving more passages will not teach
it to. That is a behavior problem, and behavior is fine-tuning's job.

### The exercise

```python
facts = {"kind": "knowledge", "changes": True, "cites": True}
assert choose_tool(facts) == "rag"
```

A changing corpus with a citation requirement is the clearest RAG case.

## 2. What Fine-Tuning Is Good At

### Behavior at training time

Fine-tuning shapes behavior at training time: the format, the tone, the instruction
pattern, the constraints the model must follow. It is good when:

- **The task is a stable format or style** (always cite, always answer in Arabic, always
  structure the response a certain way).
- **The model must follow a specific instruction pattern** consistently.
- **Latency or cost make heavy retrieval impractical** and the behavior can be baked in.

### What fine-tuning does not do well

Fine-tuning does not reliably add knowledge. A fact absent from pretraining and absent from
the SFT set will be hallucinated, no matter how many epochs. Teaching facts by fine-tuning
is the classic mistake this lecture exists to prevent.

### The exercise

```python
format_task = {"kind": "behavior", "stable": True}
assert choose_tool(format_task) == "fine-tuning"
```

A stable format the model must follow is the clearest fine-tuning case.

## 3. The Tradeoffs

| Axis | RAG | Fine-tuning |
| --- | --- | --- |
| **When the cost lands** | Query time (latency, embedding, context) | Training time (data, GPU hours) |
| **Transparency** | High (citations, inspectable sources) | Low (behavior is in the weights) |
| **Update speed** | Instant (re-index) | Slow (new run) |
| **Change type** | Knowledge | Behavior |
| **Data need** | A corpus | Labeled input-output pairs |

RAG is transparent and updatable; fine-tuning is opaque and slow to change but can bake in
behavior retrieval cannot. Neither is strictly better; they solve different problems.

## 4. The Hybrid

### The standard production shape

Retrieval supplies the facts and a fine-tuned model shapes how they are used:

```text
query -> retrieval -> context passages
      -> fine-tuned model (formats, cites, answers)
      -> grounded answer with citations
```

The retrieval makes the answer correct and citable; the fine-tune makes it well-formed and
consistent. This is the shape most serious RAG systems converge on.

### Why the split works

Each tool does what it is good at. The retrieval handles the changing, large, citable
knowledge; the fine-tune handles the stable behavior. Neither is asked to do the other's
job.

### The exercise

```python
hybrid = {"kind": "hybrid", "facts": "rag", "behavior": "fine-tuning"}
assert choose_tool(hybrid) == "hybrid"
```

## 5. The Decision as an ADR

### What it records

The choice is recorded as an architecture decision: the problem, the options considered,
the chosen split, and the rationale.

```python
adr = {
    "problem": "answer Islamic-text questions with citations",
    "decision": "RAG for knowledge, fine-tuning for citation behavior",
    "rationale": "corpus changes; answers must cite; format is stable",
}
```

### Why the ADR matters

The knowledge/behavior decision is long-lived and hard to reverse (a fine-tune is a
training run, not a config flag). The ADR makes the choice deliberate and reviewable, and it
records what evidence would change the decision (for example, retrieval latency rising
enough that behavior must be baked in, or a new corpus that makes re-indexing costly).

### Re-evaluation triggers

Revisit the decision when the corpus size or change rate shifts, when retrieval latency
becomes a problem, when the format changes, or when a model update changes what the base
model already does well.

## Real-World Application

- Deciding that Athar needs RAG for the changing Islamic-text corpus and a fine-tune for
  the citation format and scholarly tone.
- Recognizing that "the model will not always cite" is a behavior problem, so the fix is
  SFT, not more retrieval.
- Recognizing that "the model does not know this hadith" is a knowledge problem, so the fix
  is retrieval, not more training.
- Recording the split in an ADR so a future change is measured against the rationale.

## Common Mistakes

1. **Fine-tuning for a fact problem.** The model memorizes a few facts and hallucinates the
   rest.
2. **RAG for a stable behavior problem.** Retrieval cannot teach format or tone.
3. **Choosing without measuring either option.** The decision is made on intuition.
4. **No ADR.** The decision is invisible and gets reversed on vibes.
5. **Ignoring the hybrid.** Most production systems need both.
6. **Treating the choice as permanent.** The right split changes as the corpus and the task
   change.

## Key Takeaways

1. RAG is the tool for knowledge; it is transparent, updatable, and citable.
2. Fine-tuning is the tool for behavior; it is opaque and slow to change but bakes in
   format and tone.
3. RAG costs at query time; fine-tuning costs at training time.
4. The hybrid (retrieval for facts, fine-tune for behavior) is the standard production
   shape.
5. The decision is written as an ADR with re-evaluation triggers.

## Self-Check Questions

1. Classify "the model does not cite its sources" as knowledge or behavior, and name the
   tool.
2. Classify "the model does not know this recent document" as knowledge or behavior, and
   name the tool.
3. Give one advantage of RAG that fine-tuning lacks and one advantage of fine-tuning that
   RAG lacks.
4. Describe the hybrid shape and why each tool handles its half.
5. What should an ADR for this decision contain to be useful in six months?

## Further Reading / Connections

- Fine-Tuning 01 (SFT) — behavior versus knowledge in depth.
- `projects/04-ai-engineering/rag-system/` — the retrieval half of the hybrid.
- AI Evaluation 02 (faithfulness and citation precision) — measuring whether the hybrid
  works.
- `docs/decisions/` — where the RAG-versus-fine-tuning ADR lives.
