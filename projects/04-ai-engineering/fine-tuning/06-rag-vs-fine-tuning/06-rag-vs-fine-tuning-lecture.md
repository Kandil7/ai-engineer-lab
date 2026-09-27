# Fine-Tuning 06: RAG vs Fine-Tuning

## 🎯 Topic Overview

RAG and fine-tuning solve different problems. RAG supplies knowledge at
query time; fine-tuning shapes behavior at training time. Choosing between
them — or combining them — is a design decision, not a fashion choice.
This lecture covers the split, the tradeoffs, and the hybrid.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. State what RAG is good at and what it is not
2. State what fine-tuning is good at and what it is not
3. Decide which problem each tool solves
4. Design the hybrid: RAG for facts, fine-tuning for behavior
5. Write the decision as an ADR

---

## 1. What RAG Is Good At

RAG supplies knowledge at query time. It is good when the knowledge
changes (new sources, corrections), when the knowledge is too large to
train in, and when every answer must cite its source. RAG is the tool for
facts. The roadmap's exit test: "RAG is used for knowledge."

## 2. What Fine-Tuning Is Good At

Fine-tuning shapes behavior at training time. It is good when the task is
a stable format or style, when the model must follow a specific
instruction pattern, and when latency or cost make retrieval impractical.
Fine-tuning is the tool for behavior. The roadmap's exit test:
"fine-tuning is used for behavior."

## 3. The Tradeoffs

RAG costs at query time: retrieval latency, embedding cost, and the
context budget. Fine-tuning costs at training time: data curation, GPU
hours, and the risk of overfitting. RAG is transparent (citations);
fine-tuning is opaque (the behavior is in the weights). RAG updates
instantly; fine-tuning requires a new run.

## 4. The Hybrid

The two combine: RAG supplies the facts, fine-tuning shapes how the model
uses them. A fine-tuned model that follows the citation format, fed by a
retriever, is the standard production shape. The roadmap's exit test:
"the model is fine-tuned to follow the citation format."

## 5. The Decision as an ADR

The choice is recorded as an architecture decision: the problem, the
options, the chosen split, and the rationale. The ADR is the evidence that
the choice was made deliberately, not by default. The roadmap's exit test:
"the RAG vs fine-tuning decision is written as an ADR."

## Common Mistakes

- Fine-tuning for a fact problem that retrieval solves.
- RAG for a stable behavior problem that fine-tuning solves.
- Choosing without measuring either option.
- No ADR (the decision is invisible).
- Ignoring the hybrid.

## Key Takeaways

1. RAG is the tool for knowledge.
2. Fine-tuning is the tool for behavior.
3. RAG costs at query time; fine-tuning costs at training time.
4. The hybrid is the standard production shape.
5. The decision is written as an ADR.