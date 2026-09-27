# Fine-Tuning 01: Supervised Fine-Tuning (SFT)

## 🎯 Topic Overview

Supervised fine-tuning adapts a pretrained model to a task by training it
on instruction-answer pairs. The pretrained model already knows language;
SFT teaches it the format and behavior of the target task. This lecture
covers what SFT changes, what it does not change, and the loss that drives
it.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what SFT changes and what it does not
2. Apply the chat template and mask non-answer tokens
3. Explain why the loss is computed on answer tokens only
4. Detect overfitting on the training set
5. Decide when SFT is the right tool

---

## 1. What SFT Changes

SFT adapts the model's behavior, not its knowledge. A pretrained model
already knows the language; SFT teaches it to answer in the target format
and style. It does not reliably add new facts — a model that never saw a
fact in pretraining will not learn it from a few hundred examples. The
roadmap's exit test: "the model follows the target format after SFT."

## 2. The Chat Template

Instruction data is formatted with a chat template: system, user, and
assistant turns. The template is the model's contract — the same template
at training and inference. A mismatch between training and inference
templates degrades the model. The template is part of the model card.

```python
# chat template applied to one example
"<|system|>أنت مساعد فقهي</|system|>\n<|user|>ما حكم الصلاة في السفر؟</|user|>\n<|assistant|>القصر جائز"
```

## 3. The Loss on Answer Tokens

The loss is computed on the assistant's answer tokens only, not on the
prompt. The model must learn to produce the answer, not to predict the
question. Masking the prompt tokens keeps the loss focused on generation.
This is the standard SFT loss: cross-entropy on the answer span.

```python
# labels: -100 masks the prompt, the answer tokens carry the loss
labels = [-100] * len(prompt_tokens) + answer_token_ids
```

## 4. Overfitting

A small instruction set is easy to memorize. Overfitting shows as training
loss near zero while evaluation loss rises. The fix is a held-out
evaluation set, monitored during training. The roadmap's exit test: "the
model does not overfit the training set."

## 5. When SFT Is the Right Tool

SFT is right when the task is behavioral: format, style, tone, following
instructions. It is wrong when the task needs new facts — that is
retrieval's job. The roadmap's decision: RAG for knowledge, SFT for
behavior. The two are complementary, not competing.

## Common Mistakes

- Expecting SFT to add knowledge.
- Training and inference template mismatch.
- Computing loss on the prompt tokens.
- No held-out evaluation set (overfitting invisible).
- Fine-tuning for a fact problem that retrieval solves.

## Key Takeaways

1. SFT changes behavior, not knowledge.
2. The chat template is the training-inference contract.
3. Loss is computed on answer tokens only.
4. A held-out set makes overfitting visible.
5. RAG for knowledge, SFT for behavior.