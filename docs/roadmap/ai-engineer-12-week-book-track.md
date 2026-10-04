# AI Engineer Track — 12 Weeks (Book-Based)

> **Scope:** personal study plan across three books, verified against the actual
> PDF editions. This is a learning track, separate from the repo's
> [`active-track-10-week.md`](active-track-10-week.md) plan of record.
>
> **Books (edition-verified):**
> - *Hands-On Large Language Models* — Alammar & Grootendorst (12 chapters)
> - *Build a Large Language Model (From Scratch)* — Raschka (7 chapters)
> - *AI Engineering* — Chip Huyen (10 chapters)
>
> **Math reference (primary):** *Essential Math for AI* — Hala Nelson.
> **Math backup (proofs only):** *Mathematics for Machine Learning*.

---

## Weekly rhythm

- **10-15 hours/week:** 60% code, 30% reading, 10% math.
- **2 chapters/week** + one applied task.
- **One deployable project per month.**
- **Math:** look up the specific concept only at the moment the code needs it,
  never read linearly.

## Math references

- **Primary:** *Essential Math for AI* (Hala Nelson). Organized by AI task, so
  each concept maps directly to a week.
- **Backup (proofs only):** *Mathematics for Machine Learning*. Use it for the
  rigorous derivation of a single concept, not as the default reference.

---

## Month 1 — Practical foundations (Hands-On LLM)

Book is verified at 12 chapters. Month 1 uses Ch1-8; Ch9-12 are deliberately
deferred (Ch11-12 fine-tuning is covered more deeply by Raschka in Month 2).

| Week | Chapters | Practical goal | Applied task (Arabic) | Math trigger (Nelson) |
| --- | --- | --- | --- | --- |
| 1 | Ch1-2 | Tokenization + embeddings | Compare tiktoken vs an Arabic tokenizer on Arabic text; embed 100 sentences from a pinned subset of الشاملة; plot with UMAP | vectors, dot product, cosine sim — Ch7 |
| 2 | Ch3-4 | Inside the model + classification | Classify hadith by book (البخاري، مسلم...); if no labels exist, switch to zero-shot topical classification | probability, softmax — Ch11 |
| 3 | Ch5-6 | Clustering + prompt engineering | Spend 2h cleaning classical text (strip diacritics, footnotes) before BERTopic; try zero-shot, few-shot, CoT in Arabic | SVD/PCA — Ch6 |
| 4 | Ch7-8 | Build a mini RAG | Arabic Sentence-Transformers + FAISS/Chroma over a fixed subset of الشاملة | gradient descent — Ch3-4 |

**Month 1 output:** a small RAG that answers questions from a pinned subset of الشاملة.

---

## Month 2 — Build an LLM from scratch (Raschka)

| Week | Chapters | Practical goal | Applied task (Arabic) | Math trigger (Nelson) |
| --- | --- | --- | --- | --- |
| 5 | Ch1-2 | Tokenizer + data loader | Implement BPE from scratch on Arabic; build a data loader | entropy, info theory — Ch11 |
| 6 | Ch3-4 | Full transformer | Write self-attention and multi-head attention; assemble a GPT architecture | matrix multiply, softmax — Ch7 |
| 7 | Ch5 | Train a small model | Train on 1-2 books only; the goal is the training loop, not generation quality | backprop, gradients — Ch4 |
| 8 | Ch6-7 | Fine-tuning | Fine-tune for classification, then instruction-following in Arabic; wire into the RAG | regularization, Adam — Ch3-4 |

**Month 2 output:** a small Arabic GPT trained from scratch + an improved RAG.

---

## Month 3 — Production engineering (AI Engineering)

The book is exactly 10 chapters. Weeks map correctly, and Dataset Engineering is
pulled in explicitly.

| Week | Chapters | Practical goal | Applied task | Math trigger |
| --- | --- | --- | --- | --- |
| 9 | Ch3-4 (skim Ch1-2) | Evaluation framework | Define RAG metrics (faithfulness, relevance, recall@k); build an automated eval line on Arabic questions | precision/recall, F1 — Ch2 |
| 10 | Ch6 + Ch5 | RAG quality only | Add re-ranking and query expansion; measure against week-9 metrics | cosine, MMR — Ch7 |
| 11 | Ch8 then Ch7 | Dataset engineering, then fine-tuning | Curate/clean an Arabic dataset first, then LoRA a small model | — |
| 12 | Ch9 + Ch10 | Inference + deploy | Quantize; serve with Ollama; add logging, cost tracking, basic safety filters | trade-offs — Ch10 |

**Month 3 output:** a deployed, monitored, cost-optimized RAG system.

---

## Six fixes baked in

1. **Dataset Engineering (Ch8) now sits before Finetuning (Ch7)** because you
   cannot fine-tune without a dataset. This is also the chapter that most directly
   upgrades the Athar (RAG data prep) and Baligh (Arabic fine-tuning datasets) work.
2. **Agents stay deferred** to after week 12. Month 3 stays focused on RAG quality
   and evaluation.
3. **vLLM replaced with Ollama.** vLLM is unreliable on the RTX 5000 (Turing,
   sm_75); Ollama is the safe local default.
4. **The math column is a "trigger," not a topic.** Each entry names the Nelson
   chapter you open at the exact moment the code needs it.
5. **The Arabic corpus is pinned.** Work from a fixed, pre-cleaned subset (e.g.,
   ten hadith books), reusing Athar's cleaning conventions, not the whole of
   الشاملة as an open target.
6. **Built-in buffer.** Weeks 4, 8, and 12 are integration weeks. If you fall
   behind, shrink the project deliverable, never the reading.

---

## Continuity

- Push every project to GitHub with a README explaining what you learned.
- Post progress weekly (tweet, post, or short blog).
- The three integration weeks (4, 8, 12) are checkpoint and catch-up points.
- After week 12, reassess and pick a specialization: RAG, Agents, Fine-Tuning,
  or LLMOps.

## Caveats

- Weeks 6, 7, and 11 are the heaviest. If a single week must give ground, cut the
  Arabic-specific flourish first and do the book's default English dataset. The
  mechanism matters more than the language; re-apply Arabic later.
- Chapter numbers are verified against the current PDF editions. Re-check the
  table of contents if you switch editions.
