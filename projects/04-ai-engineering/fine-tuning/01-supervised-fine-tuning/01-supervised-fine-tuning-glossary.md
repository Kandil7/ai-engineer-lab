# Fine-Tuning 01: Supervised Fine-Tuning (SFT) — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| SFT | Supervised fine-tuning on instruction-answer pairs | format + behavior |
| Chat template | The system/user/assistant format | training-inference contract |
| Answer-token loss | Loss on answer tokens only, prompt masked | -100 labels |
| Overfitting | Memorizing the training set | eval loss rises |
| Held-out set | Evaluation examples not in training | overfitting visible |
| Behavior vs knowledge | SFT changes behavior, not facts | RAG supplies facts |

---

## Alphabetical Glossary

### Answer-token loss

**Definition:** The loss computed on the assistant's answer tokens only,
with the prompt masked. The model learns to produce answers, not to predict
questions.

**Example:**
```python
labels = [-100] * len(prompt_tokens) + answer_token_ids
```

**Related concepts:** SFT, Chat template

---

### Behavior vs knowledge

**Definition:** SFT changes the model's behavior — format, style, tone —
not its knowledge. New facts come from retrieval, not fine-tuning.

**Example:**
```python
# SFT teaches the answer format; RAG supplies the facts
```

**Related concepts:** SFT

---

### Chat template

**Definition:** The system/user/assistant format applied to instruction
data. The training-inference contract: the same template at both ends.

**Example:**
```python
# "<|system|>...<|user|>...<|assistant|>..."
```

**Related concepts:** SFT, Answer-token loss

---

### Held-out set

**Definition:** Evaluation examples excluded from training. Monitored
during training to make overfitting visible.

**Example:**
```python
# 10% of the instruction set held out for evaluation
```

**Related concepts:** Overfitting

---

### Overfitting

**Definition:** Memorizing the training set. Shows as training loss near
zero while evaluation loss rises.

**Example:**
```python
# train loss 0.01, eval loss rising
```

**Related concepts:** Held-out set

---

### SFT

**Definition:** Supervised fine-tuning: adapting a pretrained model to a
task by training on instruction-answer pairs. Changes behavior, not
knowledge.

**Example:**
```python
# a general model trained to answer in the target format
```

**Related concepts:** Chat template, Answer-token loss

---

## Related Concepts

- **LoRA/QLoRA**: the parameter-efficient way to run SFT (topic 02)
- **Training data**: the instruction set quality (topic 03)
- **RAG vs fine-tuning**: the knowledge/behavior split (topic 06)

## Key Takeaways

1. SFT changes behavior, not knowledge.
2. The chat template is the training-inference contract.
3. Loss is computed on answer tokens only.
4. A held-out set makes overfitting visible.
5. RAG for knowledge, SFT for behavior.