# Quiz 01: Domain-Driven Design and Domain Modeling

## Topic Overview
This quiz covers the modeling discipline behind Lecture 01: the ubiquitous language, entities and value objects with their equality semantics, aggregates and roots as consistency boundaries, invariants enforced at the boundary, factories and repositories, past-tense domain events with idempotent consumers, bounded contexts and their declared relationships, specifications, DTO discipline, and the nine-rule audit (DDD001–DDD009).

---

## Questions

### Question 1
**What is the ubiquitous language?**

- A) A shared English glossary maintained in the project wiki
- B) One rigorously defined vocabulary shared between domain experts and the code — type names, method names, and conversation all use the same words
- C) The set of API field names exposed to clients
- D) A modeling notation such as UML class diagrams

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The ubiquitous language is an engineering interface, not documentation. It binds conversation, class names, and method names into one vocabulary, and drift between the spoken word and the code word is a defect. A wiki glossary that the code does not use (A) and wire formats (C) are artifacts, not the language; UML (D) is notation.
</details>

---

### Question 2
**A domain expert says "a narration." Your code names the same concept `DataItem`. What does the lecture call this, and which audit rule fires?**

- A) An anemic model; DDD001 fires
- B) A ubiquitous-language violation (placeholder name); DDD007 fires
- C) A value object with identity; DDD002 fires
- D) Nothing — names are style choices

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Placeholder vocabulary (`DataItem`, `Info`, `Manager`, `Helper`) hides the concept the model exists to express, so every discussion about it needs translation first. DDD007 flags it as a warning. The GOOD pack names the same concept `Narration` — the expert's word — and the rule stays silent.
</details>

---

### Question 3
**What distinguishes an entity from a value object?**

- A) Entities are always mutable; value objects are always larger
- B) Entities have identity that survives attribute change and compare by identity; value objects have no identity and compare by all attributes
- C) Entities map to database tables; value objects map to columns
- D) Entities are Pydantic models; value objects are dataclasses

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The cut is mechanical: identity versus attributes. A `Narration` with a fixed `narration_id` is the same narration after its text is corrected; a `SourceLocation(book_id="b1", page=12, source_version="v1")` is equal to every other location with those attributes and nothing else. Storage mapping (C) and class mechanism (D) are implementation choices, not the distinction.
</details>

---

### Question 4
**Athar's `SourceLocation` is a `@dataclass(frozen=True)` with checks in `__post_init__`. Which two properties does this give the value object?**

- A) Lazy loading and schema migration
- B) Attribute equality with immutability, plus rejection of invalid instances at construction
- C) Automatic persistence and JSON serialization
- D) Thread-safe setters and copy-on-write

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `frozen=True` generates attribute-based `__eq__`, makes instances hashable, and blocks field assignment. The `__post_init__` checks (`book_id` non-empty, `page >= 1`) make invalid state unconstructible — parse, don't validate — so no later layer needs to re-check. That combination is the value-object pattern the lecture calls "illegal state is impossible state."
</details>

---

### Question 5
**What makes an aggregate root a consistency boundary?**

- A) It is the largest class in the domain layer
- B) All changes to any member happen inside one transaction that starts and ends at the root, and the root enforces every invariant
- C) It holds database connection pools for its members
- D) It is the only class allowed to talk to the repository of every aggregate

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The root is the single entry point and the transaction boundary: the aggregate loads and saves as a whole, and the root's methods enforce the invariants for every caller (section 5). Size (A) is explicitly not the criterion — aggregates should be as small as the invariants allow. Connection pools (C) are infrastructure; holding other aggregates' repositories (D) would couple what must stay independent.
</details>

---

### Question 6
**The GOOD pack's `Passage` root exposes `ingest`, `attach_narration`, and `extend_isnad`. Why are these preferred over `set_page`, `set_original`, and similar setters?**

- A) Methods run faster than setters in CPython
- B) Intention-revealing methods enforce the invariants at the boundary; setters accept whatever the caller passes and enforce nothing (DDD001)
- C) Setters cannot be serialized to JSON
- D) The domain-driven design literature forbids methods with arguments

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Setters are pass-throughs: every rule about a valid `Passage` moves into whichever callers remember to check. `attach_narration` names the rule it enforces — the demo shows it rejecting a narration already attached to another passage — so the guarantee lives in one place the compiler can find. Speed (A) and serialization (C) are irrelevant; D is simply false.
</details>

---

### Question 7
**An invariant is declared on `Narration`, a member of the `Passage` aggregate. Which audit rule fires, and why is the placement wrong?**

- A) DDD001 — members may not have methods
- B) DDD005 — the rule is cross-aggregate
- C) DDD004 — members can be replaced or reached through paths the root never sees, so no one is responsible for the rule
- D) No rule fires — members may declare invariants

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Only the root can guarantee a rule for every caller; a member's invariant has no enforcement point once the member is constructed or replaced outside the root's methods. DDD004 fires (critical). DDD001 is about setters on roots; DDD005 is about `scope: cross-aggregate` rules forced into one transaction — a different defect.
</details>

---

### Question 8
**Why can a cross-aggregate invariant not be enforced as a single transaction?**

- A) Transactions are too slow for cross-aggregate work
- B) Two aggregate roots cannot share one local transaction without coupling their schemas and lifecycles; the correct mechanism is a past-tense domain event with an idempotent consumer (DDD005 fires otherwise)
- C) Databases refuse to lock rows from different tables
- D) Domain events are faster than transactions

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Sharing a transaction across roots turns two aggregates into one — exactly what the boundaries exist to prevent — and does not survive distribution. The GOOD pack declares `alias_table_reflects_committed_merge` with `mechanism: domain-event`; the BAD pack's `single-transaction` mechanism trips DDD005, critical. Performance (A, D) and lock mechanics (C) are not the argument.
</details>

---

### Question 9
**Which set of names is correct for domain events?**

- A) `PublishNarration`, `CreateMergeDecision`, `SendNotification`
- B) `NarrationPublished`, `MergeDecisionCommitted`, `EntityMerged`
- C) `narration_publish`, `merge_decision_create`, `entity_merge`
- D) Any name, as long as the payload is valid

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Events are past-tense records of what happened; commands (A) are instructions, and on at-least-once transport a redelivery re-issues the instruction — DDD006's warning. Note the exercise's rule: a name starting with a verb word but ending in a past participle (`MergeDecisionCommitted`) is a record, not a command. Payload validity (D) says nothing about intent.
</details>

---

### Question 10
**The `IdempotentConsumer` in the exercise receives the same `EntityMerged` event twice. What happens, and why?**

- A) Both deliveries apply — the alias table advances twice
- B) The consumer crashes on the duplicate
- C) The first delivery applies; the second is suppressed by the stored event id; the alias table advances once
- D) The queue layer deduplicates before the consumer sees either copy

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** At-least-once delivery plus retries guarantees duplicates will arrive, so the consumer — not the transport — stores the event id before applying the side effect. The demo confirms: first delivery applied, redelivery suppressed, alias updates = 1. Relying on the queue to dedupe (D) is exactly the assumption at-least-once semantics forbid.
</details>

---

### Question 11
**Athar's `EntityId` type is used in the catalog, citation, and resolution contexts. What makes that sharing legitimate?**

- A) Sharing types across contexts is always fine
- B) It is declared as a shared kernel — co-owned, minimal, changes need both sides' consent; without the declaration, DDD008 fires
- C) It is a value object, and value objects may cross any boundary
- D) It is copied into each context at build time

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Cross-context sharing is legitimate only when the relationship is declared — shared kernel or anti-corruption layer. The GOOD pack sets `boundary_relationship: "shared-kernel"`; the BAD pack leaves it `None` and DDD008 fires (critical): two contexts silently coupled drift until neither can change safely. Value-object status (C) is orthogonal.
</details>

---

### Question 12
**What is wrong with a repository method `find_by(filters: dict)`?**

- A) Dictionaries are not type-safe enough
- B) It leaks storage mechanics; a repository is the aggregate's collection interface and its queries should be named after intent — `passages_of_book(book_id)` (DDD009)
- C) It cannot be mocked in tests
- D) Repositories should only expose `get_by_id`

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A raw filter shape pushes the domain intent back onto every caller and makes the repository a table-access layer in disguise. DDD009 fires (warning). Rich, intent-revealing queries are not only allowed — `pending_merge_candidates()` in the GOOD pack — they are the point. Mockability (C) and a `get_by_id`-only rule (D) miss the issue.
</details>

---

### Question 13
**Two narrations have identical text but different `narration_id`s. Under correct entity semantics, are they equal? If a dataclass compares them by attributes, what breaks?**

- A) Yes, they are equal; nothing breaks
- B) No — identity decides, so they are distinct; attribute comparison collapses them, breaking dedupe, caches, and collection behavior the moment a display field changes (DDD003)
- C) No — and attribute comparison also breaks serialization
- D) Yes — and DDD003 fires to force the collapse

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Entities are equal only when their identities are equal; the identical text is a coincidence of content, not of identity. The dataclass default (`eq=True`, attribute comparison) silently merges the two, so every set membership, cache key, and dedupe step built on that equality is wrong — the production shape of DDD003 (critical). The fix is `eq=False` plus an `__eq__` over the id.
</details>

---

### Question 14
**What is the specification pattern's practical payoff for the merge policy `auto_merge = (score >= 0.92) AND (veto is absent)`, given a review queue also exists?**

- A) It makes the policy run faster
- B) The review queue is `NOT auto_merge` — one line of composition — so the two queues provably partition the candidate space instead of duplicating the rule in two modules
- C) It removes the need for tests
- D) It serializes the policy to the database automatically

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Specifications compose with `and`, `or`, `not`, so the complement of the auto-merge policy *is* the review queue definition, and the partition is structural rather than a hope maintained by hand. The exercise demonstrates exactly this inversion. Speed (A), test elimination (C), and serialization (D) are not the pattern's purpose.
</details>

---

### Question 15
**Which statement best applies the lecture's proportionality guidance?**

- A) Every service, including health endpoints, needs full aggregate discipline
- B) A config-table CRUD service needs a rich domain model; anything less is an anemic model
- C) Full discipline where rules are dense and mistakes are expensive; a thin layer or none where the service is genuinely CRUD — but never the middle state of DTOs-only with rules scattered in controllers
- D) Domain-driven design applies only to non-AI backends

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The literature's own guidance — and section 14's — is that DDD is expensive overhead that pays for itself only where the domain is complex. The trap is not skipping the model (A, B both over-model); it is the unclaimed middle: "models" that are really DTOs while the business rules accrete in five services with no enforcement point. (D) is false — the Athar and resolution domains in this lecture are exactly AI-stack domains.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Easy | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Easy | | |
| 13 | Hard | | |
| 14 | Hard | | |
| 15 | Hard | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 6 | B | 11 | B |
| 2 | B | 7 | C | 12 | B |
| 3 | B | 8 | B | 13 | B |
| 4 | B | 9 | B | 14 | B |
| 5 | B | 10 | C | 15 | C |

---

*Generated for AI Engineer Lab System Design Track - Quiz 01 of the domain-modeling lane*
