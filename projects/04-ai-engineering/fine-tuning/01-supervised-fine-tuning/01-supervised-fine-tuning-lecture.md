# Fine-Tuning 01: Supervised Fine-Tuning (SFT)

## Topic Overview

Supervised fine-tuning (SFT) adapts a pretrained language model to a
specific task by training it on input-output pairs. The pretrained model
already knows language — grammar, facts, reasoning patterns. SFT teaches
it the format and behavior of the target task: how to structure answers,
what tone to use, what constraints to follow. It does not reliably add
new knowledge. A model that has never encountered a fact during
pretraining will not learn it from a few hundred examples.

This distinction — **behavior vs knowledge** — is the most important
concept in fine-tuning. It determines whether SFT is the right tool for
the job. If the problem is "the model doesn't know this fact," the answer
is retrieval (RAG). If the problem is "the model doesn't follow this
format," the answer is SFT.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what SFT changes and what it does not change
2. Apply the chat template and understand its contract
3. Compute the loss on answer tokens only (and explain why)
4. Detect and prevent overfitting
5. Design an instruction dataset for the target task
6. Decide when SFT is the right tool (behavior vs knowledge)
7. Connect SFT to the LoRA/QLoRA parameter-efficient methods

## Prerequisites

- Applied ML fundamentals (applied-ml 01-04)
- Basic understanding of neural networks and training

---

## 1. What SFT Changes

### The pretrained model

A pretrained language model (GPT, Llama, Qwen) has been trained on
trillions of tokens of text. It has learned:

- **Grammar and syntax** — how sentences work
- **World knowledge** — facts about the world (up to its training cutoff)
- **Reasoning patterns** — how to chain ideas, solve problems
- **Code patterns** — how programs are structured

What it has NOT learned:
- **Your specific format** — how to structure answers for your task
- **Your domain conventions** — how an Islamic scholar phrases a ruling
- **Your constraints** — "always cite the source," "answer in Arabic"

### What SFT does

SFT updates the model's weights so it produces output in the target
format. The training signal comes from input-output pairs:

```
Input:  "ما حكم الصلاة في السفر؟"
Output: "القصر جائز للمسافر، واستحباب الجمع بين الصلاتين. (متفق عليه)"
```

After training, the model produces answers in this format — with
citations, in Arabic, with the scholarly tone.

### What SFT does NOT do

SFT does not reliably add knowledge. Consider:

- The model knows what "القصر" means (from pretraining).
- The model knows the format (from SFT).
- But if the specific hadith was never in pretraining AND the SFT set
  doesn't cover it, the model will hallucinate.

**The rule:** SFT shapes behavior. RAG supplies knowledge.

---

## 2. The Chat Template

### What it is

The chat template is the format that structures the conversation between
the user and the model. It includes role markers, turn separators, and
special tokens.

```
<|system|>أنت مساعد فقهي متخصص في الفقه الإسلامي</|system|>
<|user|>ما حكم الصلاة في السفر؟</|user|>
<|assistant|>القصر جائز للمسافر...</|assistant|>
```

### The training-inference contract

**The template at training must be identical to the template at
inference.** If the model was trained with `<|user|>...<|assistant|>...`
but inference uses `[INST]...[/INST]`, the model will be confused.

```
Training:  <|user|>question<|assistant|>answer
Inference: <|user|>question<|assistant|>
                                        ↑ the model generates from here
```

### The template is part of the model card

When you register a fine-tuned model, the chat template is recorded
alongside it. Without the template, the model is unusable — the caller
does not know how to format input.

```python
# The template travels with the model
model_card = {
    "model": "athar-sft-v1",
    "base": "qwen2.5-7b",
    "chat_template": "<|system|>{sys}<|user|>{user}<|assistant|>{assistant}",
}
```

---

## 3. The Loss on Answer Tokens

### The problem

If we compute loss on the entire sequence (prompt + answer), the model
learns to predict the prompt. But we don't want the model to generate
the prompt — we want it to generate the answer given the prompt.

### The solution

Mask the prompt tokens. Set their labels to -100 (the ignore index in
PyTorch cross-entropy). The loss is computed only on the answer tokens.

```python
def build_labels(prompt_tokens: list[int], answer_tokens: list[int]) -> list[int]:
    """Mask the prompt with -100; answer tokens carry the loss."""
    return [-100] * len(prompt_tokens) + answer_tokens


# Example:
# prompt = [101, 102, 103, 104]  (the user's question)
# answer = [201, 202, 203]        (the target response)
# labels = [-100, -100, -100, -100, 201, 202, 203]
```

### Why this matters

Without masking, the model spends capacity learning to predict the
question. With masking, all capacity goes to learning the answer format
and content. The difference in training quality is significant.

### The gradient signal

In backpropagation, only answer tokens contribute gradients. The prompt
tokens are present in the forward pass (they condition the generation)
but contribute zero to the loss. This is the correct behavior for
instruction tuning.

---

## 4. Overfitting

### What it is

Overfitting happens when the model memorizes the training set instead of
generalizing. With a small instruction dataset (a few hundred examples),
this is a real risk.

### The symptoms

| Metric | Healthy | Overfit |
|--------|---------|---------|
| Training loss | Decreasing | Near zero |
| Evaluation loss | Decreasing | Rising |
| Eval quality | Improving | Degrading |

```
Healthy:     train=0.25  eval=0.28   (eval tracks train)
Overfit:     train=0.01  eval=0.50   (train memorized, eval diverged)
```

### The prevention

1. **Held-out evaluation set** — 10% of data, excluded from training.
   Monitor eval loss during training.

2. **Early stopping** — stop training when eval loss starts rising.

3. **Regularization** — LoRA with low rank acts as a regularizer (topic 02).

4. **Data quality over quantity** — 200 clean examples beat 2000 noisy
   ones. Noise leads to memorization.

### The detection

```python
def is_overfit(train_loss: float, eval_loss: float) -> bool:
    return train_loss < 0.05 and eval_loss > train_loss * 3


# Check during training
for epoch in range(epochs):
    train_loss = train_one_epoch()
    eval_loss = evaluate()
    if is_overfit(train_loss, eval_loss):
        print("Overfitting detected — stopping")
        break
```

---

## 5. Designing the Instruction Dataset

### The format

Each example is a pair: instruction (input) and response (target output).

```json
{
    "instruction": "ما حكم الصلاة في السفر؟",
    "response": "القصر جائز للمسافر. قال النبي ﷺ: 'ليس على المسافر صيام'"
}
```

### Quality over quantity

| Example count | Quality | Result |
|---------------|---------|--------|
| 50 | Perfect | Minimal but clean |
| 200 | Good | Good for most tasks |
| 1000 | Clean | Excellent |
| 1000 | Noisy | Worse than 200 clean |
| 10000 | Mixed | Unpredictable |

### What makes a good example

1. **Correct** — the answer is factually right
2. **Consistent** — the format matches across all examples
3. **Diverse** — covers the task's variation (question types, lengths)
4. **Realistic** — reflects how users actually ask

### What makes a bad example

1. **Wrong answers** — teaches the model to be wrong
2. **Mixed formats** — some with citations, some without
3. **Duplicates** — wastes capacity on the same pattern
4. **Too long** — dominates the batch, biases training

---

## 6. Behavior vs Knowledge — The Decision

### The framework

| Problem | Root cause | Solution |
|---------|-----------|----------|
| Model doesn't follow format | Behavior | SFT |
| Model doesn't know a fact | Knowledge | RAG |
| Model's tone is wrong | Behavior | SFT |
| Model hallucinates specifics | Knowledge | RAG |
| Model's answers lack citations | Behavior | SFT |
| Model can't answer a question | Knowledge | RAG |

### The hybrid

In production, SFT and RAG work together:

1. RAG retrieves relevant passages (knowledge)
2. SFT-tuned model formats the answer with citations (behavior)
3. The answer is grounded in the retrieved context

```
User query → RAG retrieval → context passages
    → SFT-tuned model (formats, cites, answers)
    → grounded answer with citations
```

### The ADR

The decision between SFT and RAG is recorded as an architecture decision
record (ADR). It captures:
- The problem
- The options considered
- The decision (SFT for behavior, RAG for knowledge)
- The rationale
- The re-evaluation trigger

---

## 7. Connection to LoRA and QLoRA

SFT can be done two ways:

| Method | What trains | Memory | Quality |
|--------|------------|--------|---------|
| Full fine-tuning | All weights | High (14 GB for 7B) | Best |
| LoRA | Small adapters | Low (1 GB for 7B) | Near full |
| QLoRA | LoRA on quantized base | Lowest (4 GB for 7B) | Near LoRA |

For a 16 GB GPU (RTX 5000), QLoRA is the practical choice. The base
model is quantized to 4-bit (frozen), and small LoRA adapters are
trained on top.

The next topic (LoRA and QLoRA) covers the details of parameter-efficient
fine-tuning.

---

## Real-World Application

In the Athar project (Arabic Islamic-text RAG):

1. The corpus is retrieved by RAG (knowledge).
2. A QLoRA-tuned model formats answers with citations (behavior).
3. The chat template ensures Arabic output with scholarly tone.
4. The loss is computed on answer tokens (citations + text).
5. The eval set tests: format compliance, citation accuracy, faithfulness.
6. The model is registered with its chat template and base model version.

---

## Common Mistakes

1. **Expecting SFT to add knowledge** — it won't. Use RAG for facts.

2. **Template mismatch** — training with one template, inference with
   another. The model degrades.

3. **Computing loss on the prompt** — the model learns to predict the
   question, not the answer.

4. **No held-out eval set** — overfitting goes undetected until
   production.

5. **Too many noisy examples** — 200 clean beats 2000 mixed.

6. **Overfitting a small dataset** — training for too many epochs on a
   few hundred examples.

7. **SFT for a knowledge problem** — the model memorizes a few facts and
   fails on the rest. RAG is the right tool.

---

## Key Takeaways

1. SFT changes behavior (format, tone, structure), not knowledge.
2. The chat template is the training-inference contract — identical at both ends.
3. Loss is computed on answer tokens only (prompt masked with -100).
4. A held-out eval set prevents/detects overfitting.
5. SFT for behavior, RAG for knowledge — the hybrid is the production shape.

---

## Self-Check Questions

1. What is the difference between what SFT changes and what RAG supplies?
2. Why must the chat template be identical at training and inference?
3. How does masking prompt tokens with -100 affect the training signal?
4. What are the symptoms of overfitting during SFT?
5. When would you choose SFT over RAG for a given problem?

---

## Further Reading / Connections

- **fine-tuning 02** — LoRA and QLoRA (parameter-efficient methods)
- **fine-tuning 03** — Training data preparation (quality, dedup)
- **fine-tuning 06** — RAG vs fine-tuning (the ADR)
- **rag-system 01** — Chunking (the knowledge side)
- **ai-evaluation 02** — Faithfulness (measuring the answer quality)