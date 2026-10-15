# Quiz 01: Hexagonal Architecture

Test your understanding of Lecture 01. Choose one answer per question, check
the explanation, and record your score at the end.

---

### Question 1

Which way do dependencies point in clean and hexagonal architecture?

A. Inward only, toward the domain
B. Outward only, toward infrastructure
C. In both directions as needed
D. Toward whichever layer is largest

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** Domain depends on nothing and every outer layer depends
inward. An outward import is a layering violation.
</details>

---

### Question 2

Where does a port belong?

A. In the adapter package beside the client
B. In the inner layer beside the use case that needs it
C. In the HTTP handler that parses requests
D. In the configuration file as a string

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Ports are defined where they are used. The use case
declares what it needs and adapters conform from outside.
</details>

---

### Question 3

Which name is a good port name?

A. QdrantRetriever
B. Retriever
C. TorchEmbedderV2
D. FastApiHandler

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Ports name the role, not the product. Retriever survives a
store swap while product names freeze the stack.
</details>

---

### Question 4

What does the AnswerQuestion use case receive from its caller?

A. A concrete Qdrant client it constructs itself
B. Ports such as Retriever and CitationPolicy by constructor
C. Environment variables it reads inline
D. Hardcoded model names and URLs

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Collaborators arrive injected typed to ports. Construction
happens at the composition root from typed config.
</details>

---

### Question 5

What proves the use case depends on the port rather than an adapter?

A. Running it once against Qdrant
B. Running it against two adapters with identical results asserted
C. Mocking the use case itself
D. Reading the adapter source

**Difficulty:** Easy

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The demo binds InMemoryRetriever and
SimulatedQdrantRetriever and asserts exact equality of passages and answers.
</details>

---

### Question 6

A domain file imports qdrant_client. Which rule fires and why?

A. HEX007, because a URL is hardcoded
B. HEX001, because domain imported a technical package
C. HEX006, because a step name is too broad
D. No rule, domain may use any client

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** HEX001 is critical and forbids technical packages in
domain, including qdrant_client, torch, fastapi, sqlalchemy, transformers,
numpy, and requests.
</details>

---

### Question 7

An application module imports adapters.QdrantRetriever directly. Which rule fires?

A. HEX002, concrete adapter imported instead of the port
B. HEX006, pipeline step too broad
C. HEX007, hardcoded model
D. HEX004, signature leak

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** HEX002 is critical. Application must depend on the
Retriever port while the composition root wires the adapter.
</details>

---

### Question 8

A Retriever port method is declared as search(store: QdrantClient). What is wrong?

A. Nothing, ports should expose client types
B. HEX004, the signature leaks an infrastructure type
C. HEX006, the name spans responsibilities
D. HEX007, a model literal appears

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Port signatures must use plain types. Leaking QdrantClient
forces every caller to import the store.
</details>

---

### Question 9

A class claims it implements Retriever but only defines search. Which rule fires?

A. HEX005, required retrieve method is missing
B. HEX002, wrong import
C. HEX007, hardcoded value
D. HEX008, missing seam

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** HEX005 is critical. Claiming a port without its required
methods breaks substitution for every caller.
</details>

---

### Question 10

A pipeline step is named chunk_and_embed_and_rerank. What should happen?

A. Keep it, longer names are clearer
B. Split it into three single-responsibility steps
C. Move it to the domain layer
D. Hardcode its parameters

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** HEX006 is a warning. Names joined with and carry multiple
change reasons and should split into chunk, embed, and rerank steps.
</details>

---

### Question 11

A use case calls generate with model set to a literal gpt-4o-mini. What is the fix?

A. Leave it, literals are faster
B. Move the model name to typed config and pass it through the factory
C. Import torch in the domain
D. Add a second literal for fallback

**Difficulty:** Medium

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** HEX007 is a warning. Hardcoded models and URLs outside the
config seam block sweeping and review.
</details>

---

### Question 12

Which design satisfies the Strategy pattern for chunking?

A. One chunk function with branches for every option inline
B. Section-aware and fixed-512 strategies behind one chunk method, picked by config
C. Chunking code copied into each caller
D. Chunking inside the HTTP handler

**Difficulty:** Hard

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Strategy triggers when algorithms must swap without editing
the caller. One method shape plus config selection is the pattern.
</details>

---

### Question 13

When is a flat script the right call?

A. When there are two callers and two adapters
B. When the task is a one-off spike with a single caller and no second adapter
C. When the citation policy must be shared
D. When evaluation needs repeatable runs

**Difficulty:** Hard

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The rule of two governs. One caller and one adapter means a
script; extract a port when the second use arrives.
</details>

---

### Question 14

Which decision below is a one-way door and why?

A. QLoRA-first versus from-scratch pretraining, because reversal costs data and compute
B. Redis versus no cache, because a flag toggles it
C. vLLM versus llama.cpp, because both serve the same port
D. YAML config versus hardcoded, because literals move easily

**Difficulty:** Hard

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** Training approach commits data and compute that cannot be
recovered cheaply, so it needs an ADR and evaluation first. The rest are
two-way adapter or flag swaps.
</details>

---

### Question 15

An application module imports infra.qdrant without a config seam flag. Which rule fires and how does it differ from HEX002?

A. HEX008 fires; HEX002 is about importing an adapter class name while HEX008 is about the missing seam flag
B. HEX002 fires; they are the same rule
C. HEX006 fires; the import is too broad
D. No rule fires for missing seams

**Difficulty:** Hard

<details><summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** HEX008 is a warning for application code reaching to
infrastructure without a seam. HEX002 is critical for naming a concrete
adapter class. The demo keeps them distinct by import shape and flag.
</details>

---

## Score Tracking

| Question | Topic | Correct? |
|----------|-------|----------|
| 1 | Dependency rule | |
| 2 | Port placement | |
| 3 | Port naming | |
| 4 | Injection | |
| 5 | Substitution proof | |
| 6 | HEX001 | |
| 7 | HEX002 | |
| 8 | HEX004 | |
| 9 | HEX005 | |
| 10 | HEX006 | |
| 11 | HEX007 | |
| 12 | Strategy | |
| 13 | Flat script | |
| 14 | One-way door | |
| 15 | HEX008 vs HEX002 | |
| **Total** | **/15** | |

Scoring: 13-15 excellent, 10-12 good, 7-9 review the lecture, below 7 reread sections 1-4 and 7.

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | A | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Easy |
| 5 | B | Easy |
| 6 | B | Medium |
| 7 | A | Medium |
| 8 | B | Medium |
| 9 | A | Medium |
| 10 | B | Medium |
| 11 | B | Medium |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | A | Hard |
| 15 | A | Hard |
